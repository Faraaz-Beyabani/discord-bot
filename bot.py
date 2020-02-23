import os
import random

from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands 

import asyncio
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = 'owo')
token = os.environ['BOT_TOKEN']
yt_list = requests.get('https://www.youtube.com/playlist?list=PLQrjHunXuYt7i9uaxZIdxinu71JjXY7LG')
soup = [a['href'] for a in BeautifulSoup(yt_list).body.find_all('a', class_='yt-simple-endpoint', href=True)]

@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.event
async def on_message(message):
    if not message.author.bot:
        if message.content.startswith('owoplay'):
            await channel.send('youtube.com/'+random.choice(soup))


    await client.process_commands(message)

client.run(token)