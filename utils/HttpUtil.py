import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_call(url, endpoint, params=None, headers=None):
    try:
        r = requests.get(url + endpoint, params, headers=headers)
        if r.status_code >= 300:
            raise Exception("return status code: " + str(r.status_code) + " detail: " + r.text)
    except Exception as e:
        raise Exception("get api call failed: " + url + endpoint + " with params:" + str(params) + " errors: " + str(e))
    return r.json()


def post_call(url, endpoint, data, headers=None):
    try:
        r = requests.post(url + endpoint, json=data, headers=headers)
        if r.status_code >= 300:
            raise Exception("return status code: " + str(r.status_code) + " detail: " + r.text)
    except Exception as e:
        raise Exception("post api call: " + url + endpoint + " with data:" + str(data) + " errors: " + str(e))
    return r.json()


def put_call(url, endpoint, data, headers=None):
    try:
        r = requests.put(url + endpoint, json=data, headers=headers)
        if r.status_code >= 300:
            raise Exception("return status code: " + str(r.status_code) + " detail: " + r.text)
    except Exception as e:
        raise Exception("put api call: " + url + endpoint + " with data:" + str(data) + " errors: " + str(e))
    return r.json()
