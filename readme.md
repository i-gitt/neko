Neko
====

Neko is a Discord bot for OpenArena server. Currently it only displays
OpenArena server list and players, and performs some usual functions found in
other Discord bots.

You can find info about the OpenArena game at http://www.openarena.ws. To join
the Discord server you can use this invite link: https://discord.me/openarena.

Setup
-----

Run the `install.sh` script to download and build `qstat`. Use the
`neko.service` to run with `systemd`.

Requirements
------------

- discord.py -- https://github.com/Rapptz/discord.py
- qstat -- https://github.com/multiplay/qstat

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
