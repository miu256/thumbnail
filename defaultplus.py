#!/usr/bin/env python
# coding: utf-8

# In[18]:


import requests
import json
import pprint
import pandas as pd

import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from io import BytesIO
import matplotlib.pyplot as plt
import requests
import json


baseurl = "https://apiv2.twitcasting.tv"
code = "Y3Nhc2FrdXJlX2l0YWk0LjcyOGNkYWM0NDU3MWQwYWQ2MTkxMDkxMTliNTA1OGFiMDI2YzQxNzkzZTdhMTgxMGM4NjRhOTA5NGFhZDQ1Mjk6OTFmOTY2MDBhMDI5ODlhMTFlNDA3Mzk2ZjBkZmRkZGM1MDhhNDg2MzQ5M2EzOGU2ZjYxZjRkMDg1NjQ1NWZhOA=="

headers = {
    'X-Api-Version' : '2.0',
    'Authorization' : 'Basic {}'.format(code)
}

user_ID = 'aqourshaya'

def getuserlive(user_ID):
    return str(baseurl + '/users/' + user_ID + '/current_live')

def getrealtime(user_ID):
    return str(baseurl + "/users/" + user_ID + "/live/thumbnail?size=large&position=beginning")

#ユーザIDから情報を取得する
userlive = requests.get(url = getuserlive(user_ID),headers = headers).json()
title = userlive['movie']['title']
category = userlive['movie']['category']
profile = userlive['broadcaster']['profile']
tag = userlive['tags']

rimage = requests.get(url = getrealtime(user_ID),headers=headers)
rrimage = rimage.content
immmg = Image.open(BytesIO(rrimage))
OpenCV_image= np.asarray(immmg)
plt.imshow(OpenCV_image)
ima = cv.cvtColor(OpenCV_image, cv.COLOR_RGB2BGR)
cv.imwrite('create.png' , ima)

width,height = immmg.size

print('放送タイトル')
print(title)
print('\n設定タグ')
print(tag)
print('\nユーザプロフィール')
print(profile)
print('\n放送カテゴリ')
print(category)


# In[46]:


import re

class defaultplus(object):
    def __init__(self,limit):
        self.limit = liimit
        pass
    
    
    
    @classmethod
    def puttext(cls, cv_image, text, point, font_path, font_size, color=(0,0,0)):
        
        
        heig,widt,_ = cv_image.shape
        limit = widt
        x = int(widt*0.2)
        limit = limit-x
        
        
        
        font = ImageFont.truetype(font_path, font_size)
        
        cv_rgb_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_rgb_image)
        
        draw = ImageDraw.Draw(pil_image)
        
        if draw.textsize(text,font = font)[0] > limit:
            while draw.textsize(text + '...',font = font)[0] > limit:
                text = text[:-1]
            text = text + '...'
        
        draw.text(point, text, fill=color, font=font)
        cv_rgb_result_image = np.asarray(pil_image)
        cv_bgr_result_image = cv.cvtColor(cv_rgb_result_image, cv.COLOR_RGB2BGR)

        return cv_bgr_result_image
    
    
    def comsize(image,text,fontp,fonts,limit,flg):
        if(limit == 0):
            heig,widt,_ = image.shape
            limit = widt
            x = int(widt*0.1)
            limit = limit-x
        
        font = ImageFont.truetype(fontp, fonts)
        cv_rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_rgb_image)
        draw = ImageDraw.Draw(pil_image)
        if draw.textsize(text,font = font)[0] < limit:
            tssize = int((draw.textsize(text,font = font)[0]))
            tssize = tssize + int(tssize*0.15)
            if(flg == 0):
                return tssize
            else:
                return text
        else:
            while(draw.textsize(text,font = font)[0] > limit):
                text = text[:-1]
            text = text + '...'
            if(flg == 0):
                return int(draw.textsize(text,font = font)[0])+int((draw.textsize(text,font = font)[0])*0.15)
            else:
                return text
        
    
    

    @classmethod
    def overlay(
            cls,
            cv_background_image,
            cv_overlay_image,
            point,
    ):

        overlay_height, overlay_width = OpenCV_image.shape[:2]

        # OpenCV形式の画像をPIL形式に変換(α値含む)
        # 背景画像
        cv_rgb_bg_image = cv.cvtColor(cv_background_image, cv.COLOR_BGR2RGB)
        pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
        # オーバーレイ画像
        cv_rgb_ol_image = cv.cvtColor(cv_overlay_image, cv.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

        # composite()は同サイズ画像同士が必須のため、合成用画像を用意
        pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
                                     (255, 255, 255, 0))
        # 座標を指定し重ね合わせる
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
        result_image =             Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

        # OpenCV形式画像へ変換
        cv_bgr_result_image = cv.cvtColor(
            np.asarray(result_image), cv.COLOR_RGBA2BGRA)

        return cv_bgr_result_image

    def spr(tst):
        box = []
        last = ''
        k = re.compile('[亜-黑ぁ-んァ-ヶ一二三四五六七八九十壱弐参拾百千万萬億兆〇]+')
        for i in range(len(tst)):
            if(None != k.fullmatch(tst[i]) and len(box) < 20):
                box.append(tst[i])
            elif(len(box)<2):
                box.clear
            else:
                break
        for i in range(len(box)):
            last = str(last +  box[i])
        return last


# In[16]:


def colorchange(image):
    image = cv.imread(image)
    # 画像の黒い部分を白に置き換える
    black = [80, 130, 140]
    white = [255, 255, 255]
    image[np.where((image == white).all(axis=2))] = black
    return image


# In[47]:


defont = './font/'

font_path1 = defont + 'RiiPopkkR.otf'
font_path2 = defont + 'Kaiso-Next-B.otf'
font_path3 = defont + 'AoyagiSosekiFont2.otf'
font_path4 = defont + 'font_1_kokugl_1.15_rls.ttf'
font_path5 = defont + 'KS-Kohichi-FeltPen.ttf'
font_path6 = defont + 'ラノベPOP.otf'
font_path7 = defont + 'keifont.ttf'
font_path = font_path4
defau = 47
face = 35
font_size = defau

com1 = "shikou.png"
com2 = "yurucom.png"
com3 = "husen.png"
com4 = "hukidashi1.png"
com5 = "kyouchou.png"
com6 = "kakukaku.png"
com6 = "yokonaga.png"
com = Image.open(com6)
#comim = np.asarray(colorchange(com))
#com = Image.fromarray(np.uint8(comim))


color = (0,0,0)


patern = 'defau'


lef = int(width*(1/14))
rig = int((width*(1/3))+(width*(1/14)))
x = lef
if(patern == 'defau'):
    y = [int(height*0.2),int(height*0.675)]

count,i,tflg,pflg,cflg = 0,0,0,0,0
tagle = len(tag)
text = []


if(len(title) > 13):
    title = defaultplus.spr(title)
if(len(profile) > 13):
    profile = defaultplus.spr(profile)

print(profile)
    
if(len(title) > 1 and tflg == 0 and len(text) < 2):
    tflg =1
    text.append(title)
while(len(tag) > 0 and tagle > i and len(text) < 2):
    if((tag[i] in text[0]) == False):
        text.append(tag[i])
    i += 1
if(len(profile) > 0 and pflg == 0 and len(text) < 2):
    if((profile in text[0]) == False):
        text.append(profile)
    pflg = 1
if(category != None and cflg == 0 and len(text) < 2):
    categoryy = category[:-3]
    text.append(categoryy)
    cflg =1




comsiz = []

        
if(len(text)>0):
    comsiz.append(defaultplus.comsize(OpenCV_image,text[0],font_path,font_size,150,0))
    text[0] = defaultplus.comsize(OpenCV_image,text[0],font_path,font_size,150,1)
if(len(text)>1):
    comsiz.append(defaultplus.comsize(OpenCV_image,text[1],font_path,font_size,150,0))
    text[1] = defaultplus.comsize(OpenCV_image,text[1],font_path,font_size,150,1)

        
print(comsiz)

for i in range(len(comsiz)):
   comsiz[i] = int(comsiz[i])+50
    

wid = []
openim = np.asarray(immmg)
image = openim

for i in range(len(comsiz)):
    comm = com.resize((comsiz[i],int(height*(1/2.5))))
    comm = np.asarray(comm)
    if(i == 0):
        image = defaultplus.overlay(image, comm , (0,int(y[i]*0.5)))
    else:
        image = defaultplus.overlay(image, comm , (0,int(y[i]*0.85)))
    plt.imshow(image)


# In[48]:


i=0
while(i < len(text)):
    image = defaultplus.puttext(image,text[i],(x,y[i]),font_path,font_size,color)
    i+=1

plt.imshow(image)

ima = cv.cvtColor(image, cv.COLOR_RGB2BGR)
cv.imwrite('after_last.png' , ima)

