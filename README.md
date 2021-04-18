# tiktok_discord_bot
Sending cat picture for each follower and every N reactions for specific TikTok video. I'm not sure why I did it. 

## Requirements
- Docker engine (https://docs.docker.com/engine/install/)
- Docker compose (https://docs.docker.com/compose/install/)

## Setup
1. Create Discord bot. Go with this tutorial: https://discordpy.readthedocs.io/en/stable/discord.html and save your bot `TOKEN`
2. Get `channel id` from your discord server: https://support.discord.com/hc/pl/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-
3. (Optional) Get `s_v_webid` from cookies. You can find more details here: https://medium.com/dev-genius/tiktok-api-python-41d76c67a833
3. Create `.env` file with following structure, then replace your variables:
```
TIKTOK_USER_NAME=xszym
TIKTOK_ID=6951935417507712261
TIKTOK_TOKEN=verify_knncm38l_P7NU39Dc_n5wg_4GNY_BszS_UfygUATR973L
DISCORD_CHANNEL_ID=123456789012345
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Usage
Simply run `docker-compose up`

Good luck!
