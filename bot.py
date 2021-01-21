import os
import re
import random
import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import discord
from discord import File, Status, Embed, Color
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()

client = Bot(command_prefix = '=', case_insensitive=True)
token = os.environ['BOT_TOKEN']


with open('./data/races.json') as f:
    races = json.load(f)
with open('./data/jobs.json') as f:
    jobs = json.load(f)


def roll_dice(dice):
    total_results = []

    for die in dice:
        parsed_die = re.search(r'(\d*)d(\d+)([\+\-]\d+)?', die)

        if not parsed_die:
            return None

        num_dice = parsed_die[1]
        sides    = parsed_die[2]
        modifier = parsed_die[3]

        sides = int(sides)
        num_dice = num_dice and int(num_dice) or 1

        if sides > 100 or num_dice > 100:
            return None

        roll_results = [0]

        for i in range(num_dice):
            roll = random.randint(1, sides)

            roll_results.append(roll)
            roll_results[0] += roll

        if modifier:
            roll_results.append(modifier)
            roll_results[0] += int(modifier)

        total_results.append(roll_results)

    return total_results

async def check_repost(guild, content, time):
    gen_channels = [610914973853679648,
                    691100088004771910,
                    404105660184264714,
                    616426939267284995,
                    608799459014475938,
                    717099200592085034]

    for chan_id in gen_channels:
        channel = guild.get_channel(chan_id)
        time_limit = time - timedelta(hours=36)

        async for message in channel.history(limit=None, before=time, after=time_limit):
            if isinstance(content, discord.Embed):
                for e in message.embeds:
                    if e.url == content.url:
                        return message

def str_to_color(string):
    hashed = 0

    for c in string:
        hashed = ord(c) + ((hashed << 5) - hashed)

    color = ''
    for i in range(3):
        value = (hashed >> (i * 8)) & 0xFF
        color += format(value, '02X')

    return int(color, 16)

def scrape_site(url):
    site = requests.get(url)
    soup = BeautifulSoup(site.content, "html.parser")

    return soup

def fetch_spell(soup, url):
    stats = {'Casting Time':"", 'Range':"", 'Components':"", 'Duration':"", 
             'Source':"", 'Level':"", 'Lists':""}

    spell = soup.find_all("div", class_="main-content")[0]

    name = spell.find(class_='page-title').string
    desc = spell.find(id='page-content')

    for table in desc.find_all('table'):
        table.decompose()

    desc = desc.get_text().split('\n')
    cleaned_desc = []
    cleaned_len = 0

    for d in desc:
        if not d:
            continue

        if not all(v for v in stats.values()):
            for s in stats.keys():
                if s in d and not stats[s]:
                    stats[s] = d
                    break
                elif s == 'Level' and 'cantrip' in d:
                    stats[s] = d
                    break
            else:
                if cleaned_len + len(d) <= 2048:
                    cleaned_desc.append(d)
                    cleaned_len += len(d)
                
    if not stats['Level']:
        stats['Level'] = cleaned_desc[0]
        cleaned_desc = cleaned_desc[1:]

    color_search = re.search(r'(?:\d\w+-level )?(\w*)(?: cantrip)?', stats['Level'])[1]
    color = str_to_color(color_search.lower())

    return name, cleaned_desc, color, stats

def fetch_feature(soup, url):
    return "Work In Progress", [], 16711680, {}





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

    if message.embeds:
        content = message.embeds[0]

        original_msg = await check_repost(message.guild, content, message.created_at)

        if original_msg:
            await message.delete()
            reply = f"{message.author.mention}, this content was already sent by " \
                    f"{original_msg.author} on {original_msg.created_at} at {original_msg.jump_url}"

            await message.channel.send(reply)

    res = roll_dice(['d100'])
    if res[0][0] == 1 and len(message.content.split()) >= 3:
        await message.channel.send(' '.join(message.content.split()[-3:]))

    await client.process_commands(message)






@client.command(pass_context=True, aliases=['r'])
async def roll(ctx):
    dice = ctx.message.content.lower().split()[1:]
    results = roll_dice(dice)
    result_message = '\n\n'.join([f'+ {rolls[0]}\n  {"  ".join([str(num) for num in rolls[1:]])}' for rolls in results])
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
        async for message in ctx.history(limit=None, oldest_first=True, after=(datetime.now() - timedelta(minutes = time_limit))):
            try:
                await message.delete()
            except:
                await ctx.send("Not enough permissions to scrub.")
                return
        await ctx.send(f"Done! Scrubbing of <#{channel.id}> finished.")


@client.command(pass_context=True)
async def dnd(ctx):
    split = ctx.message.content.split()[1:]
    category = split[0]
    query = split[1:]

    if len(query) == 0:
        await ctx.send("Please provide a spell or feature name.")
        return
    
    subcategory = ':' + '-'.join(query)

    url = f'http://dnd5e.wikidot.com/{category}{subcategory}'
    soup = scrape_site(url)

    if category == 'spell':
        name, desc, color, misc = fetch_spell(soup, url)
    else:
        name, desc, color, misc = fetch_feature(soup, url)

    embed = Embed()
    embed.url=url
    embed.title=name
    embed.description = "\n\n".join(desc)
    embed.color=color

    for k, v in misc.items():
        embed.add_field(name=k, value=v)

    await ctx.send(embed=embed)


client.run(token)