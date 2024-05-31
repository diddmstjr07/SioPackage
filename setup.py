import subprocess
from Siosk.package.error_manage import NondirectoryError
from Siosk.package.error_manage import IncorrectArgSelectError
from auto.delete import delete_dot_underscore_files

class CheckArguments:
    def __init__(self) -> None:
        import sys
        import os
        self.arg = sys.argv
        self.version = sys.executable
        self.os = os
    
    def brewfunc(self, argument):
        brew_command = [
            "brew",
            argument,
            "--force",
            "portaudio",
            "sox",
            "python-tk"
        ]
        return brew_command

    def commandfunc(self, version, argument):
        if version == None:
            package_manager_route = "pip"
            command = [
                package_manager_route,
                argument,
                "-r",
                "requirements.txt"
            ]
            return command, version
    
        else:
            package_manager_route = "pip" + version
            command = [
                package_manager_route,
                argument,
                "-r",
                "requirements.txt"
            ]
            return command, version
    
    def argument_check(self):
        if self.arg[-1] == "install":
            return self.install(), "install"
        elif self.arg[-1] == "uninstall":
            return self.uninstall(), "uninstall"
        elif self.arg[-1] == "--help" or self.arg[-1] == "--h":
            print("\n[install] | [uninstall] | [--pip (version)]\nArgument grammer -> Generally, using only install argument download can be done")
            print("'python setup.py install'")
            print("'python setup.py uninstall'")
            print("However if you using python and pip version diffirent you can set,")
            print("--pip (version), Example 'python setup.py --pip 3.8 install'\n")
            self.os._exit(0)
        else:
            IncorrectArgSelectError

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
        version, argument = arguments.argument_check()
        command, version = arguments.commandfunc(version, argument)
        brew_command = arguments.brewfunc(argument)
        subprocess.run(brew_command)
        subprocess.run(command)
        with open("./Siosk/log/setup.log", 'w') as w:
            w.write(str(version))
    except IncorrectArgSelectError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " "Incorrect arugment typed. Please reprocess your code again.")
        print("Did you add argument install?")
        print("It usaully works Automatically but if you want, you should mention argument after '--pip' For Example '--pip 3.8'")
        print("For more instruction, Please add --h or --help argument.\n")
        raise IncorrectArgSelectError
    except FileNotFoundError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " f"Non Correct Access. Please Check your argments!!")
        print("There is none pip in this OS. Please add --pip to Process this setup.")
        raise NondirectoryError
    except TypeError:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " "Incorrect arugment typed. Please reprocess your code again.")
        print("Did you add argument install?")
        print("It usaully works Automatically but if you want, you should mention argument after '--pip' For Example '--pip 3.8'")
        print("For more instruction, Please add --h or --help argument.")

if __name__ == "__main__":
    __setup__()
    delete_dot_underscore_files()