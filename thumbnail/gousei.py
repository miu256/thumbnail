import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image

import matplotlib.pyplot as plt

import re



def hantei(width,xp,ganmen):
    w = width/2
    if((xp+ganmen) > w):
        return 'right'
    elif((xp+ganmen) < w):
        return 'left'
    else:
        return None



class gousei(object):
    def __init__(self):
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

        overlay_height, overlay_width = cv_overlay_image.shape[:2]

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
