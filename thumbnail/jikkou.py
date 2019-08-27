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

## masking for ios
height,width = OpenCV_image.shape[:-1]
yokomask = np.full((height, int(height/6) , 3), (0,0,0), dtype=np.uint8)
tatemask = np.full((int(height/6), width+int(height/6)*2 , 3), (0,0,0), dtype=np.uint8)
#tate
tmpImg1 = cv.hconcat([yokomask, OpenCV_image])
tmpImg2 = cv.hconcat([tmpImg1, yokomask])
#yoko
tmpImg3 = cv.vconcat([tatemask, tmpImg2])
iosImg = cv.vconcat([tmpImg3, tatemask])


ima = cv.cvtColor(iosImg, cv.COLOR_RGB2BGR)
cv.imwrite('after_last.png' , ima)
