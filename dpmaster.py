#!/usr/bin/python

from requests import get
from lxml import etree

class Server:
    pass

def escape_chars(string):
    rep_chr = {'&quot;': '"', '&#39;': "'", '&lt;': '<', '&gt;': '>',
            '&amp;': '&', '*': '\\*', '_': '\\_', '~': '\\~', '`': '\\`'}
    for i, j in rep_chr.items():
        string = string.replace(i, j)
    return string.strip()

def sv_list():
    page = None
    try:
        url = 'http://dpmaster.deathmask.net'
        params = {'game': 'openarena', 'xml': '1', 'nocolors': '1'}
        page = get(url, params).content
    except:
        #  print('Error loading dpmaster page.')
        return

    tree = None
    try:
        tree = etree.fromstring(page)
        #  tree = etree.parse('test/dpmaster.xml') # DEBUG
    except:
        print('Error while parsing xml.')
        return

    servers = []
    human = 'player[ping/text()!=0]'
    for server in tree.xpath('//server[count(players/%s) > 0]' % human):
        sv = Server()
        try:
            sv.name = escape_chars(server.xpath('./name/text()')[0])
            sv.hostname = escape_chars(server.xpath('./hostname/text()')[0])
            sv.map = escape_chars(server.xpath('./map/text()')[0])
            sv.players = [escape_chars(x) for x in
                    server.xpath('.//%s/name/text()' % human)[:]]
        except:
            print('Error in xml, missing information.')
            return
        servers.append(sv)
    servers = sorted(servers, key=lambda sv: len(sv.players), reverse=True)

    player_count = 0
    for sv in servers:
        player_count += len(sv.players)
    message = 'OpenArena server list ({} players)\n\n'.format(player_count)
    hidden_sv = 0
    for sv in servers:
        new_msg = '**{}** ({}) [{}]\n'.format(sv.name, sv.hostname, sv.map)
        new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join(sv.players))
        if (len(message + new_msg) < 1970):
            message += new_msg
        else:
            hidden_sv += 1
    if hidden_sv:
        message += '+{} servers with players'.format(hidden_sv)
    return message

#  print(sv_list())
