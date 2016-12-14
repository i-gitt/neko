Neko
====

Neko is a Discord bot for OpenArena server. It displays OpenArena server list
information and and keeps statistics of players.

You can find info about the OpenArena game at http://www.openarena.ws.

Running
-------

To run the program you need to create a Python virtual environment and install
necessary libraries with pip.

Commands
--------

Neko accepts the following commands in private chat:

.seen <str> -- shows when a player(s) last appeared in game that contain <str>
in their name

.sv <str> -- find running servers that contain <str> in their name


Requirements
------------

- python >3.5
- discord.py -- https://github.com/Rapptz/discord.py
- lxml -- http://lxml.de

Testing
-------

To test this bot on your own Discord server create a new bot and invite it to
your own server.
