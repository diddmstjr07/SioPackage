from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from SioskServer.router.aianalyze import SentenceCompare
from SioskServer.router.connection import thread_read_token
from SioskServer.router.kill import KillProcess
import os
import warnings
import uvicorn

app = FastAPI()
run = SentenceCompare() # This must not exceed the json data amounts also json data must divided by amount of thread
warnings.simplefilter("ignore")
run.Airing()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

API_KEY_NAME = "token" 

def get_api_key(request: Request):
    api_key = request.query_params.get(API_KEY_NAME)
    boolen = thread_read_token(api_key)
    if boolen == True:
        pass
    elif boolen == False:
        raise HTTPException(status_code=403, detail="error")
    else:
        raise HTTPException(status_code=403, detail="error")

@app.get("/api")
async def read_root(api_key: str = Depends(get_api_key), ques: str = None):
    predicted_Q, predicted_A, embedded_time, flag = run.run(ques)
    if predicted_A == False:
        os._exit(0)
    return {"message": predicted_Q + " | " + predicted_A + " | " + flag}

@app.get("/access")
async def read_root(api_key: str = Depends(get_api_key), host: str = None, ip: str = None):
    print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Client Connected from {host} -> {ip}")
    return {"message": True}
                # ssl_keyfile="./ssl/privkey.pem", ssl_certfile="./ssl/cert.pem", reload=True)

def process():
    killer = KillProcess()
    killer.killing()
    uvicorn.run("SioskServer.server:app", host="0.0.0.0", port=9460)

'''
서버 시작할때, model을 로딩을 시키는 방식으로 진행을 하고
로딩이 완료가 되면, 서버가동 시작, while문으로 thread로 동시에
항상 실행중으로 백그라운드에서 실행시키기 --> 최종적으로 get 요청을
하면 모델을 호출을 함.

일단 그러면 Conversation 진행 상황도 중요하기 때문에, 무조건 저장하는 배열을 하나 만들어서 하는 것이 중요할 듯. 
지금 해결해야하는 문제점이, Thread 개수를 늘렸을때 정확한 답변이 오지 않는다는, 문제점.
해결해보자.

parallels@ubuntu-linux-22-04-desktop:~/Documents/SioskServer$ python3 server.py 
100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 100.0/100 [00:04<00:00, 22.03it/s]
INFO:     Loading fully Completed
INFO:     Kill Process Non-Detected... Finishing
INFO:     Loading fully Completed
INFO:     Started server process [567374]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9460 (Press CTRL+C to quit)
<starlette.requests.Request object at 0xffff80687d90>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.81 seconds
[0.16041113436222076, 0.17155049741268158]
You must modify your dataset.
[0.4864809811115265, 0.17783032357692719]
You must modify your dataset.
[0.11344011127948761, 0.18588486313819885]
You must modify your dataset.
[0.10762368142604828, 0.2535063624382019]
You must modify your dataset.
[0.22426588833332062, 0.0989202931523323]
You must modify your dataset.
안녕하세요
안녕하세요 주문하고 싶은 메뉴를 말씀해주세요. 대표적인 매뉴로는 아이스 아메리카노가 있어요
INFO:     10.211.55.2:57405 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff60806350>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.2697504758834839, 0.3803211450576782]
You must modify your dataset.
[0.6761206388473511, 0.39921361207962036]
You must modify your dataset.
[0.4551981985569, 0.3004797697067261]
You must modify your dataset.
[0.396921843290329, 0.34215328097343445]
You must modify your dataset.
[0.3679715692996979, 0.626569390296936]
You must modify your dataset.
딸기라뗴 있어?
네 몇잔드릴까요?
INFO:     10.211.55.2:57406 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%EB%94%B8%EA%B8%B0%EB%9D%BC%EB%97%B4%20%EC%9E%88%EC%96%B4? HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80686560>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.34704479575157166, 0.5218924283981323]
You must modify your dataset.
[0.5377182364463806, 0.3636137843132019]
You must modify your dataset.
[0.49253854155540466, 0.447639524936676]
You must modify your dataset.
[0.41819503903388977, 0.5674905180931091]
You must modify your dataset.
[0.4124649465084076, 0.4538121819496155]
You must modify your dataset.
3잔줘
네 한잔이 장바구니에 넣어드렸습니다.
INFO:     10.211.55.2:57407 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=3%EC%9E%94%EC%A4%98 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80687c10>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.2822532057762146, 0.4737396240234375]
You must modify your dataset.
[0.4828800559043884, 0.45119860768318176]
You must modify your dataset.
[0.5610468983650208, 0.6842849254608154]
You must modify your dataset.
[0.45847275853157043, 0.4311014413833618]
You must modify your dataset.
[0.4136146008968353, 0.5365533828735352]
You must modify your dataset.
퐁크러쉬 음료 있어?
네 몇잔드릴까요?
INFO:     10.211.55.2:57409 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%ED%90%81%ED%81%AC%EB%9F%AC%EC%89%AC%20%EC%9D%8C%EB%A3%8C%20%EC%9E%88%EC%96%B4? HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80687910>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.3131219744682312, 0.5411906838417053]
You must modify your dataset.
[0.3938419818878174, 0.603492021560669]
You must modify your dataset.
[0.5509818196296692, 0.3466731607913971]
You must modify your dataset.
[0.5027910470962524, 0.46500319242477417]
You must modify your dataset.
[0.3805910348892212, 0.43622589111328125]
You must modify your dataset.
5잔 줘
네 한잔이 장바구니에 넣어드렸습니다.
INFO:     10.211.55.2:57411 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=5%EC%9E%94%20%EC%A4%98 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80687f10>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.297312468290329, 0.22364112734794617]
You must modify your dataset.
[0.3484693467617035, 0.09622388333082199]
You must modify your dataset.
[0.17180925607681274, 0.17134660482406616]
You must modify your dataset.
[0.36598140001296997, 0.3280765116214752]
You must modify your dataset.
[0.22836148738861084, 0.36795884370803833]
You must modify your dataset.
다섯 달라고
네 몇잔드릴까요?
INFO:     10.211.55.2:57413 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%EB%8B%A4%EC%84%AF%20%EB%8B%AC%EB%9D%BC%EA%B3%A0 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80686680>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.05 seconds
[0.2804322838783264, 0.41153424978256226]
You must modify your dataset.
[0.31143856048583984, 0.4662841558456421]
You must modify your dataset.
[0.40129366517066956, 0.366080105304718]
You must modify your dataset.
[0.43532633781433105, 0.23923557996749878]
You must modify your dataset.
[0.27117374539375305, 0.41171616315841675]
You must modify your dataset.
다섯잔
네 한잔이 장바구니에 넣어드렸습니다.
INFO:     10.211.55.2:57414 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%EB%8B%A4%EC%84%AF%EC%9E%94 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80687a00>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.05 seconds
[0.2640860676765442, 0.5119428634643555]
You must modify your dataset.
[0.4065418839454651, 0.515504777431488]
You must modify your dataset.
[0.4810155928134918, 0.42817917466163635]
You must modify your dataset.
[0.4784608483314514, 0.33986896276474]
You must modify your dataset.
[0.38918912410736084, 0.4871539771556854]
You must modify your dataset.
다섯잔 달라고
네 한잔이 장바구니에 넣어드렸습니다.
INFO:     10.211.55.2:57415 - "GET /api?token=SioskKioskFixedTokenVerifyingTokenData&ques=%EB%8B%A4%EC%84%AF%EC%9E%94%20%EB%8B%AC%EB%9D%BC%EA%B3%A0 HTTP/1.1" 200 OK
<starlette.requests.Request object at 0xffff80687910>
SioskKioskFixedTokenVerifyingTokenData
Test similarity: 0.4864809811115265
Embedding test data time: 0.06 seconds
[0.24155840277671814, 0.7235641479492188]
[0.395079106092453, 0.8813157081604004]
[0.797187328338623, 0.714993953704834]
[0.39363232254981995, 0.39677199721336365]
You must modify your dataset.
[0.5153492093086243, 0.3394955098628998]
You must modify your dataset.
아이스 아메리카노 다섯잔 줘
네 한잔이 장바구니에 넣어드렸습니다.
'''