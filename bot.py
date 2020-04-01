import os
import re
import random
import json

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = '=')
token = os.environ['BOT_TOKEN']

with open('./races.json') as f:
    races = json.load(f)
with open('./jobs.json') as f:
    jobs = json.load(f)

def roll_die(die):
    result = 0
    count, sides = die.split('d')
    mod = re.search(r'\d[+\-/*]\d*', sides) or ''

    if mod:
        mod = mod.group()[1:]
        sides = sides.replace(mod, '')
    count = 1 if not count else int(count)
    sides = int(sides)

    for i in range(count):
        result += random.randint(1,sides)

    return eval(f'{result}{mod}')

def gen_phys(race):
    score = roll_die(races[race]['height_mod'])
    height = races[race]['height'] + score
    weight = races[race]['weight'] + score * roll_die(races[race]['weight_mod'])

    feet = height // 12
    inches = height % 12

    return f'. {feet}\'{inches}" {weight} lbs.'

@client.event
async def on_ready():
	try:
		print('Discord.py Version: {}'.format(discord.__version__))
	
	except Exception as e:
		print(e)

@client.event
async def on_message(message):
    if 'worgen' in message.content.lower():
        text = message.content
        channel = message.channel
        author = message.author.nick
        client.delete_message(message)
        channel.send(re.sub('worgen', '******', text, flags=re.I) + ' - ' + author)

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
        try:
            result = roll_die(die)
            roll_results.append(str(result))
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
    message = ctx.message.content

    name = ''
    choices = []
    height = 0
    weight = 0
    try:
        race = (re.search(r' [a-zA-Z]+', message)).group()[1:]
    except:
        await ctx.send("Could not find a race in your message.")
        return

    if race == 'halfelf':
        num = random.randint(2, 4)
        choices = races['elf']['names'] + races['human']['names']
    elif race in ['elf', 'gnome']:
        num = random.randint(2, 4)
    elif race in ['human', 'dragonborn', 'dwarf']:
        num = random.randint(2, 3)
    elif race in ['halfling', 'tiefling']:
        num = 2
    elif race == 'orc':
        num = random.randint(1, 2)
    else:
        await ctx.send("Could not parse the given race.")
        print(race)
        return

    if not choices:
        choices = races[race]['names']

    if not name:
        for i in range(num):
            part = random.choice(choices)
            while part in name:
                part = random.choice(choices)
            name += part

    match = re.search(r'(a|e|i|o|u)\1+', name)
    if match:
        name = re.sub(match.group(), match.group()[0]*2, name)

    name = name.capitalize()

    if ',' in message:
        name += f', {random.choice(jobs).capitalize()}'
    if '.' in message:
        name += gen_phys(race)

    await ctx.send(name)

client.run(token)