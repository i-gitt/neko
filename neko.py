#!/usr/bin/python

import asyncio
import config
import discord
import json
import subprocess
import string
from datetime import datetime
from oastat import *


def markdown_strip(value):
    value = value.encode("ascii", "ignore").decode()

    pat = "\^[A-Za-z0-9]"
    value = re.sub(pat, '',value)
    md_special_chars = ['_', '*', '>', '`']
    for char in md_special_chars:
        value = value.replace(char, '\\' + char)
    if(value == ""):
        value = "UnnamedPlayer"
    return value.strip()


def build_message():
#    servers = server_list()

    servers = getServerArray()
    servers = sorted(servers, key=lambda x: x.num_humans(), reverse=True)
    message = '\n__ **OpenArena** server list __\n\n'


    for sv in servers:
        players = sv.likely_human_players()
#        players = sorted(players, key=lambda p: p.score, reverse=True)
        servername = markdown_strip(sv.name())
        if('.eu' in servername):
            continue
        elif("lasico.de" in servername):
            servername = markdown_strip(sv.name())[9:]
        else:
            servername = markdown_strip(sv.name())
        new_msg = '**{}** ({}) [map: {}] has `{}` player{}:\n' \
            .format(servername,
                    markdown_strip(sv.saddr()),
                    markdown_strip(sv.map()),
                    len(players),
                    's' if len(players) > 1 else '')

        if(servername == ':F deathmatch'):
            new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join([markdown_strip(p.name[9:]) for p in players]))
        elif(servername == ':F normal ctf for stupids'):
           new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join([markdown_strip(p.name[13:]) for p in players]))
        elif(servername == ':F Insta'):
            new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join([markdown_strip(p.name[6:]) for p in players]))
        elif(servername == ':F ctf for GENIUSES'):
            new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join([markdown_strip(p.name[13:]) for p in players]))
        else:
            new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join([markdown_strip(p.name) for p in players]))

        if (len(message + new_msg) < 1970 and len(players)>0):
            message += new_msg

    message += datetime.utcnow().strftime('%d %b %Y %H:%M (UTC)')

    return message


async def create_new_message(channel):
    try:
        print('Removing previous messages from channel.')
        await channel.purge(limit=5, check=(lambda m: m.author == neko.user))
        print('Creating new message for server list.')
        return await channel.send(build_message())
        await asyncio.sleep(config.svlist_sleep_time)
    except Exception as e:
        print('Error creating new message: ', e)


async def server_list_update(neko):
    await neko.wait_until_ready()

    channel = neko.get_channel(config.svlist_channel)

    message = None

    try:
        message = await channel.fetch_message(channel.last_message_id)
    except discord.NotFound:
        message = await create_new_message(channel)
    except Exception as e:
        print('Could not retrieve last channel message', e)

    while True:
        try:
            await message.edit(content=build_message())
        except discord.NotFound:
            message = await create_new_message(channel)
        except discord.HTTPException:
            print('HTTP exception occured during server list update.')
        except Exception as e:
            print('Exception while editing server message update: ', e)

        await asyncio.sleep(config.svlist_sleep_time)


neko = discord.Client()
neko.loop.create_task(server_list_update(neko))
neko.run(config.token)
