# genshin-nonebot2


A chatbot based on vits and ChatGPT. It can get response from ChatGPT and convert it to sounds of characters your like.

VITS module used for single-speaker text-to-sound is cloned from https://github.com/JOETtheIV/VITS-Paimon.

VITS module used for multi-speaker text-to-sound is cloned from https://github.com/Plachtaa/VITS-fast-fine-tuning.

Thanks JOETtheIV and Plachtaa for providing the pre-trained models!

## Usage:
Install anaconda.

Create a env with python >= 3.9
```sh
conda create -n <env name> python=3.9
```
Install PyTorch, recommend use conda.

Install Nonebot2, follow instructions in: https://github.com/nonebot/nonebot2.

Install Nonebot2 plugin nonebot-plugin-gocqhttp. See https://github.com/mnixry/nonebot-plugin-gocqhttp.
```sh
nb plugin install nonebot-plugin-gocqhttp
```

Create a new project following Nonebot2's instruction.

Clone this repo:
```sh
git clone https://github.com/Elaina1919/genshin-nonebot2.git
cd genshin-nonebot2
```

Install requirements:
```sh
pip install -r requirements
```

If you get errors when installing pyopenjtalk, you can refer to this video: https://www.bilibili.com/video/BV13t4y1V7DV

Copy vits and vitsmulti to 'src/plugins' folder under your nonebot2 project folder.

Go to your plugins under your bot project folder:
```sh
cd <bot project name>
cd scr/plugins
```

Download pretrained multi-speaker model:
https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth and put it to vitsmulti/model_pt

And download pretrained single speaker model: https://mega.nz/file/4f0CgBaT#Hu4h_ZhVDC6V4RaS9zUeEJJY9cniqKx911z8duPSfCw
 and put it in vits/model_pt

Add your OpenAI api key to vits/chatbot.py and vitsmulti/chatbotmulti.py.

Build Monotonic Alignment Search for vits and vitsmulti:

```sh
cd vits/monotonic_align
python setup.py build_ext --inplace
cd ../..
cd vitsmulti/monotonic_align
python setup.py build_ext --inplace
cd ../..
```

Go back to bot project folder and start the bot:
```sh
python bot.py
```


