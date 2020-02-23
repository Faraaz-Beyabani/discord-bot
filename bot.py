import os
import discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

token = os.getenv('BOT_TOKEN')

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

client.run(token)