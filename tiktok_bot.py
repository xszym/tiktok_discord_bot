import os
import string
import random
import time
import asyncio

import pprint
import redis
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


TIKTOK_NAME = os.environ.get('TIKTOK_USER_NAME')
redis_db = redis.Redis(host='redis', port=6379)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)

url = "https://tokcount.com/?user=" + TIKTOK_NAME

last_followers_value = -1
def get_account_stats():
    global last_followers_value
    driver.get(url)
    time.sleep(random.randrange(5,10))
    try:
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, '__next')))
        result = myElem.text.split(TIKTOK_NAME)[1].split('Likes')[0].replace('\n', '').replace(',', '').split('Followers')
        result = [int(x) for x in result]
        followers = result[0]
        likes = result[1]
        
        if followers - last_followers_value > 1000 and last_followers_value != -1:
            raise Exception("Wrong number of followes") 

        last_followers_value = followers
        return followers, likes
    except TimeoutException:
        print("Loading took too much time!")


def update_tiktok_stats_to_db():
    try:
        followers, likes = get_account_stats()
        print("followerCount:", followers, 
          "| heartCount:", likes)

        redis_db.set('followerCount', followers)
        redis_db.set('heartCount', likes)

    except:
        print("TikTok data download error")


print("TikTokBot starts...")
while True:
    update_tiktok_stats_to_db()
    time.sleep(5)

