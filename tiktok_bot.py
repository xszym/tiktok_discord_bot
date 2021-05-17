import os
import string
import random
import time

import asyncio
import pprint
import redis
from dotenv import load_dotenv
from TikTokApi import TikTokApi


verifyFp = os.environ.get('TIKTOK_TOKEN', None)
if verifyFp is None:
    tiktok_api = TikTokApi.get_instance()
else:
    did = ''.join(random.choice(string.digits) for num in range(19))
    tiktok_api = TikTokApi.get_instance(custom_verifyFp=verifyFp, custom_did=did)

redis_db = redis.Redis(host='redis', port=6379)

TIKTOK_NAME = os.environ.get('TIKTOK_USER_NAME')

def get_tiktoks_ids_for_user(username=TIKTOK_NAME, count=1):
    # returns list of ids
    tiktoks = tiktok_api.byUsername(username, count=count)
    result = []
    for tiktok in tiktoks:
        result.append(tiktok['id'])
    return result

def get_tiktok_stats(tiktok_id):
    itemStruct = tiktok_api.get_tiktok_by_id(tiktok_id)['itemInfo']['itemStruct']

    # ['diggCount', 'shareCount', 'commentCount', 'playCount']
    tiktok_stats = itemStruct['stats']

    # {'followingCount': 191, 'followerCount': 446, 'heartCount': 22500, 'videoCount': 11, 'diggCount': 3176, 'heart': 22500}
    tiktok_author_stats = itemStruct['authorStats']

    return tiktok_stats, tiktok_author_stats


def update_tiktok_stats_to_db():
    tiktok_stats, tiktok_author_stats = {}, {}
    try:
        tiktok_stats, tiktok_author_stats = get_tiktok_stats(tiktok_id)
        print("followerCount:", tiktok_author_stats.get('followerCount'), 
          "| heartCount:", tiktok_author_stats.get('heartCount'))
        print("diggCount:", tiktok_stats.get('diggCount'), 
          "| commentCount:", tiktok_stats.get('commentCount'),
          "| shareCount:", tiktok_stats.get('shareCount'))
    except:
        print("TikTok data download error")

    try:   
        tiktok_likes = tiktok_stats.get('diggCount', 0)

        redis_db.set('diggCount', tiktok_stats.get('diggCount', 0))
        redis_db.set('shareCount', tiktok_stats.get('shareCount', 0))
        redis_db.set('commentCount', tiktok_stats.get('commentCount', 0))
        redis_db.set('playCount', tiktok_stats.get('playCount', 0))

        redis_db.set('followerCount', tiktok_author_stats.get('followerCount', 0))
        redis_db.set('heartCount', tiktok_author_stats.get('heartCount', 0))
    except:
        print("Update error")
        time.sleep(0.5)


print("TikTokBot starts...")
tiktok_id = os.environ.get('TIKTOK_ID', get_tiktoks_ids_for_user()[0])
while True:
    update_tiktok_stats_to_db()
    time.sleep(3)

