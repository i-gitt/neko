from lxml import etree
import stats

class Server:
    pass

def escape_chars(string):
    if not string: return
    rep_chr = {'&quot;': '"', '&#39;': "'", '&lt;': '<', '&gt;': '>',
            '&amp;': '&', '*': '\\*', '_': '\\_', '~': '\\~', '`': '\\`'}
    for i, j in rep_chr.items():
        string = string.replace(i, j)
    return string.strip()

def sv_list(track_players = False):
    tree = None
    try:
        url = 'http://dpmaster.deathmask.net/?game=openarena&xml=1&nocolors=1'
        tree = etree.parse(url)
        #  tree = etree.parse('test/dpmaster.xml') # DEBUG
    except: return

    servers = []
    for server in tree.xpath('//server'):
        sv = Server()
        try:
            sv.hostname = escape_chars(server.findtext('./hostname'))
            if not sv.hostname: continue
            sv.name = escape_chars(server.findtext('./name'))
            sv.map = escape_chars(server.findtext('./map'))

            if server.find('./players/player') is not None:
                sv.players = [escape_chars(x) for x in server.xpath(
                    './players/player[ping/text()!=0]/name/text()')]
            else: sv.players = []

        except Exception as e:
            print('Error in xml: ', e)
            return

        servers.append(sv)

    servers = sorted(servers, key=lambda sv: len(sv.players), reverse=True)

    if track_players: stats.Update(servers)

    message = '\n__ **OpenArena** server list (*{}*  players online) __\n\n' \
            .format(sum([len(sv.players) for sv in servers]))

    hidden_sv = 0

    for sv in (sv for sv in servers if sv.players):
        new_msg = '**{}** ({}) [map: {}] has `{}` player{}:\n'.format(sv.name,
                sv.hostname, sv.map, len(sv.players),
                's' if len(sv.players) > 1 else '')
        new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join(sv.players))

        if (len(message + new_msg) < 1970): message += new_msg
        else: hidden_sv += 1

    if hidden_sv: message += '+{} server(s) with players'.format(hidden_sv)

    return message
