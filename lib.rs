use std::slice;

#[no_mangle]
pub extern "C" fn process_data(data_ptr: *mut f64, data_len: usize) {
    let data = unsafe {
        assert!(!data_ptr.is_null());
        slice::from_raw_parts_mut(data_ptr, data_len)
    };

    // Here, you can process the data
    // Example: simple in-place transformation
    for i in 0..data_len {
        data[i] = data[i] * 2.0; // Example operation
    }
}
