import configparser

try:
    configfile = 'neko_test.ini'
    config = configparser.ConfigParser()
    config.read(configfile)

    token = config['neko']['token']
    ch_general = config['neko']['general']
    ch_svlist  = config['svupdate']['channel']
    sv_msg_ids = config['svupdate']['messages']
    sleep_time = int(config['svupdate']['sleep'])
except Exception as e:
    raise('Error loading config: ', e)
