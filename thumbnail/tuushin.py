import requests
import json

import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from io import BytesIO
import matplotlib.pyplot as plt


def apitushin(user_ID):

    baseurl = "https://apiv2.twitcasting.tv"
    #code = アクセストークン入れてね〜〜〜〜


    headers = {
        'X-Api-Version' : '2.0',
        'Authorization' : 'Basic {}'.format(code)
    }


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

    return OpenCV_image,title,tag,profile,category
