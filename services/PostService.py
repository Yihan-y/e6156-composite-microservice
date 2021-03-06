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
def get_all(headers, offset, limit, order_by):
    endpoint = '/api/posts'
    params = {'reverse': True}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    if order_by is not None:
        params['orderby'] = order_by
    res = HttpUtil.get_call(post_base, endpoint, params, headers=headers)
    return res['data']


# /api/posts/<post_id> returns list
def get_post(post_id, headers):
    endpoint = '/api/posts/' + post_id
    res = HttpUtil.get_call(post_base, endpoint, headers=headers)
    return res


def get_post_list(post_list, headers):
    endpoint = '/api/posts'
    params = {'ids': '.'.join(post_list)}
    res = HttpUtil.get_call(post_base, endpoint, params=params, headers=headers)
    return res['data']


def put_post(post_id, data, headers):
    endpoint = "/api/posts/" + post_id
    HttpUtil.put_call(post_base, endpoint, data, headers)


def create_post(data, headers):
    endpoint = '/api/posts'
    HttpUtil.post_call(post_base, endpoint, data, headers)


def get_user_id_set(post_list):
    res = set()
    for post in post_list:
        res.add(post['user_id'])
    return res


def get_post_task(session, post_id, headers):
    endpoint = '/api/posts/' + post_id
    url = post_base + endpoint
    return asyncio.create_task(session.get(url, headers=headers, ssl=False))


def get_post_list_task(session, post_list, headers):
    endpoint = '/api/posts'
    url = post_base + endpoint
    params = {'post_id': ','.join(post_list)}
    return asyncio.create_task(session.get(url, params=params, headers=headers, ssl=False))


def transform_post_list_to_dict(post_list):
    res = {}
    for post in post_list:
        res[post['post_id']] = post
    return res


def get_detail_user_id_set(post_list):
    res = set()
    for post in post_list:
        res.add(post['user_id'])
        if 'comments' in post:
            comment_list = post['comments']
            for comment in comment_list:
                res.add(comment['user_id'])
                if 'responses' in comment:
                    response_list = comment['responses']
                    for rsp in response_list:
                        res.add(rsp['user_id'])
    return res


