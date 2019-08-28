import requests
import jikkou


use_col = ["id", "profile", "tags"]
movie_col = ["title", "duration", "comment_count", "total_view_count"]
features = use_col + movie_col

headers = {
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic {}'.format(jikkou.code)
        }


def request_new():
    return requests.get("https://apiv2.twitcasting.tv/search/lives?limit=100&type=new&lang=ja",
                        headers = headers).json()

def request_recommend():
    return requests.get("https://apiv2.twitcasting.tv/search/lives?limit=100&type=recommend&lang=ja",
                        headers = headers).json()


