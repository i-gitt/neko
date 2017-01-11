import configparser

configfile = 'neko.ini'
config = configparser.ConfigParser()
config.read(configfile)

token = config['neko']['token']
owner = config['neko']['owner']
ch_general = config['neko']['general']
ch_info = config['neko']['info']
ch_svlist  = config['svupdate']['channel']
sv_msg_id = config['svupdate']['message']
sleep_time = int(config['svupdate']['sleep'])
