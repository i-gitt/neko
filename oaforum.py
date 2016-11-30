from os import environ
from re import sub
from lxml import etree
import time
import configparser

def parse_html(string):
    html_chars = {'&quot;': '"', '&#39;': "'", '&lt;': '<', '&gt;': '>',
            '&amp;': '&', '<br />': '\n' }
            # '<b>': '**', '</b>': '**', '<i>': '_', '</i>': '_'

    for i, j in html_chars.items():
        string = string.replace(i, j)

    # TODO: add emoji
    string = sub(r'</div>', '</div>\n', string)
    string = sub(r'&[^;]*;', '', string)
    string = sub(r'<[^>]*>', '', string.strip())

    return string

def remove_namespace(tree):
    for _, el in tree:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

def feed():
    config = configparser.ConfigParser()
    config.read('neko_test.ini')
    last_id = config['Messages']['oaforum']
    if last_id:
        last_id = int(last_id)

    tree = None
    try:
        tree = etree.parse('http://openarena.ws/board/index.php?action=.xml')
        remove_namespace(etree.iterwalk(tree))
        #  tree = etree.iterparse('test/oaforum.xml') # DEBUG
    except:
        print('Error loading forum page.')
        return

    environ['TZ'] = 'US/Central'
    time.tzset()
    messages = []
    for post in reversed(tree.xpath('//recent-post')):
        post_id = int(post.xpath('./id/text()')[0])
        try:
            if last_id and post_id > last_id:
                board = post.xpath('./board/name/text()')[0]
                topic = post.xpath('./topic/subject/text()')[0]
                poster = post.xpath('./poster/name/text()')[0]
                post_time = post.xpath('./time/text()')[0]
                link = post.xpath('./link/text()')[0]
                body = post.xpath('./body/text()')[0]

                if board == 'Development':
                    board = ':wrench: ' + board
                elif board == 'Maps':
                    board = ':triangular_flag_on_post:' + board
                elif board == 'Idea pit':
                    board = ':pencil:' + board

                post_time = post_time.replace('Today at',
                        time.strftime('%B %d, %Y'))

                message = ('[' + board + '] **' + topic + '**\n'
                    'by _' + poster + '_ on ' + post_time + '\n'
                    '<' + link + '>\n'
                    '```\n' + parse_html(body) + '\n```')
                messages.append(message)
        except:
            print('Error reading feed messages.')
            return

    config.set('Messages', 'oaforum', tree.xpath(
        '//recent-post[not(../recent-post/id > id)]/id/text()')[0])
    last_id = config['Messages']['oaforum']
    with open('neko_test.ini', 'w') as file:
        config.write(file)

    return messages
