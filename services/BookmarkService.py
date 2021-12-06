import json
import logging
import asyncio
import settings
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bookmark_base = settings.Base.BOOKMARK_URL


def is_bookmarked_task(session, user_id, post_id, headers):
    endpoint = '/api/bookmarks'
    url = bookmark_base + endpoint
    params = {'user_id': user_id, 'post_id': post_id}
    return asyncio.create_task(session.get(url, params=params, headers=headers, ssl=False))

