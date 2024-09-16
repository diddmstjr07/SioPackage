from sentence_transformers import SentenceTransformer, util
import time
import os
import shutil
import json
import threading
import numpy as np
import psutil
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

length_json = 0

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
    
    def getdata(self, threadnum):
        with open('./conversation.json', 'r') as r:
            data = json.load(r)
            data_keys = list(data.keys())
            data_values = list(data.values())
            # print(data_keys)
            # print(data_values)
            length = len(data_keys)
            tenth = length // threadnum
            self.data_keys_list = [data_keys[i*tenth:(i+1)*tenth] for i in range(threadnum)]
    
    def compare(self, data_keys):
        for data_key in range(len(data_keys)):
            self.sentences = []
            print(f"testing data: {data_keys[data_key]}")
            print(f"testing target: {self.ques}")
            self.sentences.extend([data_keys[data_key], str(self.ques)])
            start_time = time.time()
            embeddings = self.model.encode(self.sentences, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
            print(f"Similarity: {similarity.item()}")
            self.comparison_float.append(float(similarity.item()))
            self.comparison_data.append(data_keys[data_key])
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
        print(self.data_keys_list)
        threads = [threading.Thread(target=self.compare, args=(data_keys,)) for data_keys in self.data_keys_list]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

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

class RunManage:
    def __init__(self) -> None:
        self.speed_datas = []
        self.speedometer = []
        self.cpu_usage = []
        self.thread_counts = []

    def run(self):
        compare = CompareSimilaity(ques="어떤 메뉴가 있어?") # 메뉴가 뭐가 있을까요?, 아메리카노 한 잔과 블루베리 치즈케이크 먹고 싶어요, 포장할게요
        compare.delay_blocker() 
        count = 1
        for _ in range(length_json):
            for _ in range(10):
                # pointment = input("Enter to start")
                speed = 0
                print("--------------------------------------------------------------")
                start_time = time.time()
                compare.getdata(count)
                compare.thread()
                # predict_key, predict_value, ques = compare.__display__()
                # print(f"\n고유 질문: {ques}")
                # print(f"예측 분석 질문: {predict_key}")
                # print(f"예측 분석 답변: {predict_value}")
                end_time = time.time()
                print(f"최종 소요 시간: {end_time - start_time}")
                self.speed_datas.append(end_time - start_time)
                for speed_data in range(len(self.speed_datas)):
                    speed += self.speed_datas[speed_data]
                print("\033[32m" + "평균 답변 속도: " + str(speed / len(self.speed_datas)) + "\033[0m")
                # pointment = input("Enter to restart")
            count += 1
            self.speedometer.append(str(speed / len(self.speed_datas)))
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.append(cpu_percent)
            self.speed_datas = []
        return self.thread_counts, self.cpu_usage, self.speedometer

    def data_usage(self):
        self.thread_counts = list(range(1, length_json + 1))
        thread_counts, cpu_usage, processing_times = self.run()
        # print(len(thread_counts))
        # print(len(cpu_usage))
        # print(len(processing_times))
        thread_counts = np.array(thread_counts, dtype=float)
        cpu_usage = np.array(cpu_usage, dtype=float)
        processing_times = np.array(processing_times, dtype=float)
        min_index = np.argmin(processing_times)
        processing_times_normalized = processing_times * (cpu_usage.max() / processing_times.max())
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Thread Count')
        ax1.set_ylabel('CPU Usage', color=color)
        ax1.plot(thread_counts, cpu_usage, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Processing Time (normalized)', color=color)
        ax2.plot(thread_counts, processing_times_normalized, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        min_thread_count = thread_counts[min_index]
        min_processing_time = processing_times[min_index]
        ax2.scatter(min_thread_count, processing_times_normalized[min_index], color='blue')  # 점 추가
        ax2.text(min_thread_count, processing_times_normalized[min_index] + 0.2, 
                 f'Threads: {min_thread_count}', 
                 ha='center', color='black')
        ax2.text(min_thread_count, processing_times_normalized[min_index] - 0.4, 
                 f'Time: {min_processing_time:.2f}s', 
                 ha='center', color='blue')
        plt.title('CPU Usage and Processing Time vs. Thread Count')
        plt.savefig('graph_epoch6.png')

def count_amount():
    global length_json
    with open('./conversation.json', 'r') as r:
        data = json.load(r)
        data_keys = list(data.keys())
        length_json += len(data_keys)

if __name__ == "__main__":
    run = RunManage()
    with ProcessPoolExecutor(max_workers=10000) as executor:
        futures = []
        futures.append(executor.submit(count_amount))
        futures.append(executor.submit(run.data_usage))
        for future in futures:
            future.result()