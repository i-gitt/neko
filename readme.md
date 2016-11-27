Neko
====

Neko is a Discord bot for OpenArena server. Currently it only displays
OpenArena server list and players, and performs some usual functions found in
other Discord bots.

You can find info about the OpenArena game at http://www.openarena.ws. To join
the Discord server you can use this invite link: https://discord.me/openarena.

Running
-------

Use the `run.sh` script.

Requirements
------------

- python 3.5

These are Python packages, already included with pip into venv directory,
together with their dependencies:

- lxml -- http://lxml.de
- requests -- http://docs.python-requests.org/en/master
- discord.py -- https://github.com/Rapptz/discord.py

Testing
-------

To test this bot on your own Discord server:

- go to https://discordapp.com/developers/applications/me and
  choose `New Applicatons`
- name the bot, choose `Create Application`
- choose `Create a Bot User`
- uncheck the `Public Bot` (recommended)
- under `APP BOT USER` click on the reveal token. Use this token with
  config.ini file.
- Create a discord server and invite the bot with this link (replace
  Client_ID with your bot Client ID):
  https://discordapp.com/oauth2/authorize?client_id=Client_ID&scope=bot&permissions=0
- copy channel ID's to config.ini (they can be found on web app by choosing
  a channel on your Discord server and looking at the link
  https://discordapp.com/channels/<server_id>/<channel_id>)
- run the app
