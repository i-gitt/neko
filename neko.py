#!/usr/bin/python

import discord
import asyncio
import config
import stats
import sys
import svlist
#  from aiohttp import TCPConnector

neko = discord.Client() # (connector=TCPConnector(keepalive_timeout=120))

# TODO: create file if it doesn't exist
# TODO: empty file - err: Ran out of input
stats.Load()

@neko.event
async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    general_channel = neko.get_channel(config.ch_general)
    info_channel = neko.get_channel(config.ch_info)
    text = 'Welcome to the ' + general_channel.server.name + ' server, ' \
            + member.mention + '! Check out the ' + info_channel.mention \
            + ' channel.\n' + 'Official OpenArena game download: ' \
            + '<http://openarena.ws/download.php?view.4>'

    try:
        await neko.send_message(general_channel, text)
    except Exception as e:
        print('Error while sending welcome message:\n', e)

@neko.event
async def on_resume():
    print('Resuming...')

@neko.event
async def on_error():
    print('Error occured.')

@neko.event
async def on_message(message):
    try:
        if message.channel.is_private:
            if message.content == '.shutdown' or message.content == '.s':
                if message.author.id == config.owner:
                    await neko.edit_message(svlist.message, '-')
                    neko.logout()
                    sys.exit()
            elif message.content.startswith('.seen '):
                # TODO: discord user timezone issue, timestamps for now are
                # stored as UTC datetimes
                answer = stats.QueryTimestamps(message.content[6:])
                if len(answer) <= 0:
                    answer = 'No matches found for *{}*\n' \
                            .format(message.content[6:])
                await neko.send_message(message.channel, answer)
            elif message.content.startswith('.sv '):
                answer = stats.QueryServers(message.content[4:])
                if len(answer) <= 0:
                    answer = 'No matches found for *{}*\n' \
                            .format(message.content[4:])
                await neko.send_message(message.channel, answer)
    except Exception as e:
        print(e)

neko.loop.create_task(svlist.sv_update(neko))
neko.run(config.token)
