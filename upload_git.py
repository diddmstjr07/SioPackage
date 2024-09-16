import subprocess

def run_git_command(directory, commands):
    try:
        subprocess.run(commands, cwd=directory, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {commands} in directory {directory}: {e}")
        raise

def main():
    commandary = input("Commit할 대상 디렉토리 명을 작성해주세요 (둘다인 경우, 'all'): ")
    commit_index = input("Commit 구문을 작성해주세요: ")

    try:
        run_git_command("Siosk", ["git", "checkout", "main"])
        run_git_command("SioskUI", ["git", "checkout", "main"])
        run_git_command("SioskServer", ["git", "checkout", "main"])
        run_git_command(".", ["git", "checkout", "main"])
    except subprocess.CalledProcessError:
        pass

    if commandary == "Siosk" or commandary == "all":
        try:
            run_git_command("Siosk", ["git", "init"]) 
            run_git_command("Siosk", ["git", "add", "."])
            run_git_command("Siosk", ["git", "commit", "-m", commit_index])
            run_git_command("Siosk", ["git", "push", "https://github.com/diddmstjr07/Siosk.git", "main", "--force"])
        except subprocess.CalledProcessError:
            pass
    
    if commandary == "SioskUI" or commandary == "all":
        try:
            run_git_command("SioskUI", ["git", "init"])
            run_git_command("SioskUI", ["git", "add", "."])
            run_git_command("SioskUI", ["git", "commit", "-m", commit_index])
            run_git_command("SioskUI", ["git", "push", "https://github.com/diddmstjr07/SioskUI.git", "main", "--force"])
        except subprocess.CalledProcessError:
            pass

    if commandary == "SioskServer" or commandary == "all":
        try:
            run_git_command("SioskServer", ["git", "init"])
            run_git_command("SioskServer", ["git", "add", "."])
            run_git_command("SioskServer", ["git", "commit", "-m", commit_index])
            run_git_command("SioskServer", ["git", "push", "https://github.com/diddmstjr07/SioskServer.git", "main", "--force"])
        except subprocess.CalledProcessError:
            pass
    
    if commandary == "all" or commandary == "Siosk" or commandary == "SioskUI" or commandary == "SioskServer":
        try:
            run_git_command(".", ["git", "submodule", "update", "--init", "--recursive", "--remote"])
            run_git_command(".", ["git", "init"])
            run_git_command(".", ["git", "add", "."])
            run_git_command(".", ["git", "commit", "-m", commit_index])
            run_git_command(".", ["git", "push", "https://github.com/diddmstjr07/SioPackage.git", "main", "--force"])
        except subprocess.CalledProcessError:
            pass

if __name__ == "__main__":
    main()