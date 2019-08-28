import os
import cv2 as cv
from PIL import ImageFont, ImageDraw, Image
import numpy as np

from comset import comset
from tuushin import apitushin
from movie import  movie

#code = 'アクセストークン'
#user_ID = ''

def jikkou(user_ID):
    ext=0

    if(apitushin(user_ID,code) == None):
        print('録画の取得を行います。')
        if(movie(user_ID,code) == None):
            print('取れるサムネが存在しません。')
            ext = 1
        else:
            OpenCV_image,title,tag,profile,category = movie(user_ID,code)
    else:
        OpenCV_image,title,tag,profile,category = apitushin(user_ID,code)

    if(ext == 0):
        print('放送タイトル')
        print(title)
        print('\n設定タグ')
        print(tag)
        print('\nユーザプロフィール')
        print(profile)
        print('\n放送カテゴリ')
        print(category)

        image = comset(OpenCV_image,title,tag,profile,category)

        height,width = image.shape[:-1]
        yokomask = np.full((height, int(height/6) , 3), (0,0,0), dtype=np.uint8)
        tatemask = np.full((int(height/6), width+int(height/6)*2 , 3), (0,0,0), dtype=np.uint8)
        #tate
        tmpImg1 = cv.hconcat([yokomask, image])
        tmpImg2 = cv.hconcat([tmpImg1, yokomask])
        #yoko
        tmpImg3 = cv.vconcat([tatemask, tmpImg2])
        iosImg = cv.vconcat([tmpImg3, tatemask])


        ima = cv.cvtColor(iosImg, cv.COLOR_RGB2BGR)
        cv.imwrite('after_last.png' , ima)

if __name__ == '__main__':
    jikkou(user_ID)
