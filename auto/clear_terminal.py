import platform

os_system = platform.system()

def clear_terminal():
    if os_system == "Windows":
        return "cls"
    else:
        return "clear"