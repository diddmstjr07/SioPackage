import requests
import os
import warnings

warnings.simplefilter("ignore")

def download_file(
        api_url="https://anoask.site:1121/api", 
        api_key="SioskKioskFixedTokenVerifyingTokenData", 
        file:str = None, 
        save_dir:str = None
    ):
    """
    FastAPI 서버에서 파일을 다운로드합니다.

    Args:
        api_url: API 엔드포인트 URL
        api_key: API 키 (토큰)
        file_path: 서버에서 다운로드할 파일의 경로
        save_dir: 다운로드한 파일을 저장할 디렉토리
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    params = {"token": api_key, "file_path": file}
    try:
        response = requests.get(api_url, params=params, stream=True, verify=False)
        response.raise_for_status()
        save_path = os.path.join(save_dir, file)

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     {file} downloading Completed")
    except requests.exceptions.RequestException as e:
        print("\033[31m" + "ERROR" + "\033[0m" + ": " f"     {file} downloading ERROR: {e}")
