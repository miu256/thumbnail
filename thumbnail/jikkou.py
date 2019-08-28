import os
import cv2 as cv
from PIL import ImageFont, ImageDraw, Image
import numpy as np

from comset import comset
from tuushin import apitushin
from movie import  movie

code = 'Y3Nhc2FrdXJlX2l0YWk0LjcyOGNkYWM0NDU3MWQwYWQ2MTkxMDkxMTliNTA1OGFiMDI2YzQxNzkzZTdhMTgxMGM4NjRhOTA5NGFhZDQ1Mjk6OTFmOTY2MDBhMDI5ODlhMTFlNDA3Mzk2ZjBkZmRkZGM1MDhhNDg2MzQ5M2EzOGU2ZjYxZjRkMDg1NjQ1NWZhOA=='

sample = './sample/'

def jikkou(user_ID, test, stag, scate):
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

        if(test == 1):
            OpenCV_image = Image.open(sample + 'sample3.jpg')
            OpenCV_image = np.asarray(OpenCV_image)
            title = ''
            profile = ''
            tag = stag
            category = scate


        ima = cv.cvtColor(OpenCV_image, cv.COLOR_RGB2BGR)
        cv.imwrite('./output/' + user_ID + '_' + scate + '_' +'create.png' , ima)

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
        cv.imwrite('./output/' + user_ID + '_' + scate + '_' + 'after_last.png' , ima)

if __name__ == '__main__':
    user_ID = ''
    test = 1
    stag = ['顔出し', '初見さん大歓迎']
    scate = 'face'

    jikkou(user_ID, test, stag, scate)
