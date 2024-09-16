from sentence_transformers import SentenceTransformer, util
import sys
import os
from auto.clear_terminal import clear_terminal
from .flow import FlowFlagStore
import json
import time
from tqdm import tqdm
import random
import threading
import itertools
import SioskServer.router.download as download
from SioskServer.router.outer_api_gemini import CallingGemini


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
        '''
        flag에 따라서 배열로 conversation.json 파일을 나누고, __init__
        에서 데이터 로드를 진행하여, tensor 값들을 배열에 나열하는 역할을함
        '''
        self.sentences = [] # 배열을 로드
        self.sentences_A = []
        self.flagment = []
        self.sentences_train = [] # 배열을 로드
        self.sentences_A_train = []
        self.flagment_train = []
        self.sentences_4 = []
        self.sentences_A_4 = []
        self.flagment_4 = []
        self.sentences_5 = []
        self.sentences_A_5 = []
        self.flagment_5 = []
        self.sentences_6 = []
        self.sentences_A_6 = []
        self.flagment_6 = []
        self.sentences_7 = []
        self.sentences_A_7 = []
        self.flagment_7 = []
        self.callinggemini = CallingGemini()
        self.flag = FlowFlagStore() # Flag를 저장하는 class 로드및 class variant로 load하기
        self.model = SentenceTransformer(model_name, cache_folder=self.cache_folder)
        save_dir = "SioskServer/router"
        # download.download_file(file="conversation_en.json", save_dir=save_dir)
        with open('conversation.json', 'r', encoding='utf-8') as file:
            unfiltered_sentences = json.load(file)
            for unfiltered_sentences_index, unfiltered_sentences_val in enumerate(unfiltered_sentences):
                self.sentences_train.append(str(unfiltered_sentences_val).split(' | ')[0]) # flag에 따하서 append해주기 -> 4부터 7까지 0 ~ 3까지는 한가지 배열로 넣어두기
                self.sentences_A_train.append(str(unfiltered_sentences_val).split(' | ')[1])
                self.flagment_train.append(str(unfiltered_sentences_val).split(' | ')[2])
                flagment = str(unfiltered_sentences_val).split(' | ')[2]
                if flagment == '4':
                    self.sentences_4.append(str(unfiltered_sentences_val).split(' | ')[0]) # flag에 따하서 append해주기 -> 4부터 7까지 0 ~ 3까지는 한가지 배열로 넣어두기
                    self.sentences_A_4.append(str(unfiltered_sentences_val).split(' | ')[1])
                    self.flagment_4.append(str(unfiltered_sentences_val).split(' | ')[2])
                elif flagment == '5':
                    self.sentences_5.append(str(unfiltered_sentences_val).split(' | ')[0])
                    self.sentences_A_5.append(str(unfiltered_sentences_val).split(' | ')[1])
                    self.flagment_5.append(str(unfiltered_sentences_val).split(' | ')[2])
                elif flagment == '6':
                    self.sentences_6.append(str(unfiltered_sentences_val).split(' | ')[0])
                    self.sentences_A_6.append(str(unfiltered_sentences_val).split(' | ')[1])
                    self.flagment_6.append(str(unfiltered_sentences_val).split(' | ')[2])
                elif flagment == '7' or flagment == '0' or flagment == '1' or flagment == '2' or flagment == '3':
                    self.sentences_7.append(str(unfiltered_sentences_val).split(' | ')[0])
                    self.sentences_A_7.append(str(unfiltered_sentences_val).split(' | ')[1])
                    self.flagment_7.append(str(unfiltered_sentences_val).split(' | ')[2])
                    if flagment != '7':
                        self.sentences.append(str(unfiltered_sentences_val).split(' | ')[0])
                        self.sentences_A.append(str(unfiltered_sentences_val).split(' | ')[1])
                        self.flagment.append(str(unfiltered_sentences_val).split(' | ')[2])
        self.sentences_embeddings_all = self.model.encode(self.sentences_train, convert_to_tensor=True) # encoding하기
        self.sentences_embeddings = self.model.encode(self.sentences, convert_to_tensor=True) 
        self.sentences_embeddings_4 = self.model.encode(self.sentences_4, convert_to_tensor=True)
        self.sentences_embeddings_5 = self.model.encode(self.sentences_5, convert_to_tensor=True)
        self.sentences_embeddings_6 = self.model.encode(self.sentences_6, convert_to_tensor=True)
        self.sentences_embeddings_7 = self.model.encode(self.sentences_7, convert_to_tensor=True)
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
            with open('SioskServer/router/airing_data.json', 'r', encoding='utf-8') as file:
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
            similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings_all)
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
            similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings_all)
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
        
    def checking_using_outer_api(self, similarities_list, index_max_val, single_sentence):
        max_comparison_val = similarities_list[index_max_val]
        if max_comparison_val > 0.8:
            return True
        else:
            answer = self.callinggemini.creating_response(single_sentence)
            return answer
        
    def compare(self, similarities_list, single_sentence, last_flag):
        if last_flag >= 3:
            sentences = getattr(self, f"sentences_{last_flag + 1}") # 변수 생성한후 변수에 저장하기
            sentences_A = getattr(self, f"sentences_A_{last_flag + 1}") # "
            flagment = getattr(self, f"flagment_{last_flag + 1}") # "
        else:
            sentences = self.sentences
            sentences_A = self.sentences_A
            flagment = self.flagment
        max_val = max(similarities_list)
        index_max_val = list(similarities_list).index(max_val)
        checkpoint = self.checking_using_outer_api(similarities_list, index_max_val, single_sentence)
        if type(checkpoint) == str:
            print("\033[33m" + "\nLOG" + "\033[0m" + ":" + f"     Question looks Non related with Ordering")
            print("\033[33m" + "\nLOG" + "\033[0m" + ":" + f"     Predicted Script data '{single_sentence}'")
            print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Predicted Script answer '{checkpoint}'")
            return single_sentence, checkpoint, False
        elif type(checkpoint) == bool:
            print("\033[33m" + "\nLOG" + "\033[0m" + ":" + f"     Predicted Script data '{sentences[index_max_val]}'")
            print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Predicted Script answer '{sentences_A[index_max_val]}'")
            # print(similarities_list)
            # print(sentences[index_max_val], sentences_A[index_max_val], True, flagment[index_max_val])
            return sentences[index_max_val], sentences_A[index_max_val], True, flagment[index_max_val]

    def process(self, ques):
        current_flag_array = self.flag.flag_store_share_func()
        if len(current_flag_array) != 0:
            last_flag = int(current_flag_array[-1]) # 지금까지의 flag 배열들 받아오기
        else:
            last_flag = 0
        single_sentence = ques
        start = time.time()
        if last_flag < 3:
            single_embedding = self.model.encode(single_sentence, convert_to_tensor=True) # single qeustion들 encode
            similarities = util.pytorch_cos_sim(single_embedding, self.sentences_embeddings) # 유사도 검사하기
        else:
            renewal_flag = f"sentences_embeddings_{last_flag + 1}" # flag renewal하기 -> 변수 생성하기
            val = getattr(self, renewal_flag) # 변수화하기
            single_embedding = self.model.encode(single_sentence, convert_to_tensor=True) # encode하기
            similarities = util.pytorch_cos_sim(single_embedding, val) # cos_sim 구현하기
        similarities_list = similarities.squeeze().tolist()
        # import pdb
        # pdb.set_trace()
        try:
            predicted_Q, predicted_A, Hint, flag = self.compare(similarities_list, single_sentence, last_flag) # compare로 유사도, 일반 문장, 마지막 flag 전송하기 
        except ValueError:
            predicted_Q, predicted_A, Hint = self.compare(similarities_list, single_sentence, last_flag)
            flag = "Gemini"
        if Hint == True:
            modified_A = self.flag.flag_handler(predicted_Q, predicted_A)
            if modified_A == 0:
                pass
            elif modified_A == -1:
                return False, False, False
            else:
                predicted_A = modified_A
        elif Hint == False:
            pass
        end = time.time()
        print("\033[33m" + "LOG" + "\033[0m" + ":" + f"     Embedded Time: {str(end - start)}\n")
        # print(predicted_Q, predicted_A, end - start, flag)
        return predicted_Q, predicted_A, end - start, flag
    
    def Airing(self):
        self.quality_check() # Random Data Airing
        self.quality_check_main() # Real Data Airing
        os.system(clear_terminal())
            
    def run(self, ques):
        predicted_Q, predicted_A, embedded_time, flag = self.process(ques)
        return predicted_Q, predicted_A, embedded_time, flag # flag gemini 처리
    

'''
아이디어 구상 지금은 전체를 모두 scan해서 가장 유사성있는 데이터를 뽑아네지만, 추출할수 있는 데이터에 제한을 둔다면?
더 상황에 맞는 데이터들을 뽑아낼수 있겠지? 그럼 그걸 목표로써 한번 데이터를 filtering해서 그 데이터로 conversation_filtered.json
데이터를 제작하고, 그것 중에서 가장 유사성 높은 데이터를 추출하는 알고리즘으로 변경하자. 
'''