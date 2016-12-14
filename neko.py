#!/usr/bin/python

import discord
import asyncio
import configparser
import dpmaster
import sys
#  from aiohttp import TCPConnector

message = None

try:
    neko = discord.Client() # (connector=TCPConnector(keepalive_timeout=120))

    configfile = 'neko.ini'
    config = configparser.ConfigParser()
    config.read(configfile)
    token = config['neko']['token']
    ch_general = config['neko']['general']
    ch_info = config['neko']['info']
    owner = config['neko']['owner']

    ch_svlist  = config['svupdate']['channel']
    message_id = config['svupdate']['messages']
    sleep_time = int(config['svupdate']['sleep'])

    #  stats.Load()
except Exception as e:
    print('Error during initialization: ', e)

async def sv_update():
    await neko.wait_until_ready()

    global message
    message = None
    channel = neko.get_channel(ch_svlist)
    if message_id:
        #  print('Message (ID={}) already exists.'.format(message_id) +
                #  ' Overwriting...')
        try:
            message = await neko.get_message(channel, message_id)
        except:
            print('Couldn\'t retrieve message with id={}'.format(message_id))

    if not message:
        try:
            print('Creating new message for server list...')
            text = dpmaster.sv_list()
            if not text: text = '-'
            message = await neko.send_message(channel, text)
            config.set('svupdate', 'messages', message.id)
            with open(configfile, 'w') as f: config.write(f)
        except Exception as e:
            print('Error creating new message: ', e)

    #  assert message

    while not neko.is_closed:
        try:
            text = dpmaster.sv_list()
            if not text: text = '-'
            await neko.edit_message(message, text)
            await asyncio.sleep(sleep_time)
        except discord.errors.NotFound:
            print('Message deleted. Creating new one...')
            message = await neko.send_message(channel, text)
            config.set('svupdate', 'messages', message.id)
            with open(configfile, 'w') as f: config.write(f)
        except discord.errors.HTTPException:
            print('HTTP exception occured during server list update.')
            await asyncio.sleep(60)
        except Exception as e:
            print('Exception while editing server message update: ', e)

@neko.event
async def on_ready():
    print('Logged in as', neko.user.name)

@neko.event
async def on_member_join(member):
    channel = neko.get_channel(ch_general)
    info_channel = neko.get_channel(ch_info)
    text = 'Welcome to the ' + channel.server.name + ' server, ' \
            + member.mention + '! Check out the ' + info_channel.mention \
            + ' channel.\n' + 'Official OpenArena game download: ' \
            + '<http://openarena.ws/download.php?view.4>'

    try:
        await neko.send_message(channel, text)
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
            if message2.author.id == owner:
                if message2.content == '.shutdown' or message2.content == '.s':
                    await neko.edit_message(message, '-')
                    neko.logout()
                    sys.exit()
    except Exception as e:
        print('Error while executing command\n', e)

# create tasks and run main loop
try:
    neko.loop.create_task(sv_update())
    neko.run(token)
except Exception as e:
    print('Error in the main loop:\n', e)
