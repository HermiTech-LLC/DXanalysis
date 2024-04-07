use std::slice;
use log::{error, info};
use rustfft::{FftPlanner, num_complex::Complex};
use serde_json::json;
use reqwest;

fn apply_moving_average_filter(data: &mut [f64], window_size: usize) {
    let mut filtered_data = vec![0.0; data.len()];
    let divisor = window_size as f64;

    for i in 0..data.len() {
        let window_start = if i >= window_size { i - window_size + 1 } else { 0 };
        filtered_data[i] = data[window_start..=i].iter().sum::<f64>() / divisor;
    }

    data.copy_from_slice(&filtered_data);
}

fn apply_fft(data: &mut [f64]) {
    let mut input: Vec<Complex<f64>> = data.iter().map(|&x| Complex::new(x, 0.0)).collect();
    let mut output = vec![Complex::new(0.0, 0.0); data.len()];

    let mut planner = FftPlanner::new();
    let fft = planner.plan_fft_forward(data.len());
    fft.process(&mut input, &mut output);

    for i in 0..data.len() {
        data[i] = output[i].norm();
    }
}

fn apply_ml_pattern_recognition(data: &[f64]) -> Result<(), reqwest::Error> {
    let data_json = json!({ "data": data });

    let client = reqwest::blocking::Client::new();
    let res = client.post("http://your_ml_model_api_endpoint")
        .json(&data_json)
        .send()?;

    if res.status().is_success() {
        let response_data = res.json::<serde_json::Value>()?;
        info!("Pattern recognition successful: {:?}", response_data);
    } else {
        error!("Pattern recognition failed");
    }

    Ok(())
}

#[no_mangle]
pub extern "C" fn process_data(data_ptr: *mut f64, data_len: usize) -> bool {
    let data = unsafe { 
        if data_ptr.is_null() {
            error!("Null pointer provided to process_data");
            return false;
        }
        slice::from_raw_parts_mut(data_ptr, data_len)
    };

    apply_moving_average_filter(data, 5);
    apply_fft(data);

    if let Err(e) = apply_ml_pattern_recognition(data) {
        error!("Error in ML pattern recognition: {:?}", e);
        return false;
    }

    info!("Data processing completed successfully");
    true
}