import cv2 as cv
from tuushin import apitushin
from PIL import ImageFont, ImageDraw, Image
import numpy as np

from comset import comset


#user_ID = 'ユーザID入れてね'

OpenCV_image,title,tag,profile,category = apitushin(user_ID)

print('放送タイトル')
print(title)
print('\n設定タグ')
print(tag)
print('\nユーザプロフィール')
print(profile)
print('\n放送カテゴリ')
print(category)



image = comset(OpenCV_image,title,tag,profile,category)

ima = cv.cvtColor(image, cv.COLOR_RGB2BGR)
cv.imwrite('after_last.png' , ima)
