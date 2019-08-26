"""
画像の人間の目を大きくするよ！
"""

import os
import cv2


# TODO: カスケードファイルのディレクトリ変更
CASCADE_DIR = './haarcascade/haarcascade_eye.xml'
EYE_CASCADE = cv2.CascadeClassifier(CASCADE_DIR)
RATE = 1.1


def eye_bigger(img_opencv):
    """
    画像の人間の目を大きくする
    """
    eyelist, eyes = detect_eyes(img_opencv)
    if eyelist:
        eye1 = eyelist[0]
        eye2 = eyelist[1]
        eye1 = cv2.resize(eye1, (int(eyes[0][2]*RATE), int(eyes[0][3]*RATE)))
        eye2 = cv2.resize(eye2, (int(eyes[1][2]*RATE), int(eyes[1][3]*RATE)))
        return attach_eye(img_opencv, eyes, eye1, eye2)

    return img_opencv


def detect_eyes(img):
    """
    検出した目の座標を返す
    """
    face_img = img.copy()
    eyes = EYE_CASCADE.detectMultiScale(face_img)

    # 検出できなかったらそのまま返す
    if not eyes.any():
        return [], []

    # 一人分の目だけを対象にする
    if len(eyes) > 2:
        idx = len(eyes) - 2
        eyes = eyes[:-idx]

    eyelist = []
    for (x, y, w, h) in eyes:
        # 目が小さすぎる場合は除く
        if w < 10 or h < 10:
            break

        eye = img[y : y+h, x : x+w]
        eyelist.append(eye)

    return eyelist, eyes


def attach_eye(img_opencv, eyes, eye1, eye2):
    """
    目を拡大し、元の画像に合成して返す
    """
    img_bigger_opencv = img_opencv.copy()

    x_offset1 = eyes[0][0]-int(eye1.shape[0]*abs(RATE-1))//2
    y_offset1 = eyes[0][1]-int(eye1.shape[1]*abs(RATE-1))//2
    x_offset2 = eyes[1][0]-int(eye2.shape[0]*abs(RATE-1))//2
    y_offset2 = eyes[1][1]-int(eye2.shape[1]*abs(RATE-1))//2

    img_bigger_opencv[y_offset1:y_offset1+eye1.shape[0], x_offset1:x_offset1+eye1.shape[1]] = eye1
    img_bigger_opencv[y_offset2:y_offset2+eye2.shape[0], x_offset2:x_offset2+eye2.shape[1]] = eye2

    return img_bigger_opencv


if __name__ == '__main__':
    DIR = os.path.abspath(os.path.dirname('__file__'))
    face = cv2.imread(DIR + '/data/' + 'test.png')
    face = eye_bigger(face)
    cv2.imwrite(DIR + '/data/' + 'output.png', face)
