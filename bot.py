import discord

client = discord.Client()

token = None
with open('./.env', 'r') as f:
    for line in f:
        token = str(line)

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