import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from fontcom import fontcom
from ueda import drawing_word,detect_face_xy,resize
from gousei import gousei,hantei
from make_better_face import make_better_face

def comset(OpenCV_image,title,tag,profile,category):

    height,width,_ = OpenCV_image.shape

    if(category == None or ('face' in category) != True):
        image = OpenCV_image
        position = 'defau'
    else:
        OpenCV_image = make_better_face(OpenCV_image)
        image,textcolor,edgecolor = resize(OpenCV_image)
        if(textcolor == None and edgecolor == None):
            return OpenCV_image
        xp,yp,wp,hp = detect_face_xy(image)
        height,width,_ = image.shape
        position = hantei(width,xp,wp)
        comza = 0
        if(position == 'right'):
            comza = int(xp)
        elif(position == 'left'):
            comza =  int(xp+wp)

    font_path,font_size,com = fontcom(position,width)

    color = (0,0,0)

    patern = position

    if(patern == 'right' or patern == 'left'):
        lef = int(width*(1/15))
        rig = comza + int(width*(1/15))
        if(patern == 'right'):
            x = lef
        elif(patern == 'left'):
            x = rig
        y = [int(height * 0.25),int(height*0.625)]
    else:
        x = int(width*(1/8))
        y = [int(height*0.2),int(height*0.675)]


    count,i,tflg,pflg,cflg = 0,0,0,0,0
    tagle = len(tag)
    text = []


    if(len(title) > 13):
        title = gousei.spr(title)
    if(len(profile) > 13):
        profile = gousei.spr(profile)


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


    if(patern == 'left' or patern == 'right'):
        if(patern == 'left'):
            limit = -(comza-width)
            limit = limit -int(width*(1/12))
        elif(patern == 'right'):
            limit = comza
            limit = limit -int(width*(1/12))
    else:
        limit = 0


    comsiz = []

    fonts = [0,0]

    if(len(text)>0):
        comsiz.append(gousei.comsize(image,text[0],font_path,font_size,limit,0))
        text[0],fonts[0] = gousei.comsize(image,text[0],font_path,font_size,limit,1)
    if(len(text)>1):
        comsiz.append(gousei.comsize(image,text[1],font_path,font_size,limit,0))
        text[1],fonts[1] = gousei.comsize(image,text[1],font_path,font_size,limit,1)

    print(text)

    if(patern == 'left' or patern == 'right'):
        if(len(text)>0):
            image = drawing_word(image, textcolor,text[0],(x,y[0]),fonts[0],edgecolor,font_path)
        if(len(text)>1):
            image = drawing_word(image, textcolor,text[1],(x,y[1]),fonts[1],edgecolor,font_path)



    if(patern  == 'defau'):
        for i in range(len(comsiz)):
           comsiz[i] = int(comsiz[i])+50


        wid = []

        print(comsiz)

        for i in range(len(comsiz)):
            comm = com.resize((comsiz[i],int(height*(1/2.5))))
            comm = np.asarray(comm)
            if(i == 0):
                image = gousei.overlay(image, comm , (x,int(y[i]*0.5)))
            else:
                image = gousei.overlay(image, comm , (x,int(y[i]*0.85)))


        i=0
        while(i < len(text)):
            image = gousei.puttext(image,text[i],((x+int(width*(1/10))),y[i]),font_path,font_size,color)
            i+=1



    return image
