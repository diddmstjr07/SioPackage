from tqdm import tqdm
import json
import shutil
import os
import edge_tts
import tempfile
from auto.voice import play_wav
import wave

class Loading:
    def __init__(self) -> None:
        pass

    def setting_progress_bar(self):
        total_steps = 100   
        progress_bar = tqdm(total=total_steps, dynamic_ncols=True)
        return progress_bar, total_steps

    def update_progress_bar(self, total_steps, progress_bar, percentage):
        steps_to_add = (total_steps * percentage) / 100
        if progress_bar.n + steps_to_add > total_steps:
            steps_to_add = total_steps - progress_bar.n
        progress_bar.update(steps_to_add)

class TextToSpeech:
    def __init__(self) -> None:
        self.VOICE = "en-US-AndrewMultilingualNeural"
        self.Loading = Loading()
        
    
    """
    --------------------
    Name: en-US-AnaNeural
    Gender: Female
    --------------------
    Name: en-US-AndrewMultilingualNeural
    Gender: Male
    --------------------
    Name: en-US-AndrewNeural
    Gender: Male
    --------------------
    Name: en-US-AriaNeural
    Gender: Female
    --------------------
    Name: en-US-AvaMultilingualNeural
    Gender: Female
    --------------------
    Name: en-US-AvaNeural
    Gender: Female
    --------------------
    Name: en-US-BrianMultilingualNeural
    Gender: Male
    --------------------
    Name: en-US-BrianNeural
    Gender: Male
    --------------------
    Name: en-US-ChristopherNeural
    Gender: Male
    --------------------
    Name: en-US-EmmaMultilingualNeural
    Gender: Female
    --------------------
    Name: en-US-EmmaNeural
    Gender: Female
    --------------------
    Name: en-US-EricNeural
    Gender: Male
    --------------------
    Name: en-US-GuyNeural
    Gender: Male
    --------------------
    Name: en-US-JennyNeural
    Gender: Female
    --------------------
    Name: en-US-MichelleNeural
    Gender: Female
    --------------------
    Name: en-US-RogerNeural
    Gender: Male
    --------------------
    Name: en-US-SteffanNeural
    Gender: Male
    --------------------
    """
    
    async def downloading(self):
        folder_path = 'Siosk/assets/audio'
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)
        else:
            os.mkdir(folder_path)
        progress_bar, total_steps = self.Loading.setting_progress_bar()
        with open('Siosk/package/conversation.json', 'r', encoding='utf-8') as file:
            target_datas = json.load(file)
            for target_data_index, target_data_val in enumerate(target_datas):
                target_data_que = str(target_data_val).split(' | ')[0]
                target_data_ans = str(target_data_val).split(' | ')[1]
                if '?' or ' ' in target_data_ans:
                    target_data_ans = target_data_ans.replace('?', ";")
                communicate = edge_tts.Communicate(target_data_ans, self.VOICE)
                await communicate.save(f"Siosk/assets/audio/{target_data_ans}.wav")
                self.Loading.update_progress_bar(total_steps, progress_bar, 100 / len(target_datas))

    async def voice(
            self, 
            target: str, 
            resultment: str, 
            flag: bool
        ) -> None: # model.py line 70

        """Main function"""
        if flag == True: 
            play_wav(resultment)
        elif flag == False:
            communicate = edge_tts.Communicate(target, self.VOICE)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            play_wav(temp_file_path)


