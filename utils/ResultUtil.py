import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_result(msg, data, code=200):
    res = {'msg': msg, 'data': data, 'code': code}
    return res


def fail(msg, code=500):
    return get_result(msg, None, code)


def succeed(data=None, code=200):
    return get_result("success", data, code)

