import requests
from urllib3.exceptions import InsecureRequestWarning
import time
from Siosk.package.error_manage import ConnectionRefusedError, ServerDownedError, ServerSyntexError
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import webbrowser
import socket

class Api: # Server Connection
    def __init__(self, url) -> str:
        self.url = url # url classify variable

    def send_response(self, token, ques): # token, ques을 매개변수로 받음
        start_time = time.time()
        try:
            response = requests.get(f"{self.url}:9460/api?token={token}&ques={ques}", verify=False) # 쿼리문자열을 활용한 Get 요청을 보냄 
            result = response.json()['detail'] # json 데이터로 추출하여 detail 키에 대한 값을 변수에 저장
            if result == 'error': # 토큰이 부적절한 경우 에러 메세지를 띄움
                webbrowser.open(self.url)
                print("\033[31m" + '403 Refused Error' + "\033[0m" + ': None Coincide Token values, Please check if your token is expired')
                print('to get new token, please visit https://anoask.site and login to issue')
                raise ConnectionRefusedError
        except KeyError: # 키에러인 경우, 적절하게 반환된 결과이기 때문에, 추출
            result = response.json()['message'] # 결과 추출
            Q = str(result).split(" | ")[0]
            A = str(result).split(" | ")[1]
            F = str(result).split(" | ")[2]
            end_time = time.time() # 종료
            embedding_time = end_time - start_time # 임배디드 시간 측정
            return Q, A, F, embedding_time # 결과나 임배디드 시간 반환
        except requests.exceptions.ConnectionError:
            print("\033[31m" + '404 Refused Error' + "\033[0m" + ': Server is downed... Please Contact us we will found problem immediately') # 연결 에러인 경우, 서버 다운 메세지 출력
            raise ServerDownedError
        except requests.exceptions.JSONDecodeError:
            print("\033[31m" + '404 Refused Error' + "\033[0m" + ': Server Syntex error happened... Please Contact us we will found problem immediately') # 연결 에러인 경우, 서버 다운 메세지 출력
            raise ServerSyntexError
