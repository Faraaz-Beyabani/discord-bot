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
        elif re.search(r'does[n\'t]*? [a-zA-Z]', message.content.lower()):
            if message.content.split()[2] in ['your', 'the']:
                await message.channel.send(f'yep, {" ".join(message.content.split()[2:4]).replace("yours", "mine").replace("your", "my").replace("you", "i")} does {" ".join(message.content.split()[4:]).replace("yours", "mine").replace("your", "my").replace("you", "me")}')
            else:
                await message.channel.send(f'yep, {message.content.split()[2].replace("yours", "mine").replace("your", "my").replace("you", "i")} does {" ".join(message.content.split()[3:]).replace("yours", "mine").replace("your", "my").replace("you", "i")}')
        elif match := re.search(r'is [a-zA-Z]*?', message.content.lower()):
            if message.content.split()[2] in ['your', 'the']:
                await message.channel.send(f'yep, {" ".join(message.content.split()[2:4]).replace("yours", "mine").replace("your", "my").replace("you", "i")} is {" ".join(message.content.split()[4:]).replace("yours", "mine").replace("your", "my").replace("you", "me")}')
            else:
                await message.channel.send(f'yep, {message.content.split()[2].replace("yours", "mine").replace("your", "my").replace("you", "i")} is {" ".join(message.content.split()[3:]).replace("yours", "mine").replace("your", "my").replace("you", "i")}')

    await client.process_commands(message)

client.run(token)