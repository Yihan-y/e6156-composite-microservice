import json
import logging
import aiohttp
import asyncio
import uuid
from services import PostService, UserService, BookmarkService
from utils import ResultUtil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# 1. post service get all posts
# 2. extract post data from resp
# 3. make user_id a set
# 4. user service get nickname by user_id set
# 5. add nickname under the corresponding user_id in post data
def get_all_posts(cookies):
    try:
        post_list = PostService.get_all(cookies)
        user_set = PostService.get_user_id_set(post_list)
        user_list = UserService.get_user_info_by_id_list_and_field_list(list(user_set), ['user_id', 'nickname'], cookies)
        user_dict = UserService.transform_user_list_to_dict(user_list)
        transform_all_posts(post_list, user_dict)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(post_list)


# 1. async post service get post data by post_id and bookmark service get boolean by post_id and user_id
# 2. extract post data from post resp and boolean from bookmark resp
# 3. add boolean in the post data
# 4. user service get nickname by user_id from post resp
# 5. add nickname under user_id in post data
def get_post_detail(user_id, post_id, cookies):
    try:
        resp_list = []
        asyncio.run(async_get_post_info_and_bookmark(resp_list, user_id, post_id, cookies))
        post_list = resp_list[0]
        post_list[0]['is_bookmarked'] = len(resp_list[1]) == 1
        user_id = post_list[0]['user_id']
        user_dict = UserService.get_user_info_by_id_and_field_list(user_id, ['user_id', 'nickname'], cookies=cookies)
        transform_all_posts(post_list, user_dict)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(post_list)


def update_post_detail(user_id, post_id, data, cookies):
    try:
        post_list = PostService.get_post(post_id, cookies=cookies)
        new_user_id = post_list[0]['user_id']
        if user_id != new_user_id:
            return ResultUtil.fail('fetched user_id incompatible with user_id in session')
        PostService.put_post(post_id, data, cookies=cookies)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed()


def create_post(user_id, data, cookies):
    try:
        data['post_id'] = str(uuid.uuid4())
        data['user_id'] = user_id
        PostService.create_post(data, cookies)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(code=201)


def parallel_task(session, user_id, post_id, cookies):
    post_coro = PostService.get_post_task(session, post_id, cookies=cookies)
    bookmark_coro = BookmarkService.is_bookmarked_task(session, user_id, post_id, cookies=cookies)
    return [post_coro, bookmark_coro]


async def async_get_post_info_and_bookmark(resp_list, user_id, post_id, cookies):
    async with aiohttp.ClientSession() as session:
        tasks = parallel_task(session, user_id, post_id, cookies)
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            resp_list.append(await resp.json())


def transform_all_posts(post_list, user_dict):
    for post in post_list:
        user_id = post['user_id']
        if user_id in user_dict:
            post['nickname'] = user_dict[user_id]['nickname']
