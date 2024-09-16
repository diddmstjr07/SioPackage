import ctypes
import time
import platform
import os

os_system = platform.system()

def play_wav(file_path):
    if os_system == "Windows":
        ctypes.windll.winmm.mciSendStringW(f"open \"{file_path}\" type mpegvideo alias wav", None, 0, None)
        ctypes.windll.winmm.mciSendStringW("play wav", None, 0, None)

        while True:
            state = ctypes.create_string_buffer(128)
            ctypes.windll.winmm.mciSendStringW("status wav mode", state, 128, None)
            if state.value.decode().strip() == "s":
                break
            time.sleep(0.1)

        ctypes.windll.winmm.mciSendStringW("stop wav", None, 0, None)
        ctypes.windll.winmm.mciSendStringW("close wav", None, 0, None)
    elif os_system == "Darwin":
        os.system(f"afplay {file_path}")
    elif os_system == "Linux":
        os.system(f"aplay {file_path}")