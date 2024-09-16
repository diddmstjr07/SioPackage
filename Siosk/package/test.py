import pyaudio
import wave

def record_audio(output_file: str, duration: int, rate: int = 44100, chunk: int = 1024):
    # PyAudio 객체 생성
    audio = pyaudio.PyAudio()

    # 오디오 스트림 열기
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("녹음을 시작합니다...")

    frames = []

    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("녹음이 완료되었습니다.")

    # 스트림 종료 및 PyAudio 객체 해제
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAV 파일로 저장
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"오디오 파일이 저장되었습니다: {output_file}")

# 사용 예시
record_audio('recorded.wav', duration=10)  # 10초 동안 녹음
