#!/usr/bin/python

import asyncio
from config import config
import discord
import dpmaster
import stats

async def sv_update(neko):
    await neko.wait_until_ready()

    global message
    message = None
    channel = neko.get_channel(ch_svlist)
    if message_id:
        #  print('Message (ID={}) already exists.'.format(message_id))
        try:
            message = await neko.get_message(channel, message_id)
        except:
            print('Couldn\'t retrieve message with id={}'.format(message_id))

    if not message:
        try:
            print('Creating new message for server list...')
            text = dpmaster.sv_list(True)
            stats.Save()
            if not text: text = '-'
            message = await neko.send_message(channel, text)
            config.set('svupdate', 'message', message.id)
            with open(configfile, 'w') as f: config.write(f)
        except Exception as e:
            print('Error creating new message: ', e)

    while not neko.is_closed:
        try:
            text = dpmaster.sv_list()
            if not text: text = '-'
            await neko.edit_message(message, text)
            await asyncio.sleep(sleep_time)
        except discord.errors.NotFound:
            print('Message deleted. Creating new one...')
            message = await neko.send_message(channel, text)
            config.set('svupdate', 'message', message.id)
            with open(configfile, 'w') as f: config.write(f)
        except discord.errors.HTTPException:
            print('HTTP exception occured during server list update.')
            await asyncio.sleep(60)
        except Exception as e:
            print('Exception while editing server message update: ', e)
            #  break
