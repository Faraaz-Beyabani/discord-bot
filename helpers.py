import re
import random
from datetime import timedelta

import discord
import requests
from bs4 import BeautifulSoup

def roll_dice(dice):
    total_results = []

    for die in dice:
        parsed_die = re.search(r'(\d*)[dD](\d+)([\+\-]\d+)?', die)

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
    stats = {'Level':"", 'Casting Time':"", 'Range':"", 'Components':"", 'Duration':"", 
             'Source':"", 'Spell Lists':""}
    spell_attrs = ['Casting Time', 'Range', 'Components', 'Duration']

    spell = soup.find_all("div", class_="main-content")[0]

    name = spell.find(class_='page-title').string
    desc = spell.find(id='page-content')

    for table in desc.find_all('table'):
        table.decompose()

    desc = desc.get_text().split('\n')
    cleaned_desc = []
    cleaned_len = 0
    more_info = False

    for d in desc:
        if not d:
            continue

        if not all(v for v in stats.values()):
            for s in stats.keys():
                if len(d.split()) > 7:
                    continue

                if s.lower() in d.lower() and not stats[s]:
                    stats[s] = d
                    break
                elif s == 'Level' and 'cantrip' in d:
                    stats[s] = d
                    break
            else:
                if cleaned_len + len(d) <= 2048:
                    cleaned_desc.append(d)
                    cleaned_len += len(d)
                else:
                    more_info = True
                    break

    if more_info:
        cleaned_desc.append(f'[View online for more details.]({url})')

    color_search = re.search(r'(?:\d\w+-level )?(\w*)(?: cantrip)?', stats['Level'])[1]
    color = str_to_color(color_search.lower())

    stats['Details'] = ''
    for a in spell_attrs:
        stats['Details'] += stats[a] + '\n'
        del stats[a]

    return name, cleaned_desc, color, stats

def fetch_feature(soup, url, feature):

    webpage = soup.find('span', text=re.compile(feature, re.I))
    name = webpage.string

    color = str_to_color(name.lower())

    desc = []
    desc_size = 0
    more_info = False

    webpage_iter = webpage.parent.find_next_sibling()

    while webpage_iter:
        if webpage_iter.name == 'h3':
            break
        elif webpage_iter.name == 'table':
            more_info = True
        elif desc_size + len(webpage_iter.get_text()) <= 2048:
            text = webpage_iter.get_text().strip()

            desc_size += len(text)
            desc.append(text)
        else:
            break

        webpage_iter = webpage_iter.find_next_sibling()

    if more_info:
        desc.append(f'[View online for more details.]({url})')

    return name, desc, color, {}