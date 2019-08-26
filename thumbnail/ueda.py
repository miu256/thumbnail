import cv2 as cv
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def drawing_word(img, color,text,point,fontsize):
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./font/keifont.ttf", fontsize)

    textX,textY = point
    #text = "Are we centered yet?"
    w, h = draw.textsize(text, font)

    bw = 1

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
    height, width, channels = img.shape[:3]

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
    return word_color
