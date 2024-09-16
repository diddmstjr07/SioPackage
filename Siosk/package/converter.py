import time
import os
import sounddevice as sd
import wave

class SpeechToTextConverter:
    def __init__(self):
        import speech_recognition
        self.detection = speech_recognition
        self.detector = self.detection.Recognizer()
        self.recognizer = self.detection.Recognizer()
        self.error_non = speech_recognition.exceptions.UnknownValueError
        self.error_wait = speech_recognition.exceptions.WaitTimeoutError

    def check_microphone(self):
        detected = []
        for index, name in enumerate(self.detection.Microphone.list_microphone_names()):
            detected.append(str(f"[{index}] {name}")) # 존재하는 마이크 append
        return detected

    def record_audio(output_file: str, duration: int, rate: int = 44100):
        print("녹음을 시작합니다...")
        audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
        sd.wait()  # 녹음이 끝날 때까지 대기
        print("녹음을 종료합니다...")
        
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(audio_data.tobytes())
        
        print(f"오디오 파일이 저장되었습니다: {output_file}")
    
    def Detecting(self, index): # 음성인식하는 로직을 바꾸자 recognition으로 실시간으로 바꾸는게 아니라 Enter를 누르기 전까지 계속 녹음을 하고 이거를 text로 변환해서 넘겨주자
        try:
            mic = self.detection.Microphone(device_index=index)
            with mic as source:
                self.detector.dynamic_energy_threshold = True
                print("\033[33m" + "\nLOG" + "\033[0m" + ":" + f"     None Voice Detected")
                while True:  # 무한 루프로 음성 감지 시도
                    try:
                        stra = time.time()
                        audio = self.detector.listen(source, timeout=1.5, phrase_time_limit=3)  # 1.5초 동안만 듣기 시도
                        result = self.detector.recognize_google(audio, language="ko-KR") # google_google: ko-KR, whisper: ko
                        print("Embbedd time: " + str(time.time() - stra))
                        return result
                    except self.error_non:
                        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     None Voice Detected")
                    except self.error_wait:
                        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     None Voice Detected")
        except Exception as e:
            print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"     Please Check your selection if mic is speaker (마이크가 아닌 스피커를 선택하였는지 확인해주십시오)")
            os._exit(0)
