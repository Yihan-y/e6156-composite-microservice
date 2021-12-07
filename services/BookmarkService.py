import json
import logging
import asyncio
import settings
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bookmark_base = settings.Base.BOOKMARK_URL


def is_bookmarked_task(session, user_id, post_id, headers):
    return bookmark_task(session, headers, user_id, post_id)


def bookmark_by_user_id_task(session, user_id, headers):
    return bookmark_task(session, headers, user_id)


def bookmark_task(session, headers, user_id=None, post_id=None):
    endpoint = '/api/bookmarks'
    url = bookmark_base + endpoint
    params = {}
    if user_id is not None:
        params['user_id'] = user_id
    if post_id is not None:
        params['post_id'] = post_id
    return asyncio.create_task(session.get(url, params=params, headers=headers, ssl=False))