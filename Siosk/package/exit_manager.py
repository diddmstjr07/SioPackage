import os
import psutil
import signal
import platform
import time
import sys
import threading
import itertools
import inspect

PID = 0

class Spinner:
    def __init__(self):
        self.done = False
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.thread = threading.Thread(target=self.animate)

    def animate(self):
        while not self.done:
            sys.stdout.write('\r' + "\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Exiting Service " + next(self.spinner))
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + "\033[1;32mINFO\033[0m:     Successfully killed 'Flet' Process")
        sys.stdout.flush()

    def start(self):
        self.thread.start()

    def stop(self):
        self.done = True
        self.thread.join()

def kill_flet_process():
    global PID
    spinner = Spinner()
    spinner.start()
    time.sleep(5)
    current_os = platform.system()
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'flet' in proc.info['name'].lower():
                pid = proc.info['pid']
                if current_os == "Windows":
                    os.system(f"taskkill /PID {pid} /F")
                else:
                    os.kill(pid, signal.SIGKILL)
                    PID = pid
                    spinner.stop()
            else:
                print("\033[1;32m" + "\nINFO" + "\033[0m" + ":" + f"     None Process named 'Flet'")
                os._exit(0)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"     Exception detected: {e}")

def EXITING():
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_lineno = caller_frame.lineno
    caller_function = caller_frame.function
    print("\033[1;32m" + "\nINFO" + "\033[0m" + ":" + f"     Process imported from File {caller_filename}, line {caller_lineno}, in {caller_function}")
    kill_flet_process()
    try:
        os.remove("Siosk/temp/temp.wav")
        os.remove("Siosk/package/conversation.json")
    except:
        pass
    os._exit(0)