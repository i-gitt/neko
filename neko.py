#!/usr/bin/python

import discord
import asyncio
import config
import stats
import sys
from svlist import sv_update
#  from aiohttp import TCPConnector

neko = discord.Client() # (connector=TCPConnector(keepalive_timeout=120))

# TODO: create file if it doesn't exist
# TODO: empty file - err: Ran out of input
stats.Load()

# global message so we can erase it on shutdown
message = None

@neko.event
async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    general_channel = neko.get_channel(ch_general)
    info_channel = neko.get_channel(ch_info)
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
async def on_message(message2):
    global message
    try:
        if message2.channel.is_private:
            if message2.content == '.shutdown' or message2.content == '.s':
                if message2.author.id == owner:
                    await neko.edit_message(message, '-')
                    neko.logout()
                    sys.exit()
            elif message.content.startswith('.last '):
                m = 0
                h = 0
                if len(message.content[6:]) > 0:
                    h = int(message.content[6:])
                else:
                    m = 1
                answer = stats.QueryTimerange(datetime.timedelta(days=0,
                    seconds=0, microseconds=0, milliseconds=0, minutes=m,
                    hours=h, weeks=0))
                if len(answer) <= 0:
                    return
            # ask server name
            elif message.content.startswith('.sv '):
                answer = stats.QueryServers(message.content[4:])
                if len(answer) <= 0:
                    answer = 'No matches found for *{}*\n'.format(message.content[4:])
            #unsupported command
            else:
                return
            await neko.send_message(message.channel, answer)
    except Exception as e:
        print(e)

neko.loop.create_task(sv_update(neko))
neko.run(token)
