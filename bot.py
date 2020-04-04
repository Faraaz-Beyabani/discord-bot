import os
import re
import random
import json
import time
import asyncio

import discord
from discord import Activity, ActivityType
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
        for channel in client.get_all_channels():
            if channel.name == 'general':
                await channel.send("I have recovered from downtime. Reminders are no longer valid.")
    except Exception as e:
        print(e)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)

@client.command(pass_context=True, aliases=['rem'])
async def remind(ctx):
    text = ctx.message.content
    time_text = text.split()[1]
    reminder = ' '.join(text.split()[2:])

    h, m, s = re.search(r'\d*h', time_text), re.search(r'\d*m', time_text), re.search(r'\d*s', time_text)
    seconds = 0 + (h and int(h.group()[:-1]) * 3600 or 0)
    seconds += m and int(m.group()[:-1]) * 60 or 0
    seconds += s and int(s.group()[:-1]) or 0

    if not reminder or seconds == 0:
        await ctx.send('An empty message or invalid time was entered.')
        return

    await ctx.send('Reminder set.')

    await asyncio.sleep(seconds)
    await ctx.send(f'{ctx.message.author.mention} {reminder}')

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