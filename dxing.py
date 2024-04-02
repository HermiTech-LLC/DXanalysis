import ctypes
import numpy as np
import logging
import asyncio
from configparser import ConfigParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = ConfigParser()
config.read('config.ini')
lib_path = config.get('DEFAULT', 'RustLibPath', fallback='dxing_lib.so')

try:
    rust_lib = ctypes.CDLL(lib_path)
except OSError as e:
    logger.error(f"Failed to load Rust library: {e}")
    raise

process_data = rust_lib.process_data
process_data.argtypes = [np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_size_t]
process_data.restype = None

async def dxing_process(input_signal):
    if not isinstance(input_signal, np.ndarray):
        raise ValueError("Input signal must be a numpy array")

    process_data(input_signal, len(input_signal))

    await asyncio.sleep(0)  # Placeholder for async calls

    return input_signal
