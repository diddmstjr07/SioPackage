from sentence_transformers import SentenceTransformer, util
import sys
import os
from auto.clear_terminal import clear_terminal
from ..router.flow import FlowFlagStore
import json
import time
from tqdm import tqdm
import random
import threading
import itertools
import router.download as download

class LoadingIndicator:
    def __init__(self, message="\033[1;32mINFO\033[0m:     Dataset Loading Starting"):
        self.done = False
        self.message = message
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.thread = threading.Thread(target=self.animate)
        save_dir = os.getcwd() # Conversation.json이 있는지 확인하고 없으면 서버에서 다운로드
        download.download_file(file="conversation.json", save_dir=save_dir) # Conversation.json이 있는지 확인하고 없으면 서버에서 다운로드

    def animate(self):
        while not self.done:
            sys.stdout.write(f'\r{self.message} {next(self.spinner)}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r{self.message} Done!\n')
        sys.stdout.flush()

    def start(self):
        self.thread.start()

    def stop(self):
        self.done = True
        self.thread.join()

class SentenceCompare:
    def __init__(self) -> None:
        loading = LoadingIndicator()
        loading.start()
        self.cache_folder = './database'
        model_name = 'snunlp/KR-SBERT-V40K-klueNLI-augSTS'
        self.sentences = []
        self.sentences_A = []
        self.flag = FlowFlagStore()
        self.model = SentenceTransformer(model_name, cache_folder=self.cache_folder)
        with open('conversation.json', 'r', encoding='utf-8') as file:
            unfiltered_sentences = json.load(file)
            for unfiltered_sentences_index, unfiltered_sentences_val in enumerate(unfiltered_sentences):
                self.sentences.append(str(unfiltered_sentences_val).split(' | ')[0])
                self.sentences_A.append(str(unfiltered_sentences_val).split(' | ')[1])
        self.sentences_embeddings = self.model.encode(self.sentences, convert_to_tensor=True)
        loading.stop()
        print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Dataset Loading Finished..\n")

    def setting_progress_bar(self):
        total_steps = 100
        progress_bar = tqdm(total=total_steps)
        return progress_bar, total_steps

    def update_progress_bar(self, total_steps, progress_bar, percentage):
        steps_to_add = (total_steps * percentage) / 100
        progress_bar.update(steps_to_add)

    def quality_check(self):
        while True:
            Airing_start = time.time()
            compare_embedded_time = [] # time average calculation array
            random_data  = [] # quality test data array
            with open('airing_data.json', 'r', encoding='utf-8') as file:
                quality_check_data = json.load(file)
                for _ in range(5):
                    random_data.append(quality_check_data[random.randint(0, 149)])
            returning = self.quality_check_detail(random_data, compare_embedded_time)
            if returning == True:
                Airing_end = time.time()
                print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Total Airing time: {str(Airing_end - Airing_start)} seconds\n")
                return True
            elif returning == False:
                pass

    def quality_check_detail(self, random_data, compare_embedded_time):
        for qualityindex, qualityvalue in enumerate(random_data):
            compare_embedding_st = time.time()
            single_embedding = self.model.encode(qualityvalue, convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings)
            compare_embedding_en = time.time()
            compare_embedded_time.append(compare_embedding_en - compare_embedding_st)
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Airing target '{qualityvalue}'")

        if sum(compare_embedded_time) / len(compare_embedded_time) < 0.3:
            print("\033[1;32m" + "\nAiring Succeed" + "\033[0m" + ":" + f"     Airing targeted time {str(sum(compare_embedded_time) / len(compare_embedded_time))[0:4]} satisfied")
            return True
        elif sum(compare_embedded_time) / len(compare_embedded_time) > 0.3:
            print("\033[1;31m" + "\nAiring Failed" + "\033[0m" + ":" + f"     Airing targeted time {str(sum(compare_embedded_time) / len(compare_embedded_time))[0:4]} unsatisfying Reloading...\n")
            time.sleep(5)
            return False
    
    def quality_check_main(self):
        while True:
            Airing_start = time.time()
            compare_embedded_time = [] # time average calculation array
            with open('conversation.json', 'r', encoding='utf-8') as file:
                quality_check_data = json.load(file)
            returning = self.quality_check_detail_main(quality_check_data, compare_embedded_time)
            if returning == True:
                Airing_end = time.time()
                print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Total Airing time: {str(Airing_end - Airing_start)} seconds\n")
                return True
            elif returning == False:
                pass

    def quality_check_detail_main(self, main_data, compare_embedded_time):
        for qualityindex, qualityvalue in enumerate(main_data):
            compare_embedding_st = time.time()
            # import pdb
            # pdb.set_trace()
            single_embedding = self.model.encode(str(qualityvalue).split(' | ')[0], convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings)
            compare_embedding_en = time.time()
            compare_embedded_time.append(compare_embedding_en - compare_embedding_st)
            print("\033[1;32m" + "INFO" + "\033[0m" + ":" + f"     Main Airing target '{str(qualityvalue).split(' | ')[0]}'")

        if sum(compare_embedded_time) / len(compare_embedded_time) < 0.3:
            print("\033[1;32m" + "\nAiring Succeed" + "\033[0m" + ":" + f"     Main Airing targeted time {str(sum(compare_embedded_time) / len(compare_embedded_time))[0:4]} satisfied")
            return True
        elif sum(compare_embedded_time) / len(compare_embedded_time) > 0.3:
            print("\033[1;31m" + "\nAiring Failed" + "\033[0m" + ":" + f"     Main Airing targeted time {str(sum(compare_embedded_time) / len(compare_embedded_time))[0:4]} unsatisfying Reloading...")
            time.sleep(5)
            return False
        
        
    def compare(self, similarities_list):
        max_val = max(similarities_list)
        index_max_val = list(similarities_list).index(max_val)
        min_val = similarities_list[index_max_val]
        print("\033[33m" + "\nLOG" + "\033[0m" + ":" + f"     Predicted Script data '{self.sentences[index_max_val]}'")
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Predicted Script answer '{self.sentences_A[index_max_val]}'")
        # print(similarities_list)
        return self.sentences[index_max_val], self.sentences_A[index_max_val], min_val

    def process(self, ques):
        single_sentence = ques
        start = time.time()
        single_embedding = self.model.encode(single_sentence, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings)
        similarities_list = similarities.squeeze().tolist()
        # import pdb
        # pdb.set_trace()
        predicted_Q, predicted_A, min_val  = self.compare(similarities_list)
        modified_A = self.flag.flag_handler(predicted_Q, predicted_A)
        if modified_A == 0:
            pass
        elif modified_A == -1:
            pass
        else:
            predicted_A = modified_A
        end = time.time()
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Embedded Time: {str(end - start)}\n")
        return min_val
    
    def Airing(self):
        self.quality_check() # Random Data Airing
        self.quality_check_main() # Real Data Airing
        os.system(clear_terminal())
            
    def run(self, ques):
        min_val = self.process(ques)
        return min_val
