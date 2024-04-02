# DXing Radio Waves with Python and Rust

## Overview
This project provides a framework for DXing radio waves using a combination of Python and Rust. Python is used for high-level control and data analysis, while Rust is employed for efficient low-level signal processing.

## Requirements
- Rust Programming Language
- Python 3.7 or higher
- PySDR (or similar SDR Python library)

## Installation

### Rust Library
- Navigate to the Rust project directory.
- Run `cargo build --release` to compile the Rust code into a shared library.

### Python
- Ensure all Python dependencies are installed via `pip`.

## Usage
- Use `dxing.py` to start the program.
- The script interacts with an SDR to acquire radio signals and processes them using the Rust library.

## Structure
- `dxing.py`: Main Python script for DXing.
- `lib.rs`: Rust library for efficient signal processing.
- `Cargo.toml`: Configuration for Rust compilation.

## Enhancements
- Implement specific modulation/demodulation techniques in Rust.
- Expand Python script for better data visualization and user interaction.
- Include error handling and logging for robust operation.
