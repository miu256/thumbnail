#!/usr/bin/env python
# coding: utf-8

# In[207]:


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

import re


# In[208]:


def drawing_word(img, color,text,point,fontsize):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./font/keifont.ttf", fontsize)
    
    textX,textY = point
    #text = "Are we centered yet?"
    w, h = draw.textsize(text, font) 
    
    bw = 2
    
    draw.text((textX-bw, textY-bw), text,(0,0,0),font=font)
    draw.text((textX+bw, textY-bw), text,(0,0,0),font=font)
    draw.text((textX+bw, textY+bw), text,(0,0,0),font=font)
    draw.text((textX-bw, textY+bw), text,(0,0,0),font=font)
    draw.text((textX, textY), text, color, font=font)
    
    img = np.asarray(img)
    return img
    
    
def Get_backImg(img):
    # 画像を読み込む。
    
    # 画像で使用されている色一覧。(W * H, 3) の numpy 配列。
    colors = img.reshape(-1, 3)
    
    # cv2.kmeans に渡すデータは float 型である必要があるため、キャストする。
    colors = colors.astype(np.float32)
    # k平均法でクラスタリングする。
    # クラスタ数
    #K = 3
    K = 5

    # 最大反復回数: 10、移動量の閾値: 1.0
    criteria = cv.TERM_CRITERIA_MAX_ITER + cv.TERM_CRITERIA_EPS, 10, 1.0

    ret, label, center = cv.kmeans(
        colors, K, None, criteria, attempts=10, flags=cv.KMEANS_RANDOM_CENTERS
    )
    # ret: 127443.79220199585, label: (48380, 1), center: (8, 3)
    _, counts = np.unique(label, axis=0, return_counts=True)
    tmp = np.argmax(counts)
    color = center[tmp]
    
    return color
    

def detect_face(img):      
    face_img = img.copy()
    face_rects = face_cascade.detectMultiScale(face_img, scaleFactor = 1.01, minNeighbors = 3) 
    
    for (x,y,w,h) in face_rects: 
        cv.rectangle(face_img, (x,y), (x+w,y+h), (255,245,0), 2) 
        
    return face_img


def detect_face_xy(img):   
    # xml の中身は諸説あります
    face_cascade = cv.CascadeClassifier("haarcascade/haarcascade_frontalface_alt.xml")

    face_img = img.copy()
    face_rects = face_cascade.detectMultiScale(face_img, scaleFactor = 1.01, minNeighbors = 3) 
    
    face_area = []
    
    # face_rects　には顔認識した複数座標が入っている
    for (xpoint,ypoint,wpoint,hpoint) in face_rects: 
        cv.rectangle(face_img, (xpoint,ypoint), (xpoint+wpoint,ypoint+hpoint), (255,245,0), 2) 
        face_area.append([wpoint*hpoint, xpoint, ypoint, wpoint, hpoint])
        
    face_area.sort()
    xpoint,ypoint,wpoint,hpoint = face_area[-1][1:]
    
    return xpoint,ypoint,wpoint,hpoint


def resize(img,flg):
    x,y,w,h = detect_face_xy(img)
    height, width, channels = OpenCV_image.shape[:3]
    
    margin = 15
    right_edge = min(x + w + margin, width)
    left_edge = max(0, x - margin)
    
    if x > (width - (x+w)):
        margin = min(margin, width-right_edge)
        cutImg = img[:, 0: right_edge]
        backcolorImg = img[:,0: left_edge]
        maskcolor = Get_backImg(backcolorImg)
        
        mask = np.full((height, width - right_edge, 3), maskcolor, dtype=np.uint8)
        maskedImg = cv.hconcat([mask, cutImg])
        word_color = generate_word_leftside(maskedImg, maskcolor, right_edge)
        #img = drawing_word(maskedImg, word_color)
    
    else:
        margin = min(margin, left_edge)
        cutImg = img[:, left_edge: width]
        backcolorImg = img[:,right_edge: width]
        maskcolor = Get_backImg(backcolorImg)

        mask = np.full((height, left_edge, 3), maskcolor, dtype=np.uint8)
        maskedImg = cv.hconcat([cutImg, mask])
        word_color = generate_word_rightside(maskedImg, maskcolor, right_edge)
        #img = drawing_word(maskedImg, word_color)
    
    if(flg == 0):
        return maskedImg
    else:
        return word_color
    

def calculate_ComplementaryColor(color):
    RGBmax = max(color)
    RGBmin = min(color)
    base = RGBmax + RGBmin
    
    if (RGBmax - RGBmin) < 40:
        ComplementaryR = int(255 - color[0])
        ComplementaryG = int(255 - color[1])
        ComplementaryB = int(255 - color[2])
        
    else:
        ComplementaryR = int(base - color[0])
        ComplementaryG = int(base - color[1])
        ComplementaryB = int(base - color[2])
        
    maskcolor = (ComplementaryR, ComplementaryG, ComplementaryB)
    return maskcolor


def generate_word_rightside(img, maskcolor,right_edge):
    wordcolor = calculate_ComplementaryColor(maskcolor)
#    cv2.putText(img, 'moi!', (right_edge, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, wordcolor, thickness=2)
    return wordcolor

    
def generate_word_leftside(img, maskcolor,right_edge):
    wordcolor = calculate_ComplementaryColor(maskcolor)
#    cv2.putText(img, 'moi!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, wordcolor, thickness=2)
    return wordcolor

#　実行 
plt.tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False)


# In[225]:


baseurl = "https://apiv2.twitcasting.tv"
code = "Y3Nhc2FrdXJlX2l0YWk0LjcyOGNkYWM0NDU3MWQwYWQ2MTkxMDkxMTliNTA1OGFiMDI2YzQxNzkzZTdhMTgxMGM4NjRhOTA5NGFhZDQ1Mjk6OTFmOTY2MDBhMDI5ODlhMTFlNDA3Mzk2ZjBkZmRkZGM1MDhhNDg2MzQ5M2EzOGU2ZjYxZjRkMDg1NjQ1NWZhOA=="

headers = {
    'X-Api-Version' : '2.0',
    'Authorization' : 'Basic {}'.format(code)
}

user_ID = 'ponnu1119'

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


# In[211]:


def hantei(width,xp,ganmen):
    w = width/2
    if((xp+ganmen) > w):
        return 'right'
    elif((xp+ganmen) < w):
        return 'left'
    else:
        return None


# In[219]:


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
            if(flg == 0):
                return int(draw.textsize(text,font = font)[0] )
            else:
                return text
        else:
            while(draw.textsize(text,font = font)[0] > limit):
                text = text[:-1]
            text = text[:-1]
            text = text + '...'
            if(flg == 0):
                return int(draw.textsize(text,font = font)[0])
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


# In[226]:


image = resize(OpenCV_image,0)
textcolor = resize(OpenCV_image,1)
print(textcolor)
xp,yp,wp,hp = detect_face_xy(image)
heigh,widt,_ = image.shape
position = hantei(widt,xp,wp)
comza = 0
if(position == 'right'):
    comza = int(xp)
elif(position == 'left'):
    comza =  int(xp+wp)
print(widt)
print(comza)
print(position)
plt.imshow(image)


# In[ ]:





# In[227]:


defont = './font/'

font_path1 = defont + 'RiiPopkkR.otf'
font_path2 = defont + 'Kaiso-Next-B.otf'
font_path3 = defont + 'AoyagiSosekiFont2.otf'
font_path4 = defont + 'font_1_kokugl_1.15_rls.ttf'
font_path5 = defont + 'KS-Kohichi-FeltPen.ttf'
font_path6 = defont + 'ラノベPOP.otf'
font_path7 = defont + 'keifont.ttf'
font_path = font_path7
defau = 47
face = 57
font_size = face

com1 = "shikou.png"
com2 = "yurucom.png"
com3 = "husen.png"
com4 = "hukidashi1.png"
com5 = "kyouchou.png"
com6 = "kakukaku.png"
com7 = "yokonaga.png"
com = Image.open(com6)
#comim = np.asarray(colorchange(com))
#com = Image.fromarray(np.uint8(comim))


color = (0,0,0)

defa = 'defau'
patern = position

lef = int(width*(1/14))
rig = comza + int(width*(1/14))
if(patern == 'right' or patern == 'defau'):
    x = lef
elif(patern == 'left'):
    x = rig

if(patern == 'defau'):
    y = [int(height*0.2),int(height*0.675)]
else:
    y = [int(height * 0.25),int(height*0.625)]

count,i,tflg,pflg,cflg = 0,0,0,0,0
tagle = len(tag)
text = []


if(len(title) > 13):
    title = defaultplus.spr(title)
if(len(profile) > 13):
    profile = defaultplus.spr(profile)


if(len(title) > 1 and tflg == 0 and len(text) < 2):
    tflg =1
    text.append(title)
while(len(tag) > 0 and tagle > i and len(text) < 2):
    if(len(text)>0):
        if((tag[i] in text[0]) == False):
            text.append(tag[i])
    else:
        text.append(tag[i])
    i += 1
if(len(profile) > 0 and pflg == 0 and len(text) < 2):
    if(len(text)>0):
        if((profile in text[0]) == False):
            text.append(profile)
    else:
        text.append(profile)
    pflg = 1
if(category != None and cflg == 0 and len(text) < 2):
    categoryy = category[:-3]
    text.append(categoryy)
    cflg =1


if(patern == 'left'):
    limit = -(comza-widt)
    limit = limit -int(width*(1/14))
elif(patern == 'right'):
    limit = comza
    limit = limit -int(width*(1/14))


comsiz = []


if(len(text)>0):
    comsiz.append(defaultplus.comsize(image,text[0],font_path,font_size,limit,0))
    text[0] = defaultplus.comsize(image,text[0],font_path,font_size,limit,1)
if(len(text)>1):
    comsiz.append(defaultplus.comsize(image,text[1],font_path,font_size,limit,0))
    text[1] = defaultplus.comsize(image,text[1],font_path,font_size,limit,1)

print(text)    

if(len(text)>0):
    image = drawing_word(image, textcolor,text[0],(x,y[0]),font_size)
if(len(text)>1):
    image = drawing_word(image, textcolor,text[1],(x,y[1]),font_size)
    

if(patern  == 'defau'):
    #for i in range(len(comsiz)):
    #   comsiz[i] = int(comsiz[i])+50


    wid = []

    for i in range(len(comsiz)):
        comm = com.resize((comsiz[i],int(height*(1/2.5))))
        comm = np.asarray(comm)
        if(i == 0):
            image = defaultplus.overlay(image, comm , (x,int(y[i]*0.5)))
        else:
            image = defaultplus.overlay(image, comm , (x,int(y[i]*0.85)))
        plt.imshow(image)
    
    
    i=0
    while(i < len(text)):
        image = defaultplus.puttext(image,text[i],(x,y[i]),font_path,font_size,color)
        i+=1

        
    
plt.imshow(image)

ima = cv.cvtColor(image, cv.COLOR_RGB2BGR)
cv.imwrite('after_last.png' , ima)

