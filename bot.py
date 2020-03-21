import os
import re
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = '=')
token = os.environ['BOT_TOKEN']

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
    elif any(rm.id == 629821886955520011 for rm in message.role_mentions): 
        with open('peter_callout.txt', 'r') as file:
            data = file.read().replace('\n', '')
            await message.guild.get_member(135966139070152704).send(data)

    await client.process_commands(message)

@client.command(pass_context=True, aliases=['r'])
async def roll(ctx):
    dice = ctx.message.content.split()[1:]
    roll_results = []
    error = False
    for die in dice:
        result = 0
        try:
            count, sides = die.split('d')
            mod = re.search(r'\d[+\-/*]\d*', sides) or ''
            if mod:
                mod = mod.group()[1:]
                sides = sides.replace(mod, '')
            count = 1 if not count else int(count)
            sides = int(sides)

            for i in range(count):
                result += random.randint(1,sides)
            roll_results.append(str(eval(f'{result}{mod}')))
        except Exception as e:
            error = True
            roll_results.append(die)
    
    if roll_results:
        await ctx.send(' '.join(roll_results))
    if error:
        await ctx.send("Could not parse some dice.")

@client.command(pass_context=True, aliases=['f'])
async def flip(ctx):
    await ctx.send(random.choice(['heads', 'tails']))

client.run(token)