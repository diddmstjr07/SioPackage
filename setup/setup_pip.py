import subprocess
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Siosk_en.package.error_manage import NondirectoryError, IncorrectArgSelectError
from auto.delete import delete_dot_underscore_files
import platform
import os

class CheckArguments:
    def __init__(self) -> None:
        import sys
        import os
        self.arg = sys.argv
        self.version = sys.executable
        self.os = os
        self.platform = platform
    
    def windows_commandfunc(self, version, argument):
        if version == None:
            package_manager_route = "pip"
            command = [
                package_manager_route,
                argument,
                "-r",
                "setup/requirements.txt"
            ]
            return command, version
    
        else:
            package_manager_route = "pip" + version
            command = [
                package_manager_route,
                argument,
                "-r",
                "setup/requirements.txt"
            ]
            return command, version
    
    def unix_commandfunc(self, version, argument):
        if version == None:
            package_manager_route = "pip"
            command = [
                package_manager_route,
                argument,
                "-r",
                "setup/requirements_unix.txt"
            ]
            return command, version
    
        else:
            package_manager_route = "pip" + version
            command = [
                package_manager_route,
                argument,
                "-r",
                "setup/requirements_unix.txt"
            ]
            return command, version
    
    def linux_pyaudio(self):
        command = [
            "sudo",
            "apt",
            "update"
        ]
        command_1 = [
            "sudo",
            "apt",
            "install",
            "portaudio19-dev"
        ]
        subprocess.run(command)
        subprocess.run(command_1)
    
    def argument_check(self):
        if self.arg[-1] == "install":
            return self.install(), "install"
        elif self.arg[-1] == "uninstall":
            return self.uninstall(), "uninstall"
        elif self.arg[-1] == "--help" or self.arg[-1] == "--h":
            print("\n[install] | [uninstall] | [--pip (version)]\nArgument grammar -> Generally, using only install argument download can be done")
            print("'python setup.py install'")
            print("'python setup.py uninstall'")
            print("However if you are using different Python and pip versions, you can set:")
            print("--pip (version), Example 'python setup.py --pip 3.8 install'\n")
            self.os._exit(0)
        else:
            raise IncorrectArgSelectError

    def CheckOS(self):
        Operating_System = self.platform.system()
        if Operating_System == "Darwin":
            return 0
        elif Operating_System == "Windows":
            return 1
        elif Operating_System == "Linux":
            return 2

    def install(self):
        if len(self.arg) > 2:
            if len(self.arg) >= 4 and self.arg[1] == "--pip":
                return self.arg[2]
            elif len(self.arg) == 3 and self.arg[1] == "--pip":
                raise IncorrectArgSelectError
            else:
                raise IncorrectArgSelectError
        elif len(self.arg) == 2:
            version = self.version.split('/')[-1].split('python')[1]
            return version
            
    def uninstall(self):
        if len(self.arg) > 2:
            if len(self.arg) == 4 and self.arg[1] == "--pip":
                return self.arg[2]
            elif len(self.arg) == 3 and self.arg[1] == "--pip":
                raise IncorrectArgSelectError
            else:
                raise IncorrectArgSelectError
        elif len(self.arg) == 1:
            version = self.version.split('/')[-1].split('python')[1]
            return version

def __setup__():
    try:
        arguments = CheckArguments()
        OS = arguments.CheckOS()
        version, argument = arguments.argument_check()
        if OS == 0:
            command, version = arguments.unix_commandfunc(version, argument)
            subprocess.run(command)
        elif OS == 1:
            command, version = arguments.windows_commandfunc(version, argument)
            subprocess.run(command)
        elif OS == 2:
            arguments.linux_pyaudio()
            command, version = arguments.unix_commandfunc(version, argument)
            subprocess.run(command)
        
    except IncorrectArgSelectError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " "Incorrect argument typed. Please reprocess your code again.")
        print("Did you add the 'install' argument?")
        print("It usually works automatically, but if you want, you should mention the argument after '--pip'. For example, '--pip 3.8'.")
        print("For more instructions, please add '--h' or '--help' argument.\n")
        raise IncorrectArgSelectError
    except FileNotFoundError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " f"File not found. Please check your arguments!")
        print("There is no 'pip' in this OS. Please add '--pip' to process this setup.")
        raise NondirectoryError
    except TypeError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " "Incorrect argument typed. Please reprocess your code again.")
        print("Did you add the 'install' argument?")
        print("It usually works automatically, but if you want, you should mention the argument after '--pip'. For example, '--pip 3.8'.")
        print("For more instructions, please add '--h' or '--help' argument.")

if __name__ == "__main__":
    __setup__()
    delete_dot_underscore_files()
