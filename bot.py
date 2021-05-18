import os

import re
import random

import discord
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()

bot = Bot(command_prefix = '=', case_insensitive=True)
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
    if message.author.bot:
        return

    await bot.process_commands(message)

@bot.command(
    pass_context=True, 
    aliases=['r'],
    help="Ex: =roll 1d6 2d4+2 d20-1",
    brief="Roll various numbers of dice"
)
async def roll(ctx, *dice):
    results = []

    for die in dice:
        match = re.search(r'(?P<times>\d+\*)?(?P<count>\d*?)d(?P<sides>\d+)(?P<mod>[+-]\d+)?', die)
        if not match:
            await ctx.send(f"Invalid syntax: {die}.")
            return
        # elif times := match.group('times') and times > 10:
        #     await ctx.send(f"Roll this dice fewer times: {die}.")
        #     return
        # elif count := match.group('count') and count > 20:
        #     await ctx.send(f"Rolling too many dice: {die}.")
        
        results.extend(roll_result(**match.groupdict()))

    await ctx.send(str(results))

def roll_result(times, count, sides, mod):
    sides = int(sides)
    times = times and int(times[:-1]) or 1
    count = count and int(count) or 1
    mod = mod and int(mod) or 0

    all_results = []

    for i in range(times):
        one_result = {}
        total = 0
        rolls = []

        for j in range(count):
            res = random.randint(1, sides)
            total += res
            rolls.append(res)

        total += mod

        one_result['total'] = total
        one_result['rolls'] = rolls
        one_result['mod']   = mod

        all_results.append(one_result)


    return all_results



bot.run(token)