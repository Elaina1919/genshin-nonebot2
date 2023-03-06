from nonebot.plugin import on_keyword, on_startswith, on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import os
import collections
import soundfile as sf
import time

from .vits.vitschatgpt import VitsChatGPT

from revChatGPT.V3 import Chatbot

AUDIO_PATH_MULTI = './src/plugins/vitsmulti/soundfile/'
CONFIG_FILE_MULTI = './src/plugins/vitsmulti/vits/configs/modified_finetune_speaker.json'
MODEL_FILE_MULTI = './src/plugins/vitsmulti/vits/model_pt/G_trilingual.pth'
API_KEY_MULTI = '' # 请替换为你的API Key, 请勿泄露

#每个用户和每个角色对应一个chatbot
chatbot_dict_multi = collections.defaultdict(lambda: collections.defaultdict(Chatbot))
user_set_multi = collections.defaultdict(int)

vits_multi = VitsChatGPT(CONFIG_FILE_MULTI, MODEL_FILE_MULTI)

speak_list = {'九条裟罗': 92, '一斗': 96, '绫华': 99, '绫人':154, '妮露':159, '胡桃': 160, '纳西妲':162}

genshin_list = on_fullmatch(['查看所有角色'],priority=3)
@genshin_list.handle()
async def genshin_list_handle(bot: Bot, event: Event):
    user_id = event.get_user_id()
    answer_text = '旅行者你好，目前支持的juese有：派蒙'
    for speak in speak_list.keys():
        answer_text += ','+speak
    await bot.call_api('send_private_msg',user_id=user_id,message=answer_text)
    await genshin_list.finish()

genshin_gpt = on_startswith(speak_list.keys(),priority=5)
@genshin_gpt.handle()
async def genshin_gpt_handle(bot: Bot, event: Event):
    m = event.message[0]
    m = m.data['text']
    speaker = None
    for speak in speak_list.keys():
        if m.startswith(speak):
            speaker = speak
            break
    if speaker is None:
        await bot.call_api('send_private_msg',user_id=user_id,message='请在消息前加上角色名')
        await genshin_gpt.finish()
    speaker_id = speak_list[speaker]
    user_id = event.get_user_id()
    if user_id not in chatbot_dict_multi or speaker_id not in chatbot_dict_multi[user_id]:
        chatbot_dict_multi[user_id][speaker_id] = Chatbot(api_key=API_KEY_MULTI)
    chatbot = chatbot_dict_multi[user_id][speaker_id]
    audio_answer, text_answer = vits_multi.ask(m, chatbot, speaker_id=speaker_id)
    audio_name = f'{user_id}_{time.time_ns()}.mp3'
    file_path = os.path.abspath(AUDIO_PATH_MULTI)
    file_name = file_path+'\\'+audio_name
    sf.write(file_name,audio_answer,samplerate=vits_multi.hps.data.sampling_rate)
    audio_string = f'[CQ:record,file=file:///{file_name}]'
    if user_id not in user_set_multi or user_set_multi(user_id) == 0:
        await bot.call_api('send_private_msg',user_id=user_id,message=text_answer)
        await bot.call_api('send_private_msg',user_id=user_id,message=audio_string)
    elif user_set_multi(user_id) == 1:
        await bot.call_api('send_private_msg',user_id=user_id,message=text_answer)
    elif user_set_multi(user_id) == 2:
        await bot.call_api('send_private_msg',user_id=user_id,message=audio_string)
    await genshin_gpt.finish()

