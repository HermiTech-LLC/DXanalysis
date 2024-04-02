import wx
import ctypes
import numpy as np
import logging
from configparser import ConfigParser
from wx import FileDialog

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration and Rust library
config = ConfigParser()
config.read('config.ini')
lib_path = config.get('DEFAULT', 'RustLibPath', fallback='dxing_lib.so')

try:
    rust_lib = ctypes.CDLL(lib_path)
except OSError as e:
    logger.error(f"Failed to load Rust library: {e}")
    raise

# Define the interface to the Rust function
process_data = rust_lib.process_data
process_data.argtypes = [np.ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_size_t]
process_data.restype = ctypes.c_bool

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Signal and Sensor Analysis", size=(600, 400))
        panel = wx.Panel(self)

        self.load_button = wx.Button(panel, label="Load Signal")
        self.process_button = wx.Button(panel, label="Process Signal")
        self.result_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL)

        self.load_button.Bind(wx.EVT_BUTTON, self.on_load_signal)
        self.process_button.Bind(wx.EVT_BUTTON, self.on_process_signal)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.load_button, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.process_button, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.result_text, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.input_signal = None

    def on_load_signal(self, event):
        with FileDialog(self, "Open Signal Data File", wildcard="Data files (*.dat)|*.dat", 
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the action

            # Proceed to load the file
            path = fileDialog.GetPath()
            try:
                # Assuming the file contains an array in text format
                self.input_signal = np.loadtxt(path)
                logger.info("Signal loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load file: {e}")

    def on_process_signal(self, event):
        if self.input_signal is None:
            logger.error("No signal loaded")
            return

        if not isinstance(self.input_signal, np.ndarray):
            logger.error("Loaded signal is not a numpy array")
            return

        success = process_data(self.input_signal, len(self.input_signal))

        if success:
            self.result_text.SetValue(f"Processed Signal:\n{np.array_str(self.input_signal)}")
        else:
            logger.error("Signal processing failed")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()