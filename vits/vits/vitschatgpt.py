import matplotlib.pyplot as plt
import IPython.display as ipd

import os
import json
import math

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

from .commons import intersperse
from .utils import get_hparams_from_file, load_checkpoint
from .data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from .models import SynthesizerTrn
from .text.symbols import symbols
from .text import text_to_sequence

from scipy.io.wavfile import write

from revChatGPT.V3 import Chatbot

# 限制传入vits的文本长度，防止超出显存。对于24G显存的机器，可以设置为200。
MAX_TEXT_LEN = 150

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

class VitsChatGPT:
    def __init__(self, config_path, model_path):
        self.hps = get_hparams_from_file(config_path)
        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model).cuda()
        _ = self.net_g.eval()

        _ = load_checkpoint(model_path, self.net_g, None)
        #self.chatbot = chatbot = Chatbot(api_key=api_key)

    def ask(self, text, chatbot):
        text_answer = chatbot.ask(text)
        audio_text = text_answer[:]
        # 限制传入vits的文本长度，防止超出显存
        if len(text_answer) >= MAX_TEXT_LEN:
            audio_text = text_answer[:MAX_TEXT_LEN] + '阿巴阿巴不想说了'
        stn_tst = get_text(audio_text, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        audio = self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        #audio_ipd = ipd.Audio(audio, rate=self.hps.data.sampling_rate)
        return audio, text_answer