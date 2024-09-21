import pyaudio
import wave
import threading
import requests
import os
import time

class AudioRecorder:
    def __init__(
            self, 
            output_file: str = "Siosk/temp/temp.wav", 
            rate: int = 44100, 
            chunk: int = 1024
        ):
        import speech_recognition
        self.output_file = output_file
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.recording = False
        self.stop_event = threading.Event()
        self.detection = speech_recognition
        self.mic = None

    def check_microphone(self):
        detected = []
        for index, name in enumerate(self.detection.Microphone.list_microphone_names()):
            detected.append(str(f"[{index}] {name}")) # 존재하는 마이크 append
        self.detected = detected
        return detected

    def get_mic_selection(self, mic):
        self.mic = mic
    
    def record_audio(self):
        audio = pyaudio.PyAudio()
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Device {self.detected[self.mic]} set as Microphone")
        cnt=0
        for _ in range(2):
            try:
                stream = audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk,
                    input_device_index=int(self.mic)
                )
            except OSError:
                if cnt == 1:
                    print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Automatic trouble shooting Failed :(")
                    os._exit(0)
                print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Please check {self.detected[self.mic]} device is Microphone\n")
                print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Automatic trouble shooting...")
                self.mic = 1
                cnt += 1
            except Exception as e:
                print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Unpredictable error occured")
                os._exit(0)
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"      Starting Recording...")
        if os.path.exists(self.output_file):
            os.remove(self.output_file)  # Remove the previous file if it exists
        
        self.stop_event.clear()  # Reset stop event for the next recording
        self.recording = True
        self.frames = []  # Reset frames for the new recording
        
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
            if self.stop_event.is_set():
                break
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"      Record Completed")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"      Audio file stored at: {self.output_file}\n")
        self.converter()
        self.recording = False  # Reset recording state for the next session

    def stop_recording(self):
        self.recording = False
        self.stop_event.set()
    
    def converter(self): # Version 8.8 New protocol STT -> click - hearing - click - recognition -> 8.9 (scheduled) click - hearing + recognition - click
        st_time = time.time()
        recognizer = self.detection.Recognizer()
        with self.detection.AudioFile(self.output_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)  # Read the entire audio file
        try:
            text = recognizer.recognize_google(audio_data, language="ko-KR")  # Change language if needed
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Recognized Text: ", text)
        except self.detection.UnknownValueError:
            print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Could not understand audio")
        except self.detection.RequestError as e:
            print("\033[1;91m" + "ERROR" + "\033[0m" + ":" + f"    Could not request results from Google Speech Recognition service; {e}")
        nd_time = time.time()
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Processing time: ", nd_time - st_time)