from nonebot.plugin import on_keyword, on_startswith
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import os
import collections
import soundfile as sf
import time

from .vits.vitschatgpt import VitsChatGPT

from revChatGPT.V3 import Chatbot

AUDIO_PATH = './src/plugins/vits/soundfile/'
CONFIG_FILE = './src/plugins/vits/vits/configs/biaobei_base.json'
MODEL_FILE = './src/plugins/vits/vits/model_pt/G_1434000.pth'
API_KEY = '' # 请替换为你的API Key, 请勿泄露

chatbot_dict = collections.defaultdict(Chatbot)
user_set = collections.defaultdict(int)

vits = VitsChatGPT(CONFIG_FILE, MODEL_FILE)

# 接收chatgpt回答并且返回vits生成的音频
vits_gpt = on_startswith(['派蒙','gpt'],priority=50)
@vits_gpt.handle()
async def vits_gpt_handle(bot: Bot, event: Event):
    m = event.message[0]
    m = m.data['text']
    m = m.replace("派蒙",'',1)
    user_id = event.get_user_id()
    if user_id not in chatbot_dict:
        chatbot_dict[user_id] = Chatbot(api_key=API_KEY)
    chatbot = chatbot_dict[user_id]
    audio_answer, text_answer = vits.ask(m, chatbot)
    audio_name = f'{user_id}_{time.time_ns()}.mp3'
    file_path = os.path.abspath(AUDIO_PATH)
    file_name = file_path+'\\'+audio_name
    sf.write(file_name,audio_answer,samplerate=vits.hps.data.sampling_rate)
    audio_string = f'[CQ:record,file=file:///{file_name}]'
    if user_id not in user_set or user_set(user_id) == 0:
        await bot.call_api('send_private_msg',user_id=user_id,message=text_answer)
        await bot.call_api('send_private_msg',user_id=user_id,message=audio_string)
    elif user_set(user_id) == 1:
        await bot.call_api('send_private_msg',user_id=user_id,message=text_answer)
    elif user_set(user_id) == 2:
        await bot.call_api('send_private_msg',user_id=user_id,message=audio_string)
    await vits_gpt.finish()