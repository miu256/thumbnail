import os
import unittest
from tuushin import apitushin
from movie import movie
from make_better_face import make_better_face
from ueda import detect_face_xy
import jikkou
import requests
import cv2

baseurl = "https://apiv2.twitcasting.tv"

headers = {
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic {}'.format(jikkou.code)
        }

def getnowlive():
    return str(baseurl + "/search/lives?type=new&limit=1&lang=ja")


class TestThumbnail(unittest.TestCase):
    def setUp(self):
        DIR = os.path.abspath(os.path.dirname('__file__'))
        self.face = cv2.imread(DIR + '/images/' + 'test.jpg')

    def test_token(self):
        self.assertNotEqual(jikkou.code, 'アクセストークン')

    def test_movie(self):
        self.assertIsNotNone(movie('sistercleaire', jikkou.code))

    def test_tsuusin(self):
        nowlive = requests.get(url = getnowlive(),headers = headers).json()
        nowlive_user_id = nowlive['movies'][0]['movie']['user_id']
        self.assertIsNotNone(apitushin(nowlive_user_id, jikkou.code))

    def test_make_better_face(self):
        self.assertIsNotNone(make_better_face(self.face))

    def test_detect_face_xy(self):
        self.assertIsNotNone(detect_face_xy(self.face))

    def tearDown(self):
        self.face = None


if __name__ == '__main__':
    unittest.main()