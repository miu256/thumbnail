"""
顔の検出による新サムネの提案
"""

import requests
from time import sleep
import cv2
import io
import numpy as np
from PIL import Image

from get_new_thumbnail_divided import get_new_thumbnail_divided

# TODO: カスケードファイルのパス変更
CASCADE_DIR = './haarcascade/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(CASCADE_DIR)

TIMES = 100
INTERVAL = 2


def suggest_new_thumbnail(error_url_list, error_user_id_list):
    error_images = []
    better_images = []

    for url in error_url_list:
        r = requests.get(url)
        PIL_image = Image.open(io.BytesIO(r.content))
        error_img = np.asarray(PIL_image)

        error_images.append(error_img)

    for i, user_id in enumerate(error_user_id_list):
        get_current_live_url = "https://apiv2.twitcasting.tv/users/" + user_id + "/live/thumbnail?size=large&position=latest"

        for getImage in range(TIMES):
            latest_img = requests.get(url=get_current_live_url)

            if latest_img.status_code == 200:
                img = Image.open(io.BytesIO(latest_img.content))
                error_img = np.asarray(img)
                error_img_gray = cv2.cvtColor(error_img, cv2.COLOR_RGB2GRAY)

                front_face_list = face_cascade.detectMultiScale(error_img_gray)

                if len(front_face_list) != 0:
                    better_images.append(error_img)
                    break

            if getImage == TIMES - 1:
                better_images.append(error_images[i])

            sleep(INTERVAL)

    return error_images, better_images


if __name__ == '__main__':
    error_images = []
    better_images = []

    res = get_new_thumbnail_divided()
    error_url_list = res[4]
    error_user_id_list = res[5]

    error_images, better_images = suggest_new_thumbnail(error_url_list, error_user_id_list)

    # print('error_images', len(error_images))
    # print('better_images', len(better_images))

    # plt.figure(figsize=(50,35))
    # for i in range(len(error_url_list)):
    #     plt.subplot(len(error_url_list), 2, 2*(i+1)-1)
    #     plt.imshow(error_images[i])

    #     plt.subplot(len(error_url_list), 2, 2*(i+1))
    #     plt.imshow(better_images[i])
