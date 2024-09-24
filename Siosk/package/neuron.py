from auto.clear_terminal import clear_terminal
from Siosk.package.audio import AudioRecorder
import os

class NeuronAggregate:
    def __init__(self, record: AudioRecorder) -> None:
        import google_speech 
        import speech_recognition
        import os
        import time
        self.detection = speech_recognition
        self.TTS = google_speech
        self.time = time
        self.os = os
        self.record = record
    
    def Neuron(self):
        pass

    def Detection(self):
        micro_result = self.record.check_microphone() # 반환한 마이크 배열 데이터를 변수에 저장
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

    def Trans(self):
        text, embedding_time = self.record.record_audio()
        return text, embedding_time
