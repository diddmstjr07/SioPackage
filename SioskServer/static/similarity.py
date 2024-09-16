from sentence_transformers import SentenceTransformer, util
import time
import os
import shutil
import json
import threading
from concurrent.futures import ThreadPoolExecutor

class CompareSimilaity:
    def __init__(self, ques) -> str:
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)
        cache_folder = './database'
        model_name = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'
        model_cache_path = os.path.join(cache_folder, model_name.replace('/', '_'))
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        if os.path.exists(model_cache_path):
            shutil.rmtree(model_cache_path)
        self.model = SentenceTransformer(model_name, cache_folder=cache_folder)
        self.ques = ques
        self.sentences = []
        self.datas = []
        self.comparison = []
        self.comparison_float = []
        self.comparison_data = []
    
    def getdata(self):
        with open('./conversation.json', 'r') as r:
            data = json.load(r)
            data_keys = list(data.keys())
            data_values = list(data.values())
            # print(data_keys)
            # print(data_values)
            self.data_keys = data_keys
            self.data_values = data_values
    
    def compare(self, data_key):
        self.sentences = []
        print(f"testing data: {self.data_keys[data_key]}")
        print(f"testing target: {self.ques}")
        self.sentences.extend([self.data_keys[data_key], str(self.ques)])
        start_time = time.time()
        embeddings = self.model.encode(self.sentences, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        print(f"Similarity: {similarity.item()}")
        self.comparison_float.append(float(similarity.item()))
        self.comparison_data.append(self.data_keys[data_key])
        end_time = time.time()
        embedded_time = end_time - start_time
        print("Embedding time: %0.2f seconds" % embedded_time)
        self.datas.append("%0.2f" % embedded_time)
        number = 0
        for data in range(len(self.datas)):
            number += float(self.datas[data])
        aver_embedded = number / len(self.datas)
        print("Embedding average time: %0.2f" % aver_embedded)
    
    def delay_blocker(self):
        blocker = []
        blocker.extend(["안녕", "안녕하세요"])
        start_time = time.time()
        embeddings = self.model.encode(blocker, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        end_time = time.time()
        embedded_time = end_time - start_time
        print(f"Test similarity: {similarity.item()}")
        print("Embedding test data time: %0.2f seconds" % embedded_time)
    
    def thread(self):
        with ThreadPoolExecutor(max_workers=10000000) as executor:
            executor.map(self.compare, range(len(self.data_keys)))

    # def __display__(self):
    #     self.comparison.append(self.comparison_float)
    #     self.comparison.append(self.comparison_data)
    #     max_index = max(enumerate(self.comparison[0]), key=lambda x: x[1])[0]
    #     predict_key = self.comparison[1][max_index]
    #     for key in range(len(self.data_keys)):
    #         if self.data_keys[key] == predict_key:
    #             predict_value = self.data_values[key]
    #             return predict_key, predict_value, self.ques

    def testcode():
        datas = []
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)
        cache_folder = './database'
        model_name = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'
        model_cache_path = os.path.join(cache_folder, model_name.replace('/', '_'))
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        if os.path.exists(model_cache_path):
            shutil.rmtree(model_cache_path)
        model = SentenceTransformer(model_name, cache_folder=cache_folder)
        while True:
            try:
                sentences = []
                print("Please write comparison targets (Press Enter without any input to exit)")
                input_1 = input()
                if not input_1.strip():
                    print("Exiting...")
                    break
                input_2 = input()
                if not input_2.strip():
                    print("Exiting...")
                    break
                sentences.extend([input_1, input_2])
                start_time = time.time()
                embeddings = model.encode(sentences, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
                print(f"Similarity: {similarity.item()}")
                end_time = time.time()
                embedded_time = end_time - start_time
                print("Embedding time: %0.2f seconds" % embedded_time)
                datas.append("%0.2f" % embedded_time)
                number = 0
                for data in range(len(datas)):
                    number += float(datas[data])
                aver_embedded = number / len(datas)
                print("Embedding average time: %0.2f" % aver_embedded)
            except KeyboardInterrupt:
                print("Keyboard interrupt detected, exiting...")
                break

if __name__ == "__main__":
    speed_datas = []
    compare = CompareSimilaity(ques="어떤 메뉴가 있어?") # 메뉴가 뭐가 있을까요?, 아메리카노 한 잔과 블루베리 치즈케이크 먹고 싶어요, 포장할게요
    compare.delay_blocker() 
    for _ in range(100):
        speed = 0
        print("--------------------------------------------------------------")
        # pointment = input("Enter to start")
        start_time = time.time()
        compare.getdata()
        compare.thread()
        # predict_key, predict_value, ques = compare.__display__()
        # print(f"\n고유 질문: {ques}")
        # print(f"예측 분석 질문: {predict_key}")
        # print(f"예측 분석 답변: {predict_value}")
        end_time = time.time()
        print(f"최종 소요 시간: {end_time - start_time}")
        speed_datas.append(end_time - start_time)
        for speed_data in range(len(speed_datas)):
            speed += speed_datas[speed_data]
        print("\033[32m" + "평균 답변 속도: " + str(speed / len(speed_datas)) + "\033[0m")
        # pointment = input("Enter to restart")


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
'''