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
def get_all_posts(headers, offset, limit, order_by):
    try:
        post_list = PostService.get_all(headers, offset, limit, order_by)
        user_set = PostService.get_user_id_set(post_list)
        user_list = UserService.get_user_info_by_id_list_and_field_list(list(user_set), ['user_id', 'nickname'],
                                                                        headers)
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
def get_post_detail(user_id, post_id, headers):
    try:
        resp_list = []
        asyncio.run(async_get_post_info_and_bookmark(resp_list, user_id, post_id, headers))
        post_list = resp_list[0]
        post_list[0]['is_bookmarked'] = len(resp_list[1]) == 1
        user_set = PostService.get_detail_user_id_set(post_list)
        user_list = UserService.get_user_info_by_id_list_and_field_list(list(user_set), ['user_id', 'nickname'],
                                                                        headers)
        user_dict = UserService.transform_user_list_to_dict(user_list)
        transform_detail_post(post_list, user_dict)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(post_list)


# 1. async user service get user info and bookmark service get bookmarked post_id
# 2. user service get address info by address id from thr first rsp
# 3. assemble the data
def get_user_profile(user_id, headers):
    try:
        rsp_list = []
        asyncio.run(async_get_user_info_and_bookmark(rsp_list, user_id, headers))
        # address info
        res = rsp_list[0][0]
        addr_id = res['addr_id']
        res['addr_info'] = UserService.get_address_info(addr_id, headers)
        del res['addr_id']
        del res['links']
        # bookmark list
        bookmark_list = rsp_list[1]
        post_id_list = []
        for bookmark in bookmark_list:
            post_id_list.append(bookmark['post_id'])
        if len(post_id_list) == 0:
            res['bookmark_info'] = []
        else:
            post_list = PostService.get_post_list(post_id_list, headers)
            user_set = PostService.get_user_id_set(post_list)
            user_list = UserService.get_user_info_by_id_list_and_field_list(list(user_set), ['user_id', 'nickname'],
                                                                            headers)
            user_dict = UserService.transform_user_list_to_dict(user_list)
            transform_all_posts(post_list, user_dict)
            res['bookmark_info'] = post_list
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(res)


def update_post_detail(user_id, post_id, data, headers):
    try:
        post_list = PostService.get_post(post_id, headers=headers)
        new_user_id = post_list[0]['user_id']
        if user_id != new_user_id:
            return ResultUtil.fail('fetched user_id incompatible with user_id in session')
        PostService.put_post(post_id, data, headers=headers)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed()


def create_post(user_id, data, headers):
    try:
        data['post_id'] = str(uuid.uuid4())
        data['user_id'] = user_id
        PostService.create_post(data, headers)
    except Exception as e:
        return ResultUtil.fail(str(e))
    return ResultUtil.succeed(code=201)


def parallel_post_user_task(session, user_id, post_id, headers):
    post_coro = PostService.get_post_task(session, post_id, headers=headers)
    bookmark_coro = BookmarkService.is_bookmarked_task(session, user_id, post_id, headers=headers)
    return [post_coro, bookmark_coro]


def parallel_user_bookmark_task(session, user_id, headers):
    user_coro = UserService.get_user_info_task(session, user_id, headers)
    bookmark_coro = BookmarkService.bookmark_by_user_id_task(session, user_id, headers)
    return [user_coro, bookmark_coro]


async def async_get_post_info_and_bookmark(resp_list, user_id, post_id, headers):
    async with aiohttp.ClientSession() as session:
        tasks = parallel_post_user_task(session, user_id, post_id, headers)
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            resp_list.append(await resp.json())


async def async_get_user_info_and_bookmark(rsp_list, user_id, headers):
    async with aiohttp.ClientSession() as session:
        tasks = parallel_user_bookmark_task(session, user_id, headers)
        responses = await asyncio.gather(*tasks)
        for rsp in responses:
            rsp_list.append(await rsp.json())


def transform_all_posts(post_list, user_dict):
    for post in post_list:
        user_id = post['user_id']
        post['nickname'] = user_dict[user_id]['nickname'] if user_id in user_dict else 'user no longer exists'


def transform_detail_post(post_list, user_dict):
    post = post_list[0]
    curr_id = post['user_id']
    post['nickname'] = user_dict[curr_id]['nickname'] if curr_id in user_dict else 'user no longer exists'
    if 'comments' in post:
        comment_list = post['comments']
        for comment in comment_list:
            curr_id = comment['user_id']
            comment['nickname'] = user_dict[curr_id]['nickname'] if curr_id in user_dict else 'user no longer exists'
            if 'responses' in comment:
                rsp_list = comment['responses']
                for rsp in rsp_list:
                    curr_id = rsp['user_id']
                    rsp['nickname'] = user_dict[curr_id]['nickname'] if curr_id in user_dict \
                        else 'user no longer exists'


