from .neuron import NeuronAggregate
from Siosk.package.anoask import Api
from Siosk.package.TTS import TextToSpeech
from Siosk.package.audio import AudioRecorder
from Siosk.package.exit_manager import EXITING
import os
import six
import asyncio
import time

class API:
    def __init__(self, token, url) -> str:
        self.token = token # Api Token
        self.url = url # Sending url
        self.TextToSpeech = TextToSpeech()

    # def access_server(self):
    #     start_time = time.time()
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         sock.connect(("pwnbit.kr", 443))
    #         response = requests.get(f"{self.url}:9460/access?token={self.token}&host={os.getlogin()}&ip={sock.getsockname()[0]}", verify=False) # 쿼리문자열을 활용한 Get 요청을 보냄 
    #         result = response.json()['message'] # json 데이터로 추출하여 detail 키에 대한 값을 변수에 저장
    #         if result == 'error': # 토큰이 부적절한 경우 에러 메세지를 띄움
    #             webbrowser.open(self.url)
    #             print("\033[31m" + '403 Refused Error' + "\033[0m" + ': None Coincide Token values, Please check if your token is expired')
    #             print('to get new token, please visit https://anoask.site and login to issue')
    #             raise ConnectionRefusedError
    #     except KeyError: # 키에러인 경우, 적절하게 반환된 결과이기 때문에, 추출
    #         result = response.json()['message'] # 결과 추출
    #         end_time = time.time() # 종료
    #         embedding_time = end_time - start_time # 임배디드 시간 측정
    #         return result, embedding_time # 결과나 임배디드 시간 반환
    #     except requests.exceptions.ConnectionError:
    #         print("\033[31m" + '404 Refused Error' + "\033[0m" + ': Server is downed... Please Contact us we will found problem immediately') # 연결 에러인 경우, 서버 다운 메세지 출력
    #         raise ServerDownedError

    def load_models(self, record: AudioRecorder):
        api = Api(url=self.url) 
        Neuron = NeuronAggregate(record) # 음성관련 class 호출 
        return api, Neuron

    def preparing(self, recorder: AudioRecorder): # 준비 함수 
        api, Neuron = self.load_models(recorder) # api -> get 요청할때 사용, Neuron -> 마이크 선택과 음성 변환
        index = Neuron.Detection() # 마이크 선택
        recorder.get_mic_selection(index)
        self.api = api # 인스턴스 변수로 선언
        self.index = index # 인스턴스 변수로 선언
        self.Neuron = Neuron # 인스턴스 변수로 선언

    def texture_load_models(self):
        api = Api(url=self.url) # 클래스 매게변수로써 지정
        return api # 클래쓰 변수를 return 

    def texture_preparing(self):
        api = self.texture_load_models() # return한 클래쓰 변수를 변수에 저장
        self.api = api # 인스턴스 변수로써 클래쓰를 호출하여 저장

    def texture(self, keyword):
        if isinstance(keyword, six.string_types):  # keyword의 종류가 문자열인지 확인
            Q, A, F, embedding_time = self.api.send_response(self.token, keyword) # 위에서 매개변수로 삼은 token과 받은 keyword를 매개변수로써 전송
            return Q, A, F, embedding_time # 다시 결과와 시간을 return
        else:
            EXITING() # 문자의 종류가 str이 아닌 경우 exit

    def detection(self, ques:str, result:str, flag:str): # API로부터 반환되어진 result 값을 인자로
        filename = str("Siosk/assets/audio/" + result.replace('?', ";") + ".mp3") # file name creation
        file_path = os.path.abspath(filename)
        if os.path.exists(file_path): # 있다면,
            print(file_path)
            asyncio.run(self.TextToSpeech.voice(target=False, resultment=file_path, flag=True)) # 그 파일 재생하기
        else: # 없으면
            asyncio.run(self.TextToSpeech.voice(target=result, resultment=False, flag=False)) # 그자리에서 재생하기
        
    def classifying(self, Q:str, F):
        if F == '3':
            splited_menu = Q.split(" 줄래?")[0]
        elif F == '4':
            splited_menu = str(Q.split(" 줘")[0])[0]
            if splited_menu == "한":
                splited_menu = '1'
            elif splited_menu == "두":
                splited_menu = '2'
            elif splited_menu == "세":
                splited_menu = '3'
            elif splited_menu == "네":
                splited_menu = '4'
            elif splited_menu == "다":
                splited_menu = '5'
            elif splited_menu == "여":
                splited_menu = '6'
        elif F == '5':
            if Q == "차갑게 줘":
                splited_menu = "Cold"
            elif Q == "따뜻하게 줘":
                splited_menu = "Warm"
        elif F == '6':
            if Q == "네" or Q == "어" or Q == "그래" or Q == "넣어줘" or Q == "장바구니에 넣어줘":
                splited_menu = True
            else:
                splited_menu = False
        elif F == '7':
            if Q == '주문할게' or Q == '결제할게' or Q == '취소할게':
                splited_menu = "order"
        else:
            splited_menu = Q
        return splited_menu
    
    def logger(self, classified, flag):
        file_path = 'Siosk/package/log/logger.log'
        is_empty = True
        with open(file_path, 'r', encoding='utf-8') as file:
            if file.read(1) != "":
                is_empty = False
        with open(file_path, 'a', encoding='utf-8') as mod:
            if is_empty == False:
                mod.write('\n')
                mod.write(str(classified) + " | " + str(flag))
            else:
                mod.write(str(classified) + " | " + str(flag))
    
    def detecting(self): # SioPackage/main.py 
        total_st_time = time.time()
        self.keyword, time_step = self.Neuron.Trans() # 음성 정보를 keyword로써 변환후 변수에 저장
        st = time.time()
        Q, A, F, embedding_time = self.api.send_response(self.token, self.keyword) # 위에서 매개변수로 삼은 token과 받은 keyword를 매개변수로써 전송
        en = time.time()
        total_en_time = time.time()
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Answer creation term: ", embedding_time)
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Server response time: ", en - st)
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Total taken time: {total_en_time - total_st_time}")
        classified = self.classifying(Q, F)
        self.logger(classified=classified, flag=F)
        self.detection(Q, A, F) # detection 함수 호출 여기가 말하는 부분 TTS
        return A