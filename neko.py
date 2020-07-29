#!/usr/bin/python

import asyncio
import config
import discord
import json
import subprocess
from datetime import datetime


def server_list():

    args = ['./qstat']

    args.append('-cfg')
    args.append('qstat.cfg')
    args.append('-u')
    args.append('-ne')
    args.append('-P')
    args.append('-json')
    args.append('-openarenam')
    args.append('dpmaster.deathmask.net')

    # Master servers list alternative: master.ioquake3.org

    completeProcess = subprocess.run(args, capture_output=True)

    servers = json.loads(completeProcess.stdout)

    # filter bots

    for server in servers:
        players = server.get('players', [])
        server['players'] = [p for p in players if 0 < p.get('ping') < 800]

    # filter names

    name_blacklist = ['unnamedplayer']

    for server in servers:
        players = server.get('players', [])
        server['players'] = [p for p in players
                             if p.get('name').lower() not in name_blacklist]

    # filter empty servers

    servers = [s for s in servers if s.get('players')]

    # sort by player count (after filtering)

    servers = sorted(servers, key=lambda sv: len(sv.get('players')),
                     reverse=True)

    return servers


def markdown_strip(value):
    md_special_chars = ['_', '*', '>', '`']
    for char in md_special_chars:
        value = value.replace(char, '\\' + char)
    return value.strip()


def build_message():
    servers = server_list()

    message = '\n__ **OpenArena** server list (*{}*  players online) __\n\n' \
        .format(sum([len(sv.get('players')) for sv in servers]))

    for sv in servers:
        new_msg = '**{}** ({}) [map: {}] has `{}` player{}:\n' \
            .format(markdown_strip(sv.get('name')),
                    markdown_strip(sv.get('hostname')),
                    markdown_strip(sv.get('map')),
                    len(sv.get('players')),
                    's' if len(sv.get('players')) > 1 else '')
        new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join(
            [markdown_strip(p.get('name')) for p in sv.get('players')]))

        if (len(message + new_msg) < 1970):
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
