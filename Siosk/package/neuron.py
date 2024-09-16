from .converter import SpeechToTextConverter
from auto.clear_terminal import clear_terminal
import os

class NeuronAggregate:
    def __init__(self) -> None:
        import google_speech 
        import speech_recognition
        import os
        import time
        self.converter = SpeechToTextConverter() # 모델 로드, Google_Speech, SpeechRecognition converter 변수에 저장
        self.detection = speech_recognition
        self.TTS = google_speech
        self.time = time
        self.os = os
    
    def Neuron(self):
        pass

    def Detection(self):
        micro_result = self.converter.check_microphone() # 반환한 마이크 배열 데이터를 변수에 저장
        # for i in range(len(micro_result)):
        #     if "Mic" or "mic" or "마이크" in micro_result[i]:
        #         os.system(clear_terminal())
        #         print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Mic Infor: {micro_result[i]}")
        #         return int(str(micro_result[i])[1])
        print("\n-----------------------------------")
        for i in range(len(micro_result)): 
            print(micro_result[i]) # 마이크 정보 출력
        print("-----------------------------------\n")
        while True:
            try:
                index = int(input("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Please Select Microphone and Type number of index: "))
                self.os.system(clear_terminal())
                return index # 선택한 인덱스 반환
            except ValueError:
                print("\033[31m" + "ERROR" + "\033[0m" + ": " "     Please type only integer texture")


    def Trans(self, index):
        text_result = self.converter.Detecting(index) # 인식된 text를 다시 변환
        print("text_result: " + str(text_result)) # String으로 변환하여 결과 출력
        return text_result # 바로 인식된 경우, 바로 반환
