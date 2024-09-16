from sentence_transformers import SentenceTransformer, util
import time
import os
import shutil
import json
import threading
import torch
import torch.nn as nn
from tqdm import tqdm

total_steps = 100
progress_bar = tqdm(total=total_steps)

def update_progress_bar(progress_bar, percentage):
    steps_to_add = (total_steps * percentage) / 100
    progress_bar.update(steps_to_add)

class CompareSimilaity:
    def __init__(self) -> str:
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)
        cache_folder = './database'
        model_name = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'
        model_cache_path = os.path.join(cache_folder, model_name.replace('/', '_'))
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        if os.path.exists(model_cache_path):
            shutil.rmtree(model_cache_path)
        # print("\033[1;32m" + "INFO" + "\033[0m" + ":" + "     Loading module Started")
        update_progress_bar(progress_bar, 50)
        self.model = SentenceTransformer(model_name, cache_folder=cache_folder) # 모델 선언
        # print("\033[1;32m" + "INFO" + "\033[0m" + ":" + "     Loading module Completed")
        update_progress_bar(progress_bar, 50)
        progress_bar.close()
        self.datas = []
        self.comparison = []
        self.dataset_data = []
        self.dataset_float = []
        self.ifdatasetedit = []
        if torch.backends.mps.is_available(): # GPU 사용 가능여부 검사
            self.device = torch.device("mps") # 가능한 경우, 설정
            # print("MPS device is available. Using GPU.")
        else:
            self.device = torch.device("cpu")
            # print("MPS device is not available. Using CPU.")
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + "     Loading fully Completed")
    
    def check_if_data(self):
        with open('./log/server.log', 'r') as r:
            data = r.read()
            if data != "None":
                print(data)
                return data
            else:
                return None
    
    def delay_blocker(self): # 에열 함수 -> CPU 부하로 인한 속도 느려짐 방지 함수
        blocker = [] # 배열 선언
        blocker.extend(["안녕", "안녕하세요"]) # 배열에 예시 데이터 포함
        start_time = time.time() # 타이머 셋
        embeddings = self.model.encode(blocker, convert_to_tensor=True, device=self.device) # 모델 호출
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]) # 데이터 유사도 검사
        end_time = time.time() # 타이머 종료
        embedded_time = end_time - start_time # 시간 측정
        # print(f"Test similarity: {similarity.item()}") # 유사도 출력
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Airing time: {str(embedded_time)[:4]} seconds")
    
    def getdata(self, threadnum): # threadnum으로 매개변수로써 함수 선언
        with open('./conversation.json', 'r') as r: # 예시 conversation data 열기
            data = json.load(r) # json 데이터로 변환
            data_keys = list(data.keys()) # key값 즉, 질문을 list화
            data_key_datas = data_keys # self. 로써 인스턴스 변수 선언
            data_values = list(data.values()) # values 값, 질문에 대한 답변을 list화 후, 인스턴스 변수 선언. 
            # print(data_keys)
            # print(data_values)
            length = len(data_keys) # 데이터의 개수의 길이를 length 변수에 저장
            tenth = length // threadnum
            data_keys_list = [data_keys[i*tenth:(i+1)*tenth] for i in range(threadnum)] 
        return data_key_datas, data_values, data_keys_list
            # 지정한 thread 개수로 1차 배열 내부의 2차 배열로써 데이터를 나누어 넣어준 데이터를 data_keys_list에 인스턴스 변수로써 저장하기

    def thread(self, ques, data_keys_list):
        # print(self.data_keys_list) # 위에서 인스턴스 변수 thread 개수로 나누어 저장한 data_keys_list를 출력
        threads = [threading.Thread(target=self.compare, args=(data_keys, ques, )) for data_keys in data_keys_list] # compare 함수에 
        # 1차 배열 내부에 존재하는 2차 배열의 개수를 기준으로 그 개수 만큼 thread를 생성후, thread 배열에 저장.
        [thread.start() for thread in threads] # 생성된 thread 개수 만큼 start
        [thread.join() for thread in threads] # 모든 thread가 끝날때까지 기다렸다가 join 하기
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(self.dataset_data)
        print(self.dataset_float)
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
    def compare(self, data_keys, ques):
        temporary_data = []
        comparison_float = []
        comparison_data = []
        for data_key in range(len(data_keys)): # 인수로 받은 2차 배열의 len 만큼 for문 돌리기
            # print(data_keys[data_key])
            sentences = [] # 인스턴스 변수로써 sentence 배열 선언해주기.
            # print(f"testing data: {data_keys[data_key]}") # 2차원 배열에 있는 testing data 1번 ~ 인덱스 출력
            # print(f"testing target: {ques}") # 질문 출력
            sentences.extend([data_keys[data_key], str(ques)]) # 위에서 선언한 sentence 배열에 비교 배열 extend하기
            start_time = time.time() # 타이머 시작
            import pdb
            embeddings = self.model.encode(sentences, convert_to_tensor=True, device=self.device) # 모델 호출 행렬로 다 쏴버리기
            pdb.set_trace()
            similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]) # 유사도 비교하기
            # print(f"Similarity: {similarity.item()}") # 유사도 출력
            comparison_float.append(float(similarity.item())) # 유사도를 위에서 선언한 비교_소수 배열에 append하기
            comparison_data.append(data_keys[data_key]) # 유사도를 위에서 선언한 비교_데이터 배열에 append하기
            end_time = time.time() # 타이머 끄기
            embedded_time = end_time - start_time # 소요 시간 재기
            # print("Embedding time: %0.2f seconds" % embedded_time) # 소요 시간 출력
            self.datas.append("%0.2f" % embedded_time) # 소요시간 append하기
            temporary_data.append(float(similarity.item())) # 소요시간 append하기
            number = 0 # number 변수 선언
        if float(max(temporary_data)) < 0.6:
            self.ifdatasetedit.append(True)
        else:
            self.ifdatasetedit.append(False)
        for data in range(len(self.datas)): # 위에서 for문을 통해 나온 소요 시간을 배열에 append한 배열의 길이 만큼 
            number += float(self.datas[data]) # number 변수에 += 하기
        aver_embedded = number / len(self.datas) # 평균 구하기
        # print("\033[32m" + "평균 답변 속도: %0.2f" % aver_embedded  + "\033[0m") # 소요 시간의 평균 출력하기
        self.dataset_data.append(comparison_data)
        self.dataset_float.append(comparison_float)

    def selecting_max(self):
        def check_index(final_values, max_element):
            for final_value in range(len(final_values)):
                for array_data in range(len(final_values[final_value])):
                    if max_element == final_values[final_value][array_data]:
                        return f"{final_value} {array_data}"
            return None
        check_amount_thread = len(self.dataset_float)
        temporary = []
        for j in range(check_amount_thread):
            first_final_value = max(self.dataset_float[j])
            temporary.append(first_final_value)
        final_value = max(temporary)
        index = check_index(self.dataset_float, final_value)
        demension_one, demension_two = index.split(" ")
        result = self.dataset_data[int(demension_one)][int(demension_two)]
        return result
        
    def __display__(self, question, data_key_datas, data_values):
        def check_dataset():
            for amount in range(len(self.ifdatasetedit)):
                if self.ifdatasetedit[amount] == False:
                    return None
            print(self.dataset_float)
            print("You must modify your dataset.")
        predict_key = self.selecting_max()
        check_dataset()
        for key in range(len(data_key_datas)): # data_key_datas 배열을 순회하면서, 
            if data_key_datas[key] == predict_key: # 데이터를 찾기
                predict_value = data_values[key] # predict value에 답변을 저장하기
                return predict_key, predict_value, question # 질문에 대한 index 값, 질문, 본래 질문, 질문에 대한 답을 return

class RunManage: # 선언
    def __init__(self, thread) -> int:
        self.compare = CompareSimilaity() 
        self.thread = thread
        self.speed_datas = []
        self.speedometer = []
        self.cpu_usage = []
        self.thread_counts = []
        self.compare.delay_blocker()

    def run(self, data):
        # 호출 # 메뉴가 뭐가 있을까요?, 아메리카노 한 잔과 블루베리 치즈케이크 먹고 싶어요, 포장할게요
        # input("Enter to start") # Enter Key 입력 기다리기
        question = data
        start_time = time.time() # 타이머 셋
        data_key_datas, data_values, data_keys_list = self.compare.getdata(self.thread) # 지정한 thread 개수 매개변수로 getdata 함수 호출
        self.compare.thread(question, data_keys_list) # 위에서 인스턴스로써 저장해준 변수를 활용하여 thread 함수 호출
        end_time = time.time() # 타이머 종료
        predict_key, predict_value, ques = self.compare.__display__(question, data_key_datas, data_values) # __display__ 호출
        print("사용자의 질문: " + ques)
        print("답변: " + predict_value)
        self.compare.dataset_data = []
        self.compare.dataset_float = []
        return end_time - start_time, ques, predict_key, predict_value
        # 1. embedded_time, 2. general question, 3. analyzed question, 4. analyzed response

'''
다른 아이디어가 생각이 났어. -> 기본 데이터 베이스에 기본적인 스크립트를 모두 저장해두고
이에 대한 유사도를 활용하여 상대한테 물어보는 방식으로 
1. 데이터 베이스를 순회하면서, 모든 데이터 베이스에서의 데이터에 대해서 유사성을 조사,
이에 대해서 가장 유사한 문장을 조사후 어떤 답변을 내놓아야 하는지에 대해서 미리
작성해둔 대로 답변을 해주어보자.
2. 말 사이사이의 구절을 분석해보자. -> 어떤 식으로 더욱 발전시켜 볼수 있을까?
(1) Embedded 시간을 평균 0.32초로 속도가 상당히 빠른 ChatGPT-4o 
    인데 이를 목표로 자동 응답 장치를 제작하여 보자. 
    그렇다면 현재 사용 모델인 snunlp/KR-SBERT-V40K-klueNLI-augSTS
    의 평균 Embedd 속도를 측정해보자.

    평균 Embedd 속도는 0.05로 거의 7배 정도로 ChatGPT 4o보다 빠른것을 알수 있음

Example)
카푸치노로 주문할게
카푸치노가 먹고 싶네? 카푸치노 줄래?
검사를 해봐야함 json 데이터 100 ~ 1000개를 평균적으로
읽어내는데에 드는 시간은 0.04초 ~ 0.05초 정도 결림
읽어야하는 대본이 100개 정도된다고 가정했을때 1개당 
비교하는데 걸리는 평균 시간 0.05초 가량 걸리기 때문에,
직접 비교하는데에 걸리는 시간은 0.5초가 걸린다고 일반적인
연산으로써 볼수 있을듯. 만약 thread를 활용하여 작업을 
진행한다고 가정하였을때, 0.5초보다는 더 빠른 속도가 나올 수는
있겠지만, 컴퓨터의 사양이 휠씬 높아야한다는 단점이 존재함
즉, ChatGPT 4o의 성능을 타겟팅으로써, 0.32초 보다 빠르게
하는 것을 목표로 진행을 해보야겠음. 

지금 속도가 느려지는 원인을 발견 -> 속도가 느려지던 상황에 대해서
탐구를 해보자 -> ftp를 활용하여 파일을 읽어서 similarity를
읽을때 속도가 감소
또, 현재 4GB SD 카드를 활용하여 데이터를 읽어 유사성을 파악할때
속도가 감소하는 현상을 확인할 수가 있었음.

즉, 속도 감소에 대한 현상을 해결하기 위해서는, 속도가 느린 장치가 아닌,
SSD를 활용하는, mac os 디스크를 활용해보자.

여전히 속도 지연 문제에 대해서는 해결되어지지 않는다.
여러번 시도후 프로그램을 시작한다면 문제가 생기지 않을 가능성이 보임
다시 시도해보자.

혹시 conda를 사용함에 있어서 문제가 생기는 것일까?
그건 아닌듯. 만약 컴퓨터 자체의 문제라면, 다른 환경에서 테스트 해보자.

Paralles 환경에서도 테스트 해보자 -> Mac OS 환경에서의 작동이 문제일
가능성도 있어 보임

Parrales 환경에서 테스트한 결과로는 Mac OS 환경보다는 눈에 띄게 확실히 
성능이 좋아졌지만, 아직도 여전히 0.3초에서 ~ 0.5초 정도의 성능을 보여주는
것으로 보여진다. 

2024.5.19 1:40:55 다시 서버가 복구되어서, 테스트를 해본 결과 기존과 같이 빠른속도로 결과의 도출이 됨
상당한 속도로 구현하는데에는 성공 -> 일반적인 키오스크에서도 구현이 되어야 하기 때문에, 빠른
시일 내에 라즈베리 파이에서도 구현해볼 예정 -> 되도록 우분투 환경을 사용할 예정

일단은 Thread를 사용하지 않은 상태의 최종 4개의 구문에 대해서 최종 소요 시간은 0.21207666397094727초 이다.
1차 시도 - 0.21207666397094727초
2차 시도 - 0.18360662460327148초
3차 시도 - 0.1938025951385498초
4차 시도 - 0.1900007724761963초
5차 시도 - 0.19924402236938477초

최대 0.21207666397094727초 최소 0.18360662460327148초

Tread는 내일 구현해보자 일단 자야지

Thread를 구현하기 전 발생하는 문제점을 발견 ->
testing data: 안녕하세요. 메뉴 좀 보고 싶은데요.
testing target: 어떤 메뉴가 있어?
Similarity: 0.6142719388008118
Embedding time: 0.12 seconds
Embedding average time: 0.12
위의 출력 결과를 살펴보면, 첫번째 문장 유사도 테스트의 경우에 속도 딜레이가 발생하는 것을 알수 있음
가설: 첫번째 세트를 테스트 함수를 생성하여 임의의 데이터 분석후 본 데이터 진입을 한다면 속도
딜레이가 발생하는 것을 방지할수 있을 가능성이 있음.

diddmstjr@diddmstjr:/dev/Cloud/Program/Siosk/Engine$ python similarity.py 
Enter to start
['안녕하세요. 메뉴 좀 보고 싶은데요.', '그럼 아메리카노 한 잔과 블루베리 치즈케이크 주문할게요.', '매장에서 먹도록 할게요', '포장해 가도록 할게요']
['네, 여기 메뉴판이 있습니다. 우리 카페의 인기 메뉴는 아메리카노와 카페 라떼입니다. 또한 시그니처 디저트로는 블루베리 치즈케이크가 있어요.', '알겠습니다. 아메리카노 한 잔과 블루베리 치즈케이크 주문 확인됐어요.', '알겠어요. 잠시만 기다려주세요.', '알겠어요. 잠시만 기다려주세요.']

(1)
testing data: 안녕하세요. 메뉴 좀 보고 싶은데요.
testing target: 어떤 메뉴가 있어?
Similarity: 0.6142719388008118
Embedding time: 0.13 seconds
Embedding average time: 0.13

<유사도를 측정하는데에 있어서 소요 시간 -> 0.13초>

(2)
testing data: 그럼 아메리카노 한 잔과 블루베리 치즈케이크 주문할게요.
testing target: 어떤 메뉴가 있어?
Similarity: 0.36289310455322266
Embedding time: 0.04 seconds
Embedding average time: 0.09

<유사도를 측정하는데에 있어서 소요 시간 -> 0.04초>

(3)
testing data: 매장에서 먹도록 할게요
testing target: 어떤 메뉴가 있어?
Similarity: 0.41276198625564575
Embedding time: 0.04 seconds
Embedding average time: 0.07

<유사도를 측정하는데에 있어서 소요 시간 -> 0.04초>

(4)
testing data: 포장해 가도록 할게요
testing target: 어떤 메뉴가 있어?
Similarity: 0.29179635643959045
Embedding time: 0.05 seconds
Embedding average time: 0.07

<유사도를 측정하는데에 있어서 소요 시간 -> 0.05초>

고유 질문: 어떤 메뉴가 있어?
예측 분석 질문: 안녕하세요. 메뉴 좀 보고 싶은데요.
예측 분석 답변: 네, 여기 메뉴판이 있습니다. 우리 카페의 인기 메뉴는 아메리카노와 카페 라떼입니다. 또한 시그니처 디저트로는 블루베리 치즈케이크가 있어요.
최종 소요 시간: 0.2765340805053711
0.04 + 0.04 + 0.05 + 0.13 = 0.26 sec -> 0.0165340805053711 sec은 json 데이터 100개 읽는데, 0.04sec 정도가 걸리는 점, 여러 상황
margin을 고려한다면 현실적인 시간. 
그렇다면 첫번째 과정에서 소요되어지는, 0.13sec를 단축하기 위해서는 
<가설> 보통 기계등에서 에열이라고 일컷는 작업을 하면되지 않을까? </가설>

Test 2.

['안녕하세요. 메뉴 좀 보고 싶은데요.', '그럼 아메리카노 한 잔과 블루베리 치즈케이크 주문할게요.', '매장에서 먹도록 할게요', '포장해 가도록 할게요']
['네, 여기 메뉴판이 있습니다. 우리 카페의 인기 메뉴는 아메리카노와 카페 라떼입니다. 또한 시그니처 디저트로는 블루베리 치즈케이크가 있어요.', '알겠습니다. 아메리카노 한 잔과 블루베리 치즈케이크 주문 확인됐어요.', '알겠어요. 잠시만 기다려주세요.', '알겠어요. 잠시만 기다려주세요.']

testing data: 안녕하세요. 메뉴 좀 보고 싶은데요.
testing target: 어떤 메뉴가 있어?
Similarity: 0.6142719388008118
Embedding time: 0.04 seconds
Embedding average time: 0.05

<유사도를 측정하는데에 있어서 소요 시간 -> 0.04초>

testing data: 그럼 아메리카노 한 잔과 블루베리 치즈케이크 주문할게요.
testing target: 어떤 메뉴가 있어?
Similarity: 0.36289310455322266
Embedding time: 0.06 seconds
Embedding average time: 0.05

<유사도를 측정하는데에 있어서 소요 시간 -> 0.06초>

testing data: 매장에서 먹도록 할게요
testing target: 어떤 메뉴가 있어?
Similarity: 0.41276198625564575
Embedding time: 0.04 seconds
Embedding average time: 0.05

<유사도를 측정하는데에 있어서 소요 시간 -> 0.04초>

testing data: 포장해 가도록 할게요
testing target: 어떤 메뉴가 있어?
Similarity: 0.29179635643959045
Embedding time: 0.04 seconds
Embedding average time: 0.05

<유사도를 측정하는데에 있어서 소요 시간 -> 0.04초>

고유 질문: 어떤 메뉴가 있어?
예측 분석 질문: 안녕하세요. 메뉴 좀 보고 싶은데요.
예측 분석 답변: 네, 여기 메뉴판이 있습니다. 우리 카페의 인기 메뉴는 아메리카노와 카페 라떼입니다. 또한 시그니처 디저트로는 블루베리 치즈케이크가 있어요.
최종 소요 시간: 0.18316173553466797

1차 결론 -> 첫번째 에열하는데 즉, 프로그램을 실행하고 처음으로 모델을 로드하는데에 걸린시간은 1-1에는 0.13sec
1에는 총 0.27sec 하지만, 두번째 실행부터, 2-1에는 0.04sec로 상당한 속도를 보여줌. 2에는 0.18sec 소요.
최종적으로 에열 단계를 걸친다면, 0.1sec 단축 가능.

대략 4시간 후, 모델 테스트 결과 -> 초기 애열 한번만 한다면, 속도 저하가 발생하지 않을 걸 알수 있음.
에열 함수를 만들어 보자.

애열 함수를 적용한 후, 100번의 연속성 테스트를 한 결과, 4개의 답변을 기준으로 하였을때, 
실행 속도는 0.19112460374832152sec로 만약 답변이 100개일 경우, 25배인 상당히
느린 속도인, 답변까지, 2.5sec + å 가 소요될 것으로 예측된다.

그렇다면 스로틀링 현상은 해결되었으니, Thread를 활용하여 소요시간을 단축해보자.
만약, 시스템 즉, 하드웨어상으로 감당되어지지 않는다면, 서버상의 커넥션또한 고려해봐야 할듯.

그렇다면, Thread를 어떤방식으로 적용해야할까?
1. json 데이터 4개 검사를 동시에 실행해야함. 
그렇다면 for문으로 돌리는 방식으로 활용한다면 일반적으로 차례차례 실행됨
생각해보니깐, 질문은 한개, 대조 표본은 정해뎌 있기 때문에, 일방적인 숫자로
밀어붙이면 되지 않을까? 

내 가설이 적중했어. 낮은 사양으로는 이 프로그램이 효율적으로 작동할거 같지 않아

일단 git에 push 한번하고 진행해보자.

과연 thread를 사용하는 것과 그냥 실행하는 것의 차이가 있을까?
Thread를 사용함에 있어서 드는 하드웨어적 사양으로는 엄청난 사양이
요구되어짐. 일단 4개를 사용하는데 효율성을 검사해보자.

끝남과 동시에 프로그램이 종료되어지기 때문에, 
thread 4
평균 답변 속도: 0.2220454216003418
thread 5
평균 답변 속도: 0.2736165523529053
thread 6
(1) 평균 답변 속도: 0.5852203369140625
(2) 평균 답변 속도: 0.32442212104797363
(3) 평균 답변 속도: 0.28812432289123535
thread 7
평균 답변 속도: 0.564633846282959
.
.
.
thread 15
평균 답변 속도: 1.3635966777801514
.
.
.
thread 30
여기서부터는 로컬 맥북에서 테스트 -> 서버가 다운될 가능성이 존재함

서버의 작동 속도가 무지나게 느린 문제점이 있기 때문에, while로 돌리고 thread
를 돌리는 동안 서버로 요청이 들어왔을때, 이를 받을 수 있는 알고리즘이 필요해
요청이 들어오면 log 파일을 작성하는 방향으로 그렇게 되면 단순하게 해결할 수 
있을듯. 파일의 값이 none이 아니라면, 이 텍스트를 읽어서 분석하는 형식으로 
이거는 내일하자 오늘은 소개서 쓰고.

오늘 다시 시작해보자.

일단 서버에서 chrome/safari 형태로 접속하였을때,
이에 대한 header를 검사하고, 이에 대한 유효성 검
사후, 접근을 허용 등을 해주는 과정이 필요함.

token 방식을 활용하여 해결함.
'''