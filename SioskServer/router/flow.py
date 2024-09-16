import json
import random
from SioskServer.router.download import download_file

"""
지금든 생각인데, flag 별로 말할수 있는 비교군을 만들어서 데이터를 aianalyze.py에 넣어둘까? 
그리고 aianlyze.py의 flow 호출이 끝나면 flag 데이터를 공유해서 어디까지 주문현황이 진행되었는지,
그리고 이를 활용하여 할수 있는 대답을 한정하고 만약 유사도가 예상지점보다 하락하는 지점이 존재한다면,
Gemini 혹은 ChatGPT API와 연결하기.
그리고 중요한 부분은 Customer가 그냥 키오스크가 편해서 키오스크로 진행할수도 있는데, 이때를 고려해서
키오스크에서도 특정 넘김 혹은 버튼을 누르는 것이 완료되는 파트를 트래킹하여, 완료될시 flag 배열에 자동
append하도록

Example -> 
Flag 5일때는 6의 대사와만 비교 
Flag 1일때는 2와의 대사와만 비교
.
.
.

취소 기능도 넣어야겠네 
로직:
배열 구조를 
[] -> 음료 종류 (그냥 3번 Flag에서 추출해버리자)
[] -> 음료 잔 (이거는 4번 Flag에서 추출)
[] -> 음료 온도 (이거는 5번 Flag에서 추출)

0 ~ 3번 Flag까지는 일반적으로 진행 
Flag 3: 음료종류를 추출해서 음료 종류 배열에 저장 
Flag 4: 음료 잔개수를 추출해서 음료 잔 배열 index 1번에 저장
Flag 5: 음료 온도를 추출해서 음료 온도 배열 index 1번에 저장
Flag 6: 지금까지 주문하거나 설정한 음료를 취소할지/장바구니에 담을지 결정

각각 함수 만들기
탈출 조건 (탈출하는 이유):
추출한 flag 값이
7 소환 -> 6 없을때
6 소환 -> 5가 없을때
5 소환 -> 4가 없을떄
4 소환 -> 3이 없을때

음성 API TTS 수정 필요해 보임
다시 말해줘라고 할때 로직도 구현해보자
"""

class FlowFlagStore: 
    def __init__(self) -> None:
        self.flag_store = []
        self.beverage_kind = []
        self.beverage_amount = []
        self.beverage_temperature = []

    def flag_handler(self, original_predicted_sentence, predicted_answer_sentence) -> str:
        download_file(file="conversation.json", save_dir='./')
        with open('conversation.json', 'r', encoding='utf-8') as file:
            unfiltered_sentences = json.load(file)
        for unfiltered_index, unfiltered_val in enumerate(unfiltered_sentences):
            if original_predicted_sentence in unfiltered_val:
                flag = str(unfiltered_val).split(" | ")[2]
                result = self.flag_detecter(int(flag))
                result_sentence = self.A_modifier(result, original_predicted_sentence, predicted_answer_sentence)
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Flag Stored current data: {str(self.flag_store)}")
                print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Flag Connection Sentences curret data: {str(self.beverage_kind + self.beverage_amount + self.beverage_temperature)}")
                return result_sentence

    def flag_detecter(self, flag) -> int: # Return Data -> int(1, 0, -1) 
        """
        return 값이 conversation 값과 달라지는 경우, 여기서 처리해서 내보내는 것임
        """
        if flag == 7: # 돌아온 Flag가 6인 경우
            try:
                self.flag_store.index(flag - 1) # flag -1 즉, 5가 있는지 확인
                self.flag_store.append(flag) # 있으면 flag를 append
                return 7 # 정상적으로 완료되었다는 1 flag 반환
            except ValueError: # 아닌경우
                return -1 # 에러 flag -1 return
        elif flag == 6:
            try:
                self.flag_store.index(flag - 1) # flag -1 즉, 5가 있는지 확인
                self.flag_store.append(flag) # 있으면 flag를 append
                return 6 # 정상적으로 완료되었다는 1 flag 반환
            except ValueError: # 아닌경우
                return -1 # 에러 flag -1 return
        elif flag == 5:
            try:
                self.flag_store.index(flag - 1) # flag -1 즉, 5가 있는지 확인
                self.flag_store.append(flag) # 있으면 flag를 append
                return 5 # 정상적으로 완료되었다는 1 flag 반환
            except ValueError: # 아닌경우
                return -1 # 에러 flag -1 return
        elif flag == 4:
            try:
                self.flag_store.index(flag - 1) # flag -1 즉, 5가 있는지 확인
                self.flag_store.append(flag) # 있으면 flag를 append
                return 4 # 정상적으로 완료되었다는 1 flag 반환
            except ValueError: # 아닌경우
                return -1 # 에러 flag -1 return
        elif flag == 3: # 3은 치외법권
            self.flag_store.append(flag) # 있으면 flag를 append
            return 3 # 정상적으로 완료되었다는 1 flag 반환
        else:
            try:
                self.flag_store.index(flag - 1) # 위와 같이 전 flag가 있는지 확인 
                self.flag_store.append(flag) # 있다면 평범하게 append
                return 0
            except ValueError:
                if flag in (0, 1, 2, 3): # 0 ~ 3번 과정은 통상적으로 건너뛰어도 무방하기 때문에 건너뛰기
                    self.flag_store.append(flag) # 그냥 append
                    return 0
                else:
                    return -1
                
    def A_modifier(self, result: int, original_predicted_sentence: str, predicted_answer_sentence: str) -> None:
        """
        return이 0이나 -1이 아닌 str인 경우, 그걸 그대로 client로 반환해줌
        """
        if result == -1: # -1이 돌아왔으면 그대로 다시 return해준다. 
            return -1 # 이것들은 서버로 return
        elif result == 0:
            return 0
        elif result == 3: 
            beverage_result = self.beverage_kind_flag_3(original_predicted_sentence) 
            if type(beverage_result) == int:
                return 0
            elif type(beverage_result) == str:
                return beverage_result
        elif result == 4: 
            self.beverage_amount_flag_4(original_predicted_sentence) 
            return 0
        elif result == 5: 
            beverage_temperature_str = self.beverage_temperature_flag_5(original_predicted_sentence, predicted_answer_sentence) 
            return beverage_temperature_str
        elif result == 6:
            self.beverage_cancel_flag_6(predicted_answer_sentence)
            return 0
        elif result == 7: # 정상적으로 값처리가 완료되었으면 flag가 6인 경우에만 result가 int형으로 반환되어짐
            self.flag_store.clear()
            return predicted_answer_sentence # 이것들은 서버로 return
        
    def beverage_kind_flag_3(self, original_predicted_sentence: str) -> None: # This function can be entered only flag val is '6'
        data = [
            "아메리카노",
            "연유라테",
            "카푸치노",
            "헤이즐넛라테",
            "헤이즐넛아메리카노",
            "콜드브루라테",
            "콜드브루",
            "카라멜마키아또",
            "카페모카",
            "민트프라페",
            "녹차프라페",
            "유니콘프라페",
            "바나나퐁크러쉬",
            "초콜릿허니퐁크러쉬",
            "슈크림허니퐁크러쉬",
            "플래인퐁크러쉬",
            "딸기퐁크러쉬",
            "딸기쿠키프라페",
            "망고요거트스무디",
            "플래인요거트스무디",
            "딸기요거트스무디",
            "블루레몬에이드",
            "체리콕",
            "자몽에이드",
            "레몬에이드",
            "라임모히또",
            "메가에이드",
            "레몬차",
            "사과유자차",
            "케모마일차",
            "녹차",
            "얼그레이",
            "자몽차"
        ]
        if original_predicted_sentence == "추천해줘":
            selection = data[random.randint(0, len(data) - 1)]
            beverage_kind_str = selection
            self.beverage_kind.append(beverage_kind_str)
            return f"네 {beverage_kind_str} 몇잔드릴까요?"
        else:
            beverage_kind_str = original_predicted_sentence.split(' 줄래?')[0]
            self.beverage_kind.append(beverage_kind_str)
            return 3

    def beverage_amount_flag_4(self, original_predicted_sentence: str) -> None: # This function can be entered only flag val is '6'
        beverage_amount_str = original_predicted_sentence.split(' 줘')[0]
        if str(beverage_amount_str[-1]) != "잔":
            result = str(beverage_amount_str).replace(beverage_amount_str[-1], "잔")
            self.beverage_amount.append(result)
        else:
            self.beverage_amount.append(beverage_amount_str)
    
    def beverage_temperature_flag_5(self, original_predicted_sentence: str, predicted_answer_sentence: str) -> None: # This function can be entered only flag val is '6'
        beverage_temperature_str = original_predicted_sentence.split(' 줘')[0]
        if beverage_temperature_str == "차갑게":
            beverage_temperature_str = beverage_temperature_str.replace("갑게", "가운")
        elif beverage_temperature_str == "따뜻하게":
            beverage_temperature_str = beverage_temperature_str.replace("하게", "한")
        self.beverage_temperature.append(beverage_temperature_str)
        return predicted_answer_sentence.split(" 넣어드릴까요?")[0] + " " + self.beverage_temperature[-1] + " " + self.beverage_kind[-1] + " " + self.beverage_amount[-1] + " 넣어드릴까요?"
    
    def beverage_cancel_flag_6(self, predicted_answer_sentence: str) -> None: # This function can be entered only flag val is '6'
        if predicted_answer_sentence == "네 장바구니에 넣어드렸습니다. 이대로 주문하실건가요? 아니면 메뉴를 추가하시겠습니까?":
            pass
        elif predicted_answer_sentence == "네 해당 주문이 취소되었습니다. 이대로 주문하실건가요? 아니면 메뉴를 추가하시겠습니까?":
            self.beverage_kind.pop()
            self.beverage_amount.pop()
            self.beverage_temperature.pop()
    
    def beverage_order_final_flag_7(self, predicted_answer_sentence) -> None: # This function can be entered only flag val is '6'
        return_result_sentence = ""
        for final_index, final_val in enumerate(self.beverage_kind):
            menu = str(self.beverage_temperature[final_index]) + " " + str(final_val) + " " + str(self.beverage_amount[final_index]) + ", "
            return_result_sentence += menu
        orginal_final_ans = str(predicted_answer_sentence).split('결제가 완료되었습니다.')
        print(orginal_final_ans)
        print(return_result_sentence)
        return_sentence = orginal_final_ans[0] + return_result_sentence + "결제가 완료되었습니다" + orginal_final_ans[1]
        return return_sentence
    
    def flag_store_share_func(self):
        return self.flag_store