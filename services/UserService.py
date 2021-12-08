import asyncio
import json
import logging
from utils import HttpUtil
import settings
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

user_base = settings.Base.USER_URL


def validate_user(user_id, headers):
    endpoint = '/api/users/' + user_id
    HttpUtil.get_call(user_base, endpoint, headers=headers)


# /api/users/<user_id> returns list
def get_user_info_by_id_and_field_list(user_id, field_list, headers):
    endpoint = '/api/users/' + user_id
    params = {}
    if field_list is not None:
        params['fields'] = ','.join(field_list)
    res = HttpUtil.get_call(user_base, endpoint, params, headers)
    return {user_id: res[0]}


def get_user_info_by_id(user_id, headers):
    return get_user_info_by_id_and_field_list(user_id, None, headers=headers)


# /api/users returns list
def get_user_info_by_id_list_and_field_list(user_list, field_list, headers):
    endpoint = '/api/users'
    params = {}
    if user_list is not None:
        params['user_id'] = ','.join(user_list)
    if field_list is not None:
        params['fields'] = ','.join(field_list)
    res = HttpUtil.get_call(user_base, endpoint, params, headers)
    return res


def get_user_info_by_id_list(user_set, headers):
    return get_user_info_by_id_list_and_field_list(user_set, None, headers)


def transform_user_list_to_dict(user_list):
    res = {}
    for user in user_list:
        res[user['user_id']] = user
    return res


def get_user_info_task(session, user_id, headers):
    endpoint = '/api/users/' + user_id
    url = user_base + endpoint
    return asyncio.create_task(session.get(url, headers=headers, ssl=False))


def get_address_info(address_id, headers):
    if address_id is None:
        return {
            'state': None,
            'city': None,
            'street_line_1': None,
            'street_line_2': None,
            'zip_code': None
        }
    endpoint = '/api/addresses/' + address_id
    return HttpUtil.get_call(user_base, endpoint, headers=headers)[0]
