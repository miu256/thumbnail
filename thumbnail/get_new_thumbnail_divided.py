"""
get_new_thumbnail_divided
情報量多いサムネ、デフォルト、エラー(単色など)の判別
"""

import cv2
import os
import urllib.request
import numpy as np
from pprint import pprint

from twicas_req import request_new

# TODO: デフォルト画像のファイル名、パスの変更
TARGET_FILE = 'default.jpg'
IMG_DIR = os.path.abspath(os.path.dirname('__file__')) + '/images/'
IMG_SIZE = (200, 200)


def url_to_image(url):
    # 画像urlをopencvの画像に変換(グレースケール)
    with urllib.request.urlopen(url) as url:
        img = url.read()
        img = np.asarray(bytearray(img), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    return img


def get_new_thumbnail_divided():
    """
    新着配信を100件受け取り、3グループに分類する
    """

    # デフォルト画像の判別器生成
    target_img_path = IMG_DIR + TARGET_FILE
    target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    target_img = cv2.resize(target_img, IMG_SIZE)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)

    # 情報量多いサムネ
    good_url_list = []
    good_user_id_list = []

    # デフォルトサムネ
    default_url_list = []
    default_user_id_list = []

    # エラーサムネ
    error_url_list = []
    error_user_id_list = []

    # 新着配信の受け取り、判別
    new = request_new()
    for movie in new['movies']:
        image_url = str(movie['movie']['large_thumbnail'])

        try:
            comparing_img = url_to_image(image_url)
            comparing_img = cv2.resize(comparing_img, IMG_SIZE)

            (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
            matches = bf.match(target_des, comparing_des)
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)
        except cv2.error:
            # エラー画像の判別
            ret = 100000
            # print('error')
            error_url_list.append(image_url)
            error_user_id_list.append(movie['movie']['user_id'])
            continue

        if ret < 50:
            # default画像の判別(閾値50)
            default_url_list.append(image_url)
            default_user_id_list.append(movie['movie']['user_id'])
        else:
            # 情報量多い画像の判別
            good_url_list.append(image_url)
            good_user_id_list.append(movie['movie']['user_id'])

    return [
        good_url_list, good_user_id_list,
        default_url_list, default_user_id_list,
        error_url_list, error_user_id_list
    ]


if __name__ == '__main__':
    res = get_new_thumbnail_divided()

    good_url_list = res[0]
    good_user_id_list = res[1]
    default_url_list = res[2]
    default_user_id_list = res[3]
    error_url_list = res[4]
    error_user_id_list = res[5]

    print('good数', len(good_url_list))
    pprint(good_url_list)

    print('default数', len(default_url_list))
    pprint(default_url_list)

    print('error数', len(error_url_list))
    pprint(error_url_list)
