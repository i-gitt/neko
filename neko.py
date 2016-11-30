#!/usr/bin/python

import discord
import asyncio
import configparser
import dpmaster
import oaforum

neko = discord.Client()

config = configparser.ConfigParser()
config.read('neko.ini')
#  config.read('neko_test.ini')
token = config['Credentials']['token']
ch_svlist = config['Channels']['servers']
ch_general = config['Channels']['general']
ch_notifications = config['Channels']['notifications']

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

async def forum_feed():
    await neko.wait_until_ready()
    channel = neko.get_channel(ch_notifications)
    while not neko.is_closed:
        try:
            for text in oaforum.feed():
                await neko.send_message(channel, text)
            await asyncio.sleep(600)
        except Exception as e:
            print(e)
            print('Exception while getting forum feed')

@neko.event
async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    channel = neko.get_channel(ch_general)
    text = 'Welcome to the ' + channel.server.name + ' server, ' \
           + member.mention + '!'
    try:
        await neko.send_message(channel, text)
    except:
        print('Error while sending welcome message.')

@neko.event
async def on_resume():
    print('Resuming...')

@neko.event
async def on_error():
    print('Error occured.')

neko.loop.create_task(sv_update())
neko.loop.create_task(forum_feed())
neko.run(token)
