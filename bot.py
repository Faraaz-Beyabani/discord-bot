import os

import discord
from discord.ext import commands 

import asyncio
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = 'p')

token = os.environ['BOT_TOKEN']

@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.event
async def on_message(message):
    if not message.author.bot:
        channel = message.channel
        await channel.send(message.content)

    await client.process_commands(message)

client.run(token)