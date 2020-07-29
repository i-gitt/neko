import configparser

config = configparser.ConfigParser()
config.read('neko.ini')

token = config['neko']['token']
svlist_channel = int(config['neko']['server_list_channel'])
svlist_sleep_time = int(config['neko']['server_list_sleep_time'])
