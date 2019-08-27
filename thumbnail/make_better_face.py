"""
画像の人間の目を大きくして、フィルターをかける
input:  image format OpenCV
output: image format OpenCV
"""

import os
import cv2
from skimage.util import img_as_float, img_as_ubyte
from eye_bigger import eye_bigger
from filter_skimage import filter_nice


def make_better_face(face):
    """
    画像の人間の目を大きくして、フィルターかける
    """
    try:
        bigeye_face_cv = eye_bigger(face)
        bigeye_face_ski = cv2.cvtColor(bigeye_face_cv, cv2.COLOR_BGR2RGB)

        better_face_ski = img_as_ubyte(filter_nice(img_as_float(bigeye_face_ski)))
        better_face_cv = cv2.cvtColor(better_face_ski, cv2.COLOR_RGB2BGR)

        return better_face_cv
    except:
        return None

if __name__ == '__main__':
    DIR = os.path.abspath(os.path.dirname('__file__'))
    face = cv2.imread(DIR + '/images/' + 'test.jpg')
    face = make_better_face(face)
    cv2.imwrite(DIR + '/images/' + 'output.jpg', face)
  