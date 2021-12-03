import json
import logging
import asyncio
from utils import HttpUtil
import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

post_base = settings.Base.POST_URL


# /api/posts returns list
def get_all(cookies):
    endpoint = '/api/posts'
    res = HttpUtil.get_call(post_base, endpoint, cookies=cookies)
    return res


# /api/posts/<post_id> returns list
def get_post(post_id, cookies):
    endpoint = '/api/posts/' + post_id
    res = HttpUtil.get_call(post_base, endpoint, cookies=cookies)
    return res


def put_post(post_id, data, cookies):
    endpoint = "/api/posts/" + post_id
    HttpUtil.put_call(post_base, endpoint, data, cookies)


def create_post(data, cookies):
    endpoint = '/api/posts'
    HttpUtil.post_call(post_base, endpoint, data, cookies)


def get_user_id_set(post_list):
    res = set()
    for post in post_list:
        res.add(post['user_id'])
    return res


def get_post_task(session, post_id, cookies):
    endpoint = '/api/posts/' + post_id
    url = post_base + endpoint
    return asyncio.create_task(session.get(url, cookies=cookies, ssl=False))

