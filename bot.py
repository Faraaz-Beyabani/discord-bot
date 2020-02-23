import os
import random

from bs4 import BeautifulSoup
import requests
import asyncio
import youtube_dl as ytdl

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import FFmpegAudio

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = 'owo')
token = os.environ['BOT_TOKEN']
ydl = ytdl.YoutubeDL({
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
})


@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.command(pass_context=True)
async def play(ctx):
    yt_list = requests.get('https://www.youtube.com/playlist?list=PLQrjHunXuYt7i9uaxZIdxinu71JjXY7LG')
    soup = [a['href'] for a in BeautifulSoup(yt_list.text, 'html.parser').body.find_all('a',{'class':'pl-video-title-link'})]
    url = ('https://www.youtube.com'+random.choice(soup)).split('&list')[0]

    voice_channel =  ctx.message.author.voice
    if not voice_channel or not voice_channel.channel:
        await ctx.send("You are not connected to a voice channel, idiot.\nhttps://tenor.com/r4Hd.gif")
        return
    elif client.voice_clients:
        await ctx.send("Already connected to a channel, moron.\nhttps://tenor.com/r4Hd.gif")
        return

    file = ydl.extract_info(url, download=True)
    path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    vc = await voice_channel.channel.connect()
    vc.play(discord.FFmpegPCMAudio(path), after=lambda: os.remove(path))
    
@client.command(pass_context = True)
async def stop(ctx):
    for x in client.voice_clients:
        return await x.disconnect()

    return await ctx.send("You or I are not connected to any voice channel on this server... worgen.\nhttps://tenor.com/r4Hd.gif")

client.run(token)