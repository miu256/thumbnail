import requests
import json
import urllib.request
import io
from io import BytesIO

import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def url_to_image(url):
   # 画像urlをopencvの画像に変換

   latest_img = requests.get(url = url)
   if latest_img.status_code == 200:
       img = Image.open(io.BytesIO(latest_img.content))
       img = np.asarray(img)
   return img


def movie(user_ID,code):

    try:
        baseurl = "https://apiv2.twitcasting.tv"



        headers = {
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic {}'.format(code)
        }


        def getusermovie(user_ID):
            return str(baseurl + '/users/' + user_ID + '/movies')

        def getuserinfo(user_ID):
            return str(baseurl + '/users/' + user_ID)

    #ユーザIDから情報を取得する
        userlive = requests.get(url = getusermovie(user_ID),headers = headers).json()
        title = userlive['movies'][0]['title']
        category = userlive['movies'][0]['category']
        userinfo = requests.get(url = getuserinfo(user_ID),headers = headers).json()
        profile = userinfo['user']['profile']
        tag = []

        imageurl = userlive['movies'][0]['large_thumbnail']
        OpenCV_image = url_to_image(str(imageurl))
        ima = cv.cvtColor(OpenCV_image, cv.COLOR_RGB2BGR)
        cv.imwrite('create.png' , ima)

        return OpenCV_image,title,tag,profile,category

    except:
        return None
