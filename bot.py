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

@client.command(pass_context=True)
async def npc(ctx):
    races = {
        'elf': ['ara', 'be', 'tha', 'dan', 'gali', 'var', 'lego', 'las', 'vol', 'lynn', 'eth', 'riel', 'kiir', 'enna', 'and', 'mor', 'vor'],
        'human': ['del', 'vik', 'thaz', 'mith', 'gan', 'frey', 'mal', 'ath', 'ina', 'arra', 'et', 'ram', 'kina', 'ang', 'der'],
        'dragonborn':  ['ash', 'kry', 'iv', 'gar', 'cleth', 'ava', 'har', 'kor', 'inn', 'verth', 'yarj', 'fek', 'jho', 'mah', 'un', 'ghe', 'ina'],
        'gnome': ['ook', 'nock', 'nam', 'oodle', 'vyn', 'kin', 'fun', 'berg', 'bimp', 'sche', 'kle', 'loop', 'aard', 'bree', 'illa', 'froo'],
        'orc': ['kre', 'nur', 'nor', 'ogg', 'gogg', 'ukk', 'thar', 'lug', 'mur', 'uda', 'sha', 'mog', 'gûl', 'ok', 'grum', 'mhu', 'rex'],
        'dwarf': ['rich', 'din', 'rin', 'albe', 'arge', 'wynn', 'hild', 'gar', 'bru', 'nor', 'thor', 'jörn', 'rik', 'rim'],
        'halfling': ['rin', 'mer', 'ret', 'dri', 'tia', 'os', 'born', 'by', 'mia', 'sera', 'ela', 'jil', 'ver'],
        'tiefling': ['bara', 'kas', 'kis', 'nos', 'am', 'mal', 'isto', 'seis', 'kal', 'ista', 'mon', 'ana', 'rai', 'kos', 'mak'],
    }
    message = ctx.message.content
    name = ''

    if 'half-elf' in message:
        choices = races['elf'] + races['human']
        num = random.randint(2, 4)
        for i in range(num):
            part = random.choice(choices)
            while part in name:
                part = random.choice(choices)
            name += part
    elif 'elf' in message:
        num = random.randint(2, 4)
        for i in range(num):
            part = random.choice(races['elf'])
            while part in name:
                part = random.choice(races['elf'])
            name += part
    elif 'human' in message:
        num = random.randint(2, 3)
        for i in range(num):
            part = random.choice(races['human'])
            while part in name:
                part = random.choice(races['human'])
            name += part
    elif 'dragon' in message:
        num = random.randint(2, 3)
        for i in range(num):
            part = random.choice(races['dragonborn'])
            while part in name:
                part = random.choice(races['dragonborn'])
            name += part
    elif 'gnome' in message:
        num = random.randint(2, 4)
        for i in range(num):
            part = random.choice(races['gnome'])
            while part in name:
                part = random.choice(races['gnome'])
            name += part
    elif 'orc' in message:
        num = random.randint(1, 2)
        for i in range(num):
            part = random.choice(races['orc'])
            while part in name:
                part = random.choice(races['orc'])
            name += part
    elif 'dwarf' in message:
        num = random.randint(2, 3)
        for i in range(num):
            part = random.choice(races['dwarf'])
            while part in name:
                part = random.choice(races['dwarf'])
            name += part
    elif 'half' in message:
        num = 2
        for i in range(num):
            part = random.choice(races['halfling'])
            while part in name:
                part = random.choice(races['halfling'])
            name += part
    elif 'tief' in message:
        num = 2
        for i in range(num):
            part = random.choice(races['tiefling'])
            while part in name:
                part = random.choice(races['tiefling'])
            name += part

    match = re.search(r'(a|e|i|o|u)\1+', name)
    if match:
        name = re.sub(match.group(), match.group()[0]*2, name)

    await ctx.send(name.capitalize())


client.run(token)