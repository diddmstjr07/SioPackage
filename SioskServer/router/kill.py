import subprocess
import platform

class KillProcess:
    def __init__(self) -> None:
        self.os_type = platform.system()
        if self.os_type == "Windows":
            self.command = "netstat -ano | findstr :9460"
        else: 
            self.command = ["lsof", "-i", ":9460"]

    def kill(self, pids):
        if len(pids) > 0:
            print("\033[1;32mINFO\033[0m:\033[1;32m     Kill Process Detected... Starting\033[0m")
        else:
            print("\033[1;32mINFO\033[0m:\033[1;32m     Kill Process Non-Detected... Finishing\033[0m")
            return False
        pid = ""
        for pid_id in pids:
            if self.os_type == "Windows":
                kill_command = ["taskkill", "/F", "/PID", str(pid_id)]
            else:
                kill_command = ["kill", "-9", str(pid_id)]
            
            pid += str(pid_id) + ", "
            process = subprocess.Popen(kill_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
        print("\033[1;32mINFO\033[0m:\033[1;32m     Killing Process Successfully Finished ---> \033[0m\033[1;31m[{}]\033[0m".format(pid[:len(pid) - 2]))

    def extract_pid_from_line(self, line) -> int:
        fields = str(line).split()
        if self.os_type == "Windows":
            if len(fields) >= 5:
                pid_str = fields[-1]
        else:
            if len(fields) >= 2:
                pid_str = fields[1]
        
        if pid_str.isdigit():
            return int(pid_str)
        return None

    def extract_pids_from_ps_output(self, ps_output) -> list:
        lines = str(ps_output).splitlines()
        pids = [self.extract_pid_from_line(line) for line in lines if self.extract_pid_from_line(line) is not None]
        return pids

    def killing(self):
        if self.os_type == "Windows":
            process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        pids = self.extract_pids_from_ps_output(stdout)
        self.kill(pids)

if __name__ == "__main__":
    kp = KillProcess()
    kp.killing()
