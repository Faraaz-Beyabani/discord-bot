import os
import json
import random

from helpers import *

import discord
from discord import Embed, Intents, ui, PartialEmoji, ButtonStyle
from discord.ext.commands import Bot

import requests
from googlesearch import search

from dotenv import load_dotenv

load_dotenv()

bot = Bot(command_prefix = '=', case_insensitive=True, intents=Intents.default() | Intents(message_content=True))
token = os.environ['BOT_TOKEN']

@bot.event
async def on_ready():
    try:
        print('Discord.py Version: {}'.format(discord.__version__))
    except Exception as e:
        print(e)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for =help"))

@bot.event
async def on_message(message):
    print(message)
    if message.author.bot:
        return

    if message.embeds:
        content = message.embeds[0]

        original_msg = await check_repost(message.guild, content, message.created_at)

        if original_msg:
            curr_day = message.created_at.day
            orig_day = original_msg.created_at.day

            await message.delete()
            reply = f"{message.author.mention}, this content was already sent by " \
                    f"{original_msg.author.display_name} {'today' if curr_day == orig_day else 'yesterday'} at {original_msg.jump_url}"

            await message.channel.send(reply)

    res = roll_dice(['d100'])
    if res[0][0] == 1 and len(message.content.split()) >= 3:
        await message.channel.send(' '.join(message.content.split()[-3:]))

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def sync(ctx, scope) -> None:
    if ctx.message.author.id == 229103556614029312:
        if scope == 'global':
            synced = await ctx.bot.tree.sync()
        else:
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(
                f"Synced {len(synced)} commands to this server"
            )




@bot.tree.command(
    description="Flips a coin, returning heads or tails."
)
async def flip(interaction):
    await interaction.response.send_message(random.choice(['heads', 'tails']))

@bot.tree.command(
    description="Roll various dice, including modifiers: /roll 2d4+2."
)
async def roll(interaction, dice: str):
    results = roll_dice(dice.split(' '))

    if not results:
        await interaction.response.send_message("Couldn't parse the request. Please make sure you don't have more than 100 dice or 100 sides.")
        return

    result_message = '\n\n'.join([f'+ {rolls[0]}\n  {"  ".join([str(num) for num in rolls[1:]])}' for rolls in results])
    await interaction.response.send_message(f'```diff\n{result_message}```')

@bot.tree.command(
    description="Query a subreddit for a post (rate-limited, nsfw-able)"
)
async def reddit(interaction, subreddit: str):

    posts = requests.get(f"https://www.reddit.com/r/{subreddit}/hot.json?restrict_sr=on&limit=100",
                        headers={'User-Agent': 'RaazOCop:1.0 (by /u/Armtrader'})
    print(posts.headers)
    posts = json.loads(posts.text)

    if posts.get('message'):
        await interaction.response.send_message(posts['message'] + ': Please wait a while before trying again.')
        return

    random_post = posts['data']['children'][int(random.random()*100)]['data']
    link = random_post.get('url_overridden_by_dest')
    link2 = random_post.get('url')
    comments = random_post.get('permalink')

    url = link or link2

    button = ui.Button(url=f'https://www.reddit.com{comments}', label="Open in Browser", style=ButtonStyle.link)
    view = ui.View()
    view.add_item(button)

    await interaction.response.send_message(url, view=view)

@bot.tree.command(
    description="Search for a D&D 5e spell or class feature (BETA)"
)
async def dnd(interaction, query: str):

    try:
        url = list(search(f"site:dnd5e.wikidot.com {query}", num=1, stop=1, pause=0))[0]
    except Exception as e:
        await interaction.response.send_message("Sorry, couldn't find that spell or class feature.")
        return
    soup = scrape_site(url)

    title = soup.find(class_="page-title").string.lower()

    try:
        if query.lower() == 'ability score improvement' or query.lower() == 'asi':
            url = 'http://dnd5e.wikidot.com/'
            name = 'Ability Score Improvement'
            color = str_to_color(name)
            desc = [
                "For most classes: When you reach 4th level, 8th, 12th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1.",
                "For Fighters: When you reach 4th level, and again at 6th, 8th, 12th, 14th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1.",
                "For Rogues: When you reach 4th level, and again at 8th, 10th, 12th, 16th, and 19th level, you can increase one ability score of your choice by 2, or you can increase two ability scores of your choice by 1.",
                "As normal, you can't increase an ability score above 20 using this feature."
            ]
            misc = {}
        elif query.lower() == 'channel divinity' or query.lower() == 'cd':
            url = 'http://dnd5e.wikidot.com/'
            name = 'Channel Divinity'
            color = str_to_color(name)
            desc = [
                "Clerics and paladins get different Channel Divinity options based on their subclass.",  
                "View the class pages below for more details.",
                "[Cleric](http://dnd5e.wikidot.com/cleric)",
                "[Paladin](http://dnd5e.wikidot.com/paladin)"
            ]
            misc = {}
        elif query.lower() == 'extra attack':
            url = 'http://dnd5e.wikidot.com/'
            name = 'Extra Attack'
            color = str_to_color(name)
            desc = [
                "Beginning at 5th level, you can attack twice, instead of once, whenever you take the Attack action on your turn.",
                "For Fighters, the number of attacks increases to three when you reach 11th level in this class and to four when you reach 20th level in this class."
            ]
            misc = {}
        elif query.lower() in title:
            name, desc, color, misc = fetch_spell(soup, url)
        else:
            name, desc, color, misc = fetch_feature(soup, url, query)
    except Exception as e:
        await interaction.response.send_message("Sorry, couldn't find that spell or class feature.")
        return

    embed = Embed()
    embed.url=url
    embed.title=name
    embed.description = "\n\n".join(desc)
    embed.color=(color or 7526629)

    for k, v in misc.items():
        clean_v = v.strip()
        if not clean_v:
            continue
        embed.add_field(name=k, value=clean_v, inline=False)

    await interaction.response.send_message(embed=embed)


bot.run(token)