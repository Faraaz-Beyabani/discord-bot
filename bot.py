import os
import random

from bs4 import BeautifulSoup
import requests

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

import asyncio
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = 'owo')
token = os.environ['BOT_TOKEN']
yt_list = requests.get('https://www.youtube.com/playlist?list=PLQrjHunXuYt7i9uaxZIdxinu71JjXY7LG')
soup = [a['href'] for a in BeautifulSoup(yt_list.text, 'html.parser').body.find_all('a',{'class':'pl-video-title-link'})]

@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.command(pass_context=True)
async def play(ctx):
    url = 'https://www.youtube.com'+random.choice(soup)

    voice_channel =  ctx.message.author.voice
    if not voice_channel or not voice_channel.channel:
        await ctx.send("You are not connected to a voice channel, idiot.")
        return

    vc = await voice_channel.channel.connect()
    
@client.command(pass_context = True)
async def stop(ctx):
    for x in client.voice_clients:
        if(x == ctx.message.author.voice.channel):
            return await x.disconnect()

    return await ctx.send("I am not connected to any voice channel on this server!")

client.run(token)