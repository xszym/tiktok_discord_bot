import json
import os
import random
import time

import asyncio
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import nest_asyncio
import pprint
import redis
import requests


nest_asyncio.apply()
redis_db = redis.Redis(host='redis', port=6379)

discord_channel_id = int(os.environ.get('DISCORD_CHANNEL_ID'))
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

emoji_arr = ['0️⃣', '1️⃣', '2️⃣', '3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣', '🐈', '🔟']
pic_every_x_reactions = 5


def get_cat_picture():
    r = requests.get('https://aws.random.cat/meow')
    cat_api_result = json.loads(r.text)
    cat_pic_url = cat_api_result.get('file')
    cat_pic_response = requests.get(cat_pic_url)
    filename = cat_pic_url.split('/')[-1]
    if cat_pic_response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(cat_pic_response.content)
        return filename
    else:
        return None


class MyClient(discord.Client):        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_reactions_count = 0 # int(redis_db.get('diggCount'))
        self.last_followers_count = int(redis_db.get('followerCount'), 0)
        self.last_send_discord_msg = None
        self.msg_channel = None

        # self.reactions_task.start()
        self.followers_task.start()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    
    async def send_msg_with_cat(self, msg_with_cat, msg_no_cat, update_last_send_msg=True):
        cat_pic = get_cat_picture()
        send_msg = None
        if cat_pic is None:
            send_msg = await self.msg_channel.send(msg_no_cat)
        else:
            picture = discord.File(cat_pic)
            send_msg = await self.msg_channel.send(msg_with_cat, file=picture)
            os.remove(cat_pic)
        if update_last_send_msg:
            self.last_send_discord_msg = send_msg

    async def add_emoji_cout_to_last_msg(self, no_of_emocji):
        for x in range(1, no_of_emocji+1):
            await self.last_send_discord_msg.add_reaction(emoji_arr[x])

    @tasks.loop(seconds=1)
    async def followers_task(self):
        # Followers msg
        now_tiktok_followers = int(redis_db.get('followerCount'))
        delta_followers = now_tiktok_followers - self.last_followers_count
        for x in range(self.last_followers_count, now_tiktok_followers):
            await self.send_msg_with_cat( 
                f"Kot dla {x+1} followera ❤️", 
                f"Wszystkie koty się pochowały, więc zdjęcia nie ma, ale specjalne podziękowania dla {now_tiktok_followers} followera <3",
                False)
            print("New follower")
        if now_tiktok_followers > self.last_followers_count:
            self.last_followers_count = now_tiktok_followers

    @tasks.loop(seconds=1)
    async def reactions_task(self):
        # Video reactions msg
        now_tiktok_likes = int(redis_db.get('diggCount'))
        now_tiktok_reactions = int(redis_db.get('diggCount')) + int(redis_db.get('shareCount')) + int(redis_db.get('commentCount'))
        delta_reactions = now_tiktok_reactions - self.last_reactions_count
        if delta_reactions >= pic_every_x_reactions:
            if self.last_send_discord_msg is not None: 
                await self.add_emoji_cout_to_last_msg(pic_every_x_reactions)
                await self.last_send_discord_msg.add_reaction('🐈')
            
            await self.send_msg_with_cat( 
                f"Kot na {now_tiktok_reactions} reakcji ❤️", 
                f"Wszystkie koty się pochowały, więc zdjęcia nie ma, ale jest {now_tiktok_reactions} interakcji w tym {now_tiktok_likes} serduszek <3")
            print("New cat for reactions")
            self.last_reactions_count = now_tiktok_reactions
        else:
            if self.last_send_discord_msg is not None:
                await self.add_emoji_cout_to_last_msg(delta_reactions)
        if delta_reactions > 0:
            print("Reactions delta: ", delta_reactions)

    @followers_task.before_loop
    @reactions_task.before_loop
    async def before_task(self):
        await self.wait_until_ready() # wait until the bot logs in
        self.msg_channel = self.get_channel(discord_channel_id) 
        self.last_followers_count = int(redis_db.get('followerCount'))
    
    
client = MyClient()
client.run(TOKEN)
