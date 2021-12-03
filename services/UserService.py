import json
import logging
from utils import HttpUtil
import settings
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

user_base = settings.Base.USER_URL


def validate_user(user_id, cookies):
    endpoint = '/api/users/' + user_id
    HttpUtil.get_call(user_base, endpoint, cookies=cookies)


# /api/users/<user_id> returns list
def get_user_info_by_id_and_field_list(user_id, field_list, cookies):
    endpoint = '/api/users/' + user_id
    params = {}
    if field_list is not None:
        params['fields'] = ','.join(field_list)
    res = HttpUtil.get_call(user_base, endpoint, params, cookies)
    return {user_id: res[0]}


def get_user_info_by_id(user_id, cookies):
    return get_user_info_by_id_and_field_list(user_id, None, cookies=cookies)


# /api/users returns list
def get_user_info_by_id_list_and_field_list(user_list, field_list, cookies):
    endpoint = '/api/users'
    params = {}
    if user_list is not None:
        params['user_id'] = ','.join(user_list)
    if field_list is not None:
        params['fields'] = ','.join(field_list)
    res = HttpUtil.get_call(user_base, endpoint, params, cookies)
    return res


def get_user_info_by_id_list(user_set, cookies):
    return get_user_info_by_id_list_and_field_list(user_set, None, cookies)


def transform_user_list_to_dict(user_list):
    res = {}
    for user in user_list:
        res[user['user_id']] = user
    return res
