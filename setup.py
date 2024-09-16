import asyncio
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
def unpredictable_problem():
    print("\033[31m" + "ERROR" + "\033[0m" + ":" "     Unpredictable problem detected Exiting...")
    os._exit(0)
try:
    from Siosk.package.TTS import TextToSpeech
    import platform
    import subprocess
    import SioskServer.router.download as download
    import zipfile
    import os
    import shutil
    from tqdm import tqdm
    import time
    import requests
except:
    unpredictable_problem()

class SetupProcess:
    def __init__(self) -> None:
        self.OS = platform.system()
        self.vcredist_versions = [
            '14.0',  # Visual C++ 2015
            '14.1',  # Visual C++ 2017
            '14.2',  # Visual C++ 2019 & 2022
        ]
        self.command_unix = [
            "pip3",
            "install",
            "-r",
            "setup/requirements_unix.txt"
        ]
        
    def downloading_vc_redist(self):
        self.checking_validation_vc_redist()
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     None visual studio redistributable C++ Package detected...")
        url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        download_path = "setup/vc_redist.x64.exe"
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Sending Request to vc_redist.x64.exe file...")
        response = requests.get(url)
        with open(download_path, 'wb') as file:
            file.write(response.content)
        try:
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Setting env - vc_redist.x64....")
            subprocess.run([download_path, '/install', '/passive', '/norestart'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error happened while donwloading..: {e}")

    def checking_validation_vc_redist(self):
        for version in range(len(self.vcredist_versions)):
            try:
                import winreg
                reg_path = rf"SOFTWARE\Microsoft\VisualStudio\{self.vcredist_versions[version]}\VC\Runtimes\x64"
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
                installed = winreg.QueryValueEx(registry_key, 'Installed')[0]
                if installed == 1:
                    return True
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Error happened while checking vc_redist existence: {e}")
                return False
        return False

    def audio_check(self):
        return os.path.exists("Siosk/assets/audio") and os.path.isdir("Siosk/assets/audio")

    def unziping_dll(self, zip_file_path, extract_to, move_to):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            total_files = len(zip_ref.namelist())
            progress_bar = tqdm(total=total_files, desc="Extracting files", unit="file")
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith('.dll'):
                    extracted_path = zip_ref.extract(file_name, extract_to)
                    if not os.path.exists(move_to):
                        os.makedirs(move_to)
                    destination_path = os.path.join(move_to, os.path.basename(file_name))
                    shutil.move(extracted_path, destination_path)
                    progress_bar.update(1)
                    time.sleep(0.5) 
                    progress_bar.close()
                    return
            progress_bar.close()

    def setup_process(self):
        download.download_file(file="conversation.json", save_dir="Siosk/package/")
        if self.OS == "Windows":
            if self.audio_check() == False:
                print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Downloading TTS Data...\n")
                texttospeech = TextToSpeech()
                asyncio.run(texttospeech.downloading())
            if self.checking_validation_vc_redist() == False:
                self.downloading_vc_redist()
            self.unziping_dll("assets/torch_cpu.zip", "_internal/torch/lib", "_internal/torch/lib")
        else:
            if not os.path.exists("Siosk/assets/audio"):
                texttospeech = TextToSpeech()
                print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Downloading TTS Data...\n")
                asyncio.run(texttospeech.downloading())
                subprocess.run(self.command_unix)
        try:
            from SioskServer.server import process
            sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
            process()    
        except:
            unpredictable_problem()
            
if __name__ == "__main__":
    setupprocess = SetupProcess()
    setupprocess.setup_process() 