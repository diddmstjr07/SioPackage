import subprocess
from Siosk.package.error_manage import ServerPortUsingError
import time
import platform

os_system = platform.system()

def windows_track(port) -> int:
    port = str(port)
    def extract_pid_from_line(line) -> int:
        fields = str(line).split()
        if len(fields) >= 5:
            pid_str = fields[4]
        if pid_str.isdigit():
            return int(pid_str)
        return None
    
    def extract_pids_from_ps_output(ps_output) -> list:
        lines = str(ps_output).splitlines()
        pids = [extract_pid_from_line(line) for line in lines if extract_pid_from_line(line) is not None]
        return pids
    
    try:
        command = ["netstat", "-ano", "|", "findstr", port]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        pids = extract_pids_from_ps_output(stdout)
        for pid_index, pid_val in enumerate(pids):
            process = subprocess.Popen(f"tasklist /FI \"PID eq {pid_val}\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            program = stdout.split("\n")[3].split(" ")[0]
            if "python" in program:
                return f"{program} | {str(pid_val)}"
        return True, "None"
    except Exception as e:
        return False, program

def unix_track(port):
    result = subprocess.check_output(['lsof', '-i', f':{port}'])
    result = result.decode('utf-8').strip().split('\n')
    if len(result) > 1:
        header = result[0]
        process_info = result[1].split()
        process_name = str(process_info[0])
        processer = process_name[:6]
        if processer == "Python" or processer == "python":
            pid = process_info[1]
            return f"{process_name} | {pid}"
        else:
            return False, processer
    else:
        return True, processer
    
def linux_track(port):
    result = subprocess.check_output(['lsof', '-i', f':{port}'])
    result = result.decode('utf-8').strip().split('\n')
    if len(result) > 1:
        return f"Python | PID"
    else:
        return True, "None"

def find_process_by_port(port):
    try:
        if os_system == "Windows":
            try:
                return_data, processer = windows_track(port)
            except ValueError:
                return_data = windows_track(port)
        else:
            try:
                return_data, processer = unix_track(port)
            except ValueError:
                return_data = unix_track(port)

        if return_data == False:
            print("\033[1;31m" + "ERROR" + "\033[0m" + ":" + f"     Is there any process is working on Port 9460? | {processer} is running currently")
            raise ServerPortUsingError
        elif return_data == True:
            result_data =  f'No process found using port {port}'
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
            return False
        else:
            process_name, pid = str(return_data).split(" | ")
            result_data = f'1 process found using port http://127.0.0.1:9460 name: {process_name}, PID: {pid}'
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
            return True
        
    except subprocess.CalledProcessError:
        result_data =  f'No process found using port {port}'
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
        return False

def find_process_by_port_Voice(port):
    try:
        if os_system == "Windows":
                try:
                    return_data, processer = windows_track(port)
                except ValueError:
                    return_data = windows_track(port)
        elif os_system == "Darwin":
                try:
                    return_data, processer = unix_track(port)
                except ValueError:
                    return_data = unix_track(port)
        elif os_system == "Linux":
                try:
                    return_data, processer = linux_track(port)
                except ValueError:
                    return_data = linux_track(port)
        
        if return_data == False:
            print("\033[1;31m" + "ERROR" + "\033[0m" + ":" + f"     Is there any process is working on Port 9460? | {processer} is running currently")
            raise ServerPortUsingError
        elif return_data == True:
            result_data =  f'No process found using port {port}'
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
            time.sleep(1)
            return False
        else:
            process_name, pid = str(return_data).split(" | ")
            result_data = f'1 process found using port http://127.0.0.1:9460 name: {process_name}, PID: {pid}'
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
            time.sleep(1)
            return True
        
    except subprocess.CalledProcessError:
        result_data =  f'No process found using port {port}'
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {result_data}")
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Directing...")
        time.sleep(1)
        return False

