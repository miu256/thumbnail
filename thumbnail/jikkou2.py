import cv2 as cv
from PIL import Image
import numpy as np
import jikkou
from get_new_thumbnail_divided import get_new_thumbnail_divided
from suggest_new_thumbnail import suggest_new_thumbnail
from comset import comset
from tuushin import apitushin
from movie import movie

limit = 3

def jikkou2():
    try:
        res = get_new_thumbnail_divided()
        good_url_list = res[0]
        good_user_id_list = res[1]
        default_url_list = res[2]
        default_user_id_list = res[3]
        error_url_list = res[4]
        error_user_id_list = res[5]
    except:
        return None

    good_cnt = min(len(good_user_id_list), 20)
    default_cnt = min(len(default_user_id_list), limit)
    error_cnt = len(error_user_id_list)

    good_user_id_list = good_user_id_list[:good_cnt]
    default_user_id__list = default_user_id_list[:default_cnt]

    error_images, better_images = suggest_new_thumbnail(error_url_list, error_user_id_list)


    # 情報量多いサムネ
    for user_id in good_user_id_list:
        jikkou_tagged(user_id, 'face')

    # デフォルトサムネ
    for user_id in default_user_id__list:
        jikkou_tagged(user_id, 'defau')

    # 失敗したサムネ
    for i in range(error_cnt):
        jikkou_tagged(error_user_id_list[i], 'error', better_images[i])



def jikkou_tagged(user_ID, scate, better_img = []):
    """
    はじめに識別した後の画像加工
    """
    try:
        OpenCV_image, title, tag, profile, category = apitushin(user_ID, jikkou.code)
    except:
        print('放送が終了してしまいました。')
        return None

    if scate == 'error':
        OpenCV_image = better_img
        scate = 'face'

    # print('放送タイトル')
    # print(title)
    # print('\n設定タグ')
    # print(tag)
    # print('\nユーザプロフィール')
    # print(profile)
    # print('\n放送カテゴリ')
    # print(category)

    ima = cv.cvtColor(OpenCV_image, cv.COLOR_RGB2BGR)
    cv.imwrite('./output/' + user_ID + '_' + scate + '_' + 'create.png', ima)

    image = comset(OpenCV_image, title, tag, profile, category, scate)

    if image is None:
        return None
    height, width = image.shape[:-1]
    yokomask = np.full((height, int(height / 6), 3), (0, 0, 0), dtype=np.uint8)
    tatemask = np.full((int(height / 6), width + int(height / 6) * 2, 3), (0, 0, 0), dtype=np.uint8)
    # tate
    tmpImg1 = cv.hconcat([yokomask, image])
    tmpImg2 = cv.hconcat([tmpImg1, yokomask])
    # yoko
    tmpImg3 = cv.vconcat([tatemask, tmpImg2])
    iosImg = cv.vconcat([tmpImg3, tatemask])

    ima = cv.cvtColor(iosImg, cv.COLOR_RGB2BGR)
    cv.imwrite('./output/' + user_ID + '_' + scate + '_' + 'after_last.png', ima)


if __name__ == '__main__':
    jikkou2()
