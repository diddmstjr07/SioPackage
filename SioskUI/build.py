import subprocess
import ftplib

ftp_server = 'anoask.site'
ftp_username = 'diddmstjr'
ftp_password = 'soso0909@'
file_to_upload = './build/apk/app-release.apk'
remote_directory = '/' 
remote_file_name = 'app-release.apk'  

subprocess.run([
    "flet",
    "build",
    "apk",
    "--verbose"
])

try:
    ftp = ftplib.FTP(ftp_server)
    ftp.login(ftp_username, ftp_password)
    ftp.cwd(remote_directory)
    print(f'Contents of {remote_directory}:')
    ftp.retrlines('LIST')
    remote_file_path = f'{remote_directory}{remote_file_name}'

    with open(file_to_upload, 'rb') as file:
        ftp.storbinary(f'STOR {remote_file_path}', file)

    ftp.quit()
    print(f'Successfully uploaded {file_to_upload} to {remote_file_path}')
except ftplib.all_errors as e:
    print(f'FTP error: {e}')
except FileNotFoundError:
    print(f'File not found: {file_to_upload}')
except Exception as e:
    print(f'An error occurred: {e}')
