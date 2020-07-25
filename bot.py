import os
import re
import random
import json
import datetime

import discord
from discord import File, Status
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()

client = Bot(command_prefix = '=', case_insensitive=True)
token = os.environ['BOT_TOKEN']


with open('./data/races.json') as f:
    races = json.load(f)
with open('./data/jobs.json') as f:
    jobs = json.load(f)


def roll_die(dice):
    results = [sorted([random.randint(1, int(sides or 20)) for rolls in range(int(count or 1))])[::-1] for count, sides in [die.split('d') for die in dice.split()]]
    return results


@client.event
async def on_ready():
    try:
        print('Discord.py Version: {}'.format(discord.__version__))
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id == 300061459864616962:
        await message.delete()
        return

    if message.channel.id == 710664883661963306:
        await message.channel.send(message.content)
        return

    res = roll_die('d100')
    if res[0][0] == 1 and len(message.content.split()) >= 3:
        await message.channel.send(' '.join(message.content.split()[-3:]))

    await client.process_commands(message)


@client.command(pass_context=True, aliases=['r'])
async def roll(ctx):
    dice = ctx.message.content.lower().split()[1:]
    results = roll_die(' '.join(dice))
    result_message = '\n\n'.join([f'+ {sum(rolls)}\n  {"  ".join([str(num) for num in rolls])}' for rolls in results])
    await ctx.send(f'```diff\n{result_message}```')


@client.command(pass_context=True, aliases=['f'])
async def flip(ctx):
    await ctx.send(random.choice(['heads', 'tails']))


@client.command(pass_context=True, aliases=['c'])
async def choose(ctx):
    try:
        members = [m for m in ctx.guild.members if not m.bot]
        if 'all' in ctx.message.content.lower():
            await ctx.send((random.choice(members)).nick)
        else:
            await ctx.send((random.choice([m for m in members if m.status == Status.online])).nick)
    except Exception as e:
        print(e)
        await ctx.send("Error choosing a user; this command does not work in DMs.")


@client.command(pass_context=True)
async def archive(ctx):
    channel = ctx.channel
    filename = f'./data/{channel}.txt'
    await ctx.send(f'Archiving channel {channel}...')
    with ctx.typing():
        with open(filename, 'w') as f:
            async for message in ctx.history(limit=None, oldest_first=True):
                f.write(message.author.name + '\n')
                if message.content:
                    f.write(message.content + '\n')
                if message.attachments:
                    f.write(message.attachments[0].url + '\n')
                f.write('\n')
        log_file = open(filename, 'rb')
        await client.get_channel(708532851188170845).send(file=File(fp=log_file, filename=f'{channel}.txt'))
        await ctx.send(f"Done! Archive of <#{channel.id}> created at <#708532851188170845>.")
        log_file.close()
    os.remove(filename)


@client.command(pass_context=True)
async def scrub(ctx):
    channel = ctx.channel
    try:
        time_limit = int(ctx.message.content.split()[1])
    except:
        await ctx.send("Invalid parameter.")
        return
    await ctx.send(f'Scrubbing channel {channel}...')
    with ctx.typing():
        async for message in ctx.history(limit=None, oldest_first=True, after=(datetime.datetime.now() - datetime.timedelta(minutes = time_limit))):
            try:
                await message.delete()
            except:
                await ctx.send("Not enough permissions to scrub.")
                return
        await ctx.send(f"Done! Scrubbing of <#{channel.id}> finished.")


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

    if race == 'worgen':
        await ctx.send("...Did you actually just try to do that?")
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

    await ctx.send(name)


client.run(token)