import random
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

import os

from .setu_finder import pixiv_finder
from .model import setu_score

setu_search = on_keyword(['色图','涩图'],priority=3)
@setu_search.handle()
async def setu_search_handle(bot: Bot, event: Event):
    finder = pixiv_finder()
    m = event.message[0]
    #await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}], 没有找到{m}的涩图'))
    m = m.data['text']
    m = m.replace("色图",'')
    m = m.replace('涩图','')
    m = m.replace('瑟图','')
    pic_list = finder.get_id(m)
    pid_list = list(pic_list.keys())
    if(len(pid_list)==0):
        await setu_search.finish(Message(f'没有找到{m}的涩图喵'))
    else:
        pid = random.choice(pid_list)
        title = pic_list[pid]
        image_name = finder.get_image(m,pid)
        file_path = os.path.abspath(image_name)
        print(file_path)
        score = setu_score(image_name, './src/plugins/pixiv/model/setu-resnet-0825.pt',3)
        string = f'[CQ:image,file=file:///{file_path}]标题:{title}\npid:{pid}\n涩图指数{score[0][0]:.4}'
        await setu_search.finish(Message(string))