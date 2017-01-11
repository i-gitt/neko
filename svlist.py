#!/usr/bin/python

import asyncio
import config
import discord
import dpmaster
import stats

# global message so we can erase it on shutdown
message = None

async def sv_update(neko):
    await neko.wait_until_ready()

    global message
    channel = neko.get_channel(config.ch_svlist)
    if config.sv_msg_id:
        #  print('Message (ID={}) already exists.'.format(config.sv_msg_id))
        try:
            message = await neko.get_message(channel, config.sv_msg_id)
        except:
            print('Couldn\'t retrieve message with id={}'.format(config.sv_msg_id))

    if not message:
        try:
            print('Creating new message for server list...')
            text = dpmaster.sv_list()
            stats.Save()
            if not text: text = '-'
            message = await neko.send_message(channel, text)
            config.config.set('svupdate', 'message', message.id)
            with open(config.configfile, 'w') as f: config.config.write(f)
        except Exception as e:
            print('Error creating new message: ', e)

    while not neko.is_closed:
        try:
            text = dpmaster.sv_list()
            if not text: text = '-'
            await neko.edit_message(message, text)
            await asyncio.sleep(config.sleep_time)
        except discord.errors.NotFound:
            print('Message deleted. Creating new one...')
            message = await neko.send_message(channel, text)
            config.set('svupdate', 'message', message.id)
            with open(config.configfile, 'w') as f: config.config.write(f)
        except discord.errors.HTTPException:
            print('HTTP exception occured during server list update.')
            await asyncio.sleep(config.sleep_time)
        except Exception as e:
            print('Exception while editing server message update: ', e)
            #  break
