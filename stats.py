#TODO: add alias method to merge different nicknames into one, not exposed as a bot command
#TODO: add exclusion method to skip particular nicknames (e.g. UnnamedPlayer), not exposed as a bot command

import pickle
from datetime import datetime, date, time, timedelta
from collections import OrderedDict
import itertools
from threading import Lock
import shutil

# 100 players are <5Kb
# 1M players should be safely less than 50Mb
# 10K players should be safely less than 500Kb
# 2K players should be around 100Kb
MAX_NUM_PLAYERS = 4000
MAX_QUERY_RESULTS = 50

# players = OrderedDict([('player1_name', player1_timestamp), ..., ('playerN_name', playerN_timestamp)])
players = OrderedDict()

# online servers = dict[('sv1_name', sv1_info), ..., ('svN_name', svN_info)]
servers = dict()

# thread safety
_LOCK = Lock()

# possibly for a smarter search
smart_chars = dict({'4':'a', '^':'a', '@':'a', \
                    '6':'b', '8':'b', \
                    '(':'c', '<':'c', \
                    '3':'e', \
                    '9':'g', \
                    '1':'i', '!':'i', '|':'i', ':':'i', '\'':'i', \
                    '\\':'l', '/':'l', \
                    '0':'o', '*':'o', '#':'o', \
                    '5':'s', \
                    '7':'t', '+':'t', \
                    '2':'z'})
def smart_string(string):
    if len(string) < 2:
        return string
    smarter_string = string.upper().lower()
    for i, c in enumerate(smarter_string):
        if c in smart_chars:
            smarter_string = smarter_string[:i] + smart_chars[c] + smarter_string[(i+1):]
    return smarter_string

# load previously saved data
def Load():
    global players
    bak_size = 0
    this_size = 0
    try:
        with open('stats.pickle.bak', 'rb') as f:
            f.seek(0, 2)
            bak_size = f.tell()
    except FileNotFoundError:
        pass
    try:
        with open('stats.pickle', 'rb') as f:
            f.seek(0, 2)
            this_size = f.tell()
    except FileNotFoundError:
        pass
    try:
        loadfn = 'stats.pickle'
        if this_size < round(0.5 * bak_size):
            # mmm... something is wrong
            loadfn = 'stats.pickle.bak'
        else:
            # backup
            try:
                shutil.copy2('stats.pickle', 'stats.pickle.bak')
            except Exception as exb:
                print(exb)
        with open(loadfn, 'rb') as f:
            players = pickle.load(f)
    except Exception as ex:
        print(ex)

# save current available data
def Save():
    global _LOCK
    _LOCK.acquire(blocking=True, timeout=-1)
    try:
        with open('stats.pickle', 'wb') as f:
            pickle.dump(players, f)
        _LOCK.release()
    except Exception as ex:
        _LOCK.release()
        print(ex)

# clear all stats
def Clear():
    global players
    try:
        players = OrderedDict()
    except Exception as ex:
        print(ex)

# update stats with current dpmaster servers list
def Update(dpmaster_servers):
    global _LOCK
    global servers
    global players
    _LOCK.acquire(blocking=True, timeout=-1)
    try:
        #c = 0
        for sv in dpmaster_servers:
            if len(sv.players) == 1:
                plinfo = 'player'
            else:
                plinfo = 'players'
            players_list = ''
            if len(sv.players) > 0:
                players_list += ': {}'.format(sv.players[0])
                for p in sv.players[1:]:
                    players_list += ' *|* {}'.format(p)
            servers[sv.name] = ' ({}) [{}] has `{}` {}{}'.format(sv.hostname, sv.map, len(sv.players), plinfo, players_list)
            # limit loop?
            #c += len(sv.players)
            #if c < MAX_NUM_PLAYERS:
            for player in sv.players:
                try:
                    players[player] = datetime.utcnow()
                except:
                    pass
        # limit by keeping only the most recently seen players
        players_sorted = OrderedDict(sorted(players.items(), key=lambda t: t[1], reverse=True))
        players = OrderedDict(itertools.islice(players_sorted.items(), MAX_NUM_PLAYERS))
        _LOCK.release()
    except Exception as ex:
        _LOCK.release()
        print(ex)

# query players timestamps
def QueryTimestamps(search_string):
    global _LOCK
    message = ''
    try:
        filtered = OrderedDict()
        ss = smart_string(search_string)
        _LOCK.acquire(blocking=True, timeout=-1)
        try:
            for n, t in players.items():
                sn = smart_string(n)
                if ss in sn:
                    filtered[n] = t
        except:
            _LOCK.release()
            return ''
        _LOCK.release()
        # case-insensitive alphabetical order
        filtered_sorted = OrderedDict(sorted(filtered.items(), key=lambda col: col[0].upper().lower()))
        # show only first MAX_QUERY_RESULTS
        num_shown = 0
        for n, t in itertools.islice(filtered_sorted.items(), MAX_QUERY_RESULTS):
            ts = filtered[n].strftime('%d %b %Y %H:%M:%S')
            message_part = '**{}** last seen on {} (UTC)\n'.format(n, ts)
            if len(message_part) + len(message) > 1970:
                break;
            message += message_part
            num_shown += 1
        num_notshown = len(filtered) - num_shown
        if num_notshown > 0:
            message += '*and {} more...*\n'.format(num_notshown)
    except Exception as ex:
        print(ex)
        return ''
    return message

# query number of players in time range
def QueryTimerange(search_timedelta=timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)):
    global _LOCK
    message = ''
    try:
        c = 0
        _LOCK.acquire(blocking=True, timeout=-1)
        try:
            for n, t in players.items():
                if datetime.utcnow() - t <= search_timedelta:
                    c += 1
        except:
            _LOCK.release()
            return ''
        _LOCK.release()
        message = '>> `{}` players in the last '.format(c)
        secs = round(search_timedelta.total_seconds())
        mins = round(secs / 60)
        hours = round(mins / 60)
        days = round(hours / 24)
        if hours < 1:
            if mins < 2:
                message += 'minute\n'
            else:
                message += '{} minutes\n'.format(mins)
        elif days < 2:
            if hours < 2:
                message += 'hour\n'
            else:
                message += '{} hours\n'.format(hours)
        else:
            message += '{} days\n'.format(days)
    except Exception as ex:
        print(ex)
        return ''
    return message

# query server name
def QueryServers(search_string):
    global _LOCK
    message = ''
    try:
        filtered = OrderedDict()
        ss = smart_string(search_string)
        _LOCK.acquire(blocking=True, timeout=-1)
        try:
            for n, i in servers.items():
                sn = smart_string(n)
                if ss in sn:
                    filtered[n] = i
        except:
            _LOCK.release()
            return ''
        _LOCK.release()
        # case-insensitive alphabetical order
        filtered_sorted = OrderedDict(sorted(filtered.items(), key=lambda col: col[0].upper().lower()))
        # show only first MAX_QUERY_RESULTS
        num_shown = 0
        for n, i in itertools.islice(filtered_sorted.items(), MAX_QUERY_RESULTS):
            message_part = '**{}**{}\n'.format(n, i)
            if len(message_part) + len(message) > 1970:
                break;
            message += message_part
            num_shown += 1
        num_notshown = len(filtered) - num_shown
        if num_notshown > 0:
            message += '*and {} more...*\n'.format(num_notshown)
    except Exception as ex:
        print(ex)
        return ''
    return message

# print current stats
def Print():
    try:
        for n, t in players.items():
            print('{}:\t{}'.format(n, t.strftime('%d %b %Y %H:%M:%S')))
    except Exception as ex:
        print(ex)
