import re
import os
import time
from multiprocessing import Process, Queue, Pool
import threading
from urllib import request, error
from tqdm import tqdm
import http.client
import datetime
import urllib

import requests

setu_folder ='./src/plugins/pixiv/'
cookie = '' # 替换为你的cookie

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def get_url_code(name):
    url_code = urllib.parse.quote(name)
    return(url_code)

class pixiv_finder:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
                "cookie": cookie,
               "Referer": ""}
        self.refer = 'https://www.pixiv.net/ajax/search/artworks/{0}?word={0}&order=popular_male_d&mode=safe&p=1&s_mode=s_tag&type=all'
    def get_id(self,name):
        url_code = get_url_code(name)
        refer = self.refer.format(url_code)
        header = self.headers
        header['Referer'] = refer
        session = requests.get(refer, headers=header)
        JSON = session.json()
        pic_list ={}
        for data in JSON["body"]["illustManga"]["data"]:
            if 'id' in data.keys():
                #print(data.keys())
                pic_list[data['id']] = data['title']
                #url_list[data['id']] = url[0]
        return(pic_list)
    def get_image(self, name, pic_id):
        URL = "https://www.pixiv.net/ajax/illust/{0}/pages?lang=zh".format(pic_id)
        url_code = get_url_code(name)
        refer = self.refer.format(url_code)
        header = self.headers
        header['Referer'] = refer
        session = requests.get(URL, headers=header)
        JSON1 = session.json()
        print(JSON1)
        url = JSON1["body"][0]["urls"]["original"]
        timeout = 1000
        req = request.Request(url,None, header)
        res = request.urlopen(req, timeout=timeout)
        rstream = res.read()
        if('jpg' in url):
            filename = setu_folder+f'/pixiv/temp/{pic_id}.jpg'
        elif('png' in url):
            filename = setu_folder+f'/pixiv/temp/{pic_id}.png'
        with open(filename,'wb') as f:
            f.write(rstream)
        return(filename)