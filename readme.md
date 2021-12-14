Neko
====

Neko is a Discord bot for OpenArena server. Currently it only displays
OpenArena server list and players, and performs some usual functions found in
other Discord bots.

You can find info about the OpenArena game at http://www.openarena.ws. To join
the Discord server you can use this invite link: https://discord.me/openarena.

This version includes Code of https://github.com/rdntcntrl/oaquery.

Running since 12/2021 on #servers in the Official Open Arena Discord 
https://discord.gg/n3dTmzM

Setup
-----

Run the `install.sh` script to download required files (discord.py).
Use the `neko.service` to run with `systemd` or run.sh

Requirements
------------

- discord.py -- https://github.com/Rapptz/discord.py

Testing
-------

To test this bot on your own Discord server:

- create a `New Application` at https://discord.com/developers/applications
- choose `Create a Bot User`
- uncheck the `Public Bot` (recommended)
- under Bot click on the reveal token. Use this token with neko.ini file.
- Create a discord server and invite the bot with this link (replace
  Client_ID with your bot Client ID):
  https://discordapp.com/oauth2/authorize?client_id=Client_ID&scope=bot&permissions=0
- copy channel ID's to neko.ini (they can be found on web app by choosing
  a channel on your Discord server and looking at the link
  https://discordapp.com/channels/<server_id>/<channel_id>)
- run the app
