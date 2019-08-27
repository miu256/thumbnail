import cv2 as cv
from PIL import ImageFont, ImageDraw, Image
import numpy as np

from comset import comset
from tuushin import apitushin
from movie import  movie

#code = 'アクセストークン入れてね'
#user_ID = 'ユーザID入れてね'

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

    ima = cv.cvtColor(OpenCV_image, cv.COLOR_RGB2BGR)
    cv.imwrite('Before.png' , ima)


    image = comset(OpenCV_image,title,tag,profile,category)

    ima = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    cv.imwrite('after_last.png' , ima)
