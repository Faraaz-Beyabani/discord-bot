import os
import re
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
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
})

@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.event
async def on_message(message):
    if message.content.lower().startswith('bot'):
        if re.search('am i', message.content.lower()):
            await message.channel.send('yep, you are')
        elif re.search(r'are*? u', message.content.lower().replace('you', 'u')):
            await message.channel.send(f'yes i am {" ".join(message.content.split()[3:])}')
        elif re.search(r'do[n\'t]*? u', message.content.lower().replace('you', 'u')):
            await message.channel.send('yep, i do')
        elif match := re.search(r'is [a-zA-z]*?', message.content.lower()):
            if message.content.split()[2] in ['your', 'the']:
                await message.channel.send(f'yep, {" ".join(message.content.split()[2:4]).replace("yours", "mine").replace("your", "my").replace("you", "i")} is {" ".join(message.content.split()[4:])}')
            else:
                await message.channel.send(f'yep, {message.content.split()[2].replace("yours", "mine").replace("your", "my").replace("you", "i")} is {" ".join(message.content.split()[3:]).replace("yours", "mine").replace("your", "my").replace("you", "i")}')

    await client.process_commands(message)

# @client.command(pass_context=True)
# async def play(ctx):
#     yt_list = requests.get('https://www.youtube.com/playlist?list=PLQrjHunXuYt7i9uaxZIdxinu71JjXY7LG')
#     soup = [a['href'] for a in BeautifulSoup(yt_list.text, 'html.parser').body.find_all('a',{'class':'pl-video-title-link'})]
#     url = ('https://www.youtube.com'+random.choice(soup)).split('&list')[0]
#     vc = None

#     voice_channel =  ctx.message.author.voice
#     if not voice_channel or not voice_channel.channel:
#         await ctx.send("You are not connected to a voice channel, idiot.\nhttps://tenor.com/r4Hd.gif")
#         return
#     elif client.voice_clients:
#         vc = await voice_channel.move_to()

#     loop = asyncio.get_event_loop()
#     data = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
#     filename = data['url']

#     vc = await voice_channel.channel.connect()
#     vc.play(discord.FFmpegPCMAudio(filename, executable='./ffmpeg/bin/ffmpeg.exe', **{'options': '-vn'}))

# @client.command(pass_context = True)
# async def stop(ctx):
#     for x in client.voice_clients:
#         return await x.disconnect()

#     return await ctx.send("You or I are not connected to any voice channel on this server... worgen.\nhttps://tenor.com/r4Hd.gif")

client.run(token)