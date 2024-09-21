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

    def record_audio(self):
        audio = pyaudio.PyAudio()
        print(self.mic)
        
        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,  # Set this to 1 for mono or 2 for stereo
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=int(self.mic)  # Use mic as input device index
            )
        except Exception as e:
            print(f"오류 발생: {e}")
            return
        
        print("녹음을 시작합니다...")
        self.recording = True
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
            if self.stop_event.is_set():
                break
        print("녹음이 완료되었습니다.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(1)  # Save as mono
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        print(f"오디오 파일이 저장되었습니다: {self.output_file}")
        self.converter()

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
