#!/usr/bin/python

import discord
import asyncio
import configparser
import dpmaster

neko = discord.Client()

config = configparser.ConfigParser()
config.read('config.ini')
token = config['Credentials']['token']
ch_svlist = config['Channels']['servers']
ch_general = config['Channels']['general']

async def sv_update():
    await neko.wait_until_ready()

    message = None
    channel = neko.get_channel(ch_svlist)
    while not neko.is_closed:
        try:
            text = dpmaster.sv_list()
            if not text: text = '-'
            if not message:
                message = await neko.send_message(channel, text)
            else:
                await neko.edit_message(message, text)
            await asyncio.sleep(60)
        except discord.errors.NotFound:
            print('Message deleted. Creating new one.')
            message = None
        except:
            break

async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    channel = neko.get_channel(ch_general)
    text = 'Welcome to the ' + channel.server.name + ' server, ' \
           + member.mention + '!\n'
    await neko.send_message(channel, text)

neko.loop.create_task(sv_update())
neko.run(token)
