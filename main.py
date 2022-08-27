######################################################### IMPORTS
import threading
import subprocess
import ctypes
import os
import sys
import time
import math
import colorama
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import datetime
import platform
import wieprint as print
import tempfile
import requests
from PIL import Image
######################################################### END OF IMPORTS

######################################################### VARIABLES
timestarted = math.floor(time.time())
######################################################### END OF VARIABLES

######################################################### FUNCTIONS
def isAdmin():
    # Return:
    # WinNT w/ admin - True
    # WinNT wo/ admin - False
    # Linux - None
    if 'nt' in os.name:
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return None

def format_time(time):
    # Expected: <INT> - nr of secs
    # Return: hh:mm:ss
    seconds = time % 60
    minutes = math.floor((time % 3600) / 60)
    hours = math.floor((time % 21600) / 3600)
    
    strsec = str(seconds)
    strmin = str(minutes)
    strhor = str(hours)

    if(len(strhor) == 1):
        strhor = "0" + strhor
    if(len(strmin) == 1):
        strmin = "0" + strmin
    if(len(strsec) == 1):
        strsec = "0" + strsec
    
    return strhor + ":" + strmin + ":" + strsec

def sfcSN():
    output = subprocess.Popen("sfc /scannow", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scanstart = math.floor(time.time())
    for line in iter(output.stdout.readline, b''):
        form = line
    print.info("Analyzing...")
    # Analyze variables
    cantrepair, repair, repaircorrupted = 0, 0, 0
    entrycr, entryr, entryrc = "Cannot repair member file", "Repaired file", "Repairing corrupted file"
    # Logs from "sfc /scannow"
    with open("C:/Windows/Logs/CBS/CBS.log", "r") as read:
        ### https://docs.microsoft.com/en-us/troubleshoot/windows-client/deployment/analyze-sfc-program-log-file-entries
        today = datetime.date.today()
        for x in read.readlines():
            if ( x in str(today.strftime("%Y-%m-%d")) ):
                if( entrycr in x ):
                    cantrepair = cantrepair + 1
                    with open("cannot_fix_sfc.log", "a") as append:
                        append.write(print.ttToReturn("CRITICAL", "Program can't fix " + x.replace(entrycr + " ", "")))
                if( entryr in x ):
                    repair = repair + 1
                if( entryrc in x ):
                    repaircorrupted = repaircorrupted + 1
    print.info("Time spent " + format_time(math.floor(time.time()) - scanstart))

def dismCH():
    output = subprocess.Popen("DISM /Online /Cleanup-Image /CheckHealth", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scanstart = math.floor(time.time())
    for line in iter(output.stdout.readline, b''):
        form = line
    print.info("Time spent " + format_time(math.floor(time.time()) - scanstart))

def dismSH():
    output = subprocess.Popen("DISM /Online /Cleanup-Image /ScanHealth", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scanstart = math.floor(time.time())
    for line in iter(output.stdout.readline, b''):
        form = line
    print.info("Time spent " + format_time(math.floor(time.time()) - scanstart))

def dismRH():
    file = filedialog.askopenfilename(initialdir="/", title="Open file", filetypes = [("install.wim with " + platform.system() + " " + platform.release(), ".wim")])
    for x in range(3):
        print.critical("IS THIS FILE CORRECT? (wrong wim file can chance with destroying computer)" + file)
    print.critical("(Y/n)")
    if(str(input()).lower() != "y"):
        return
    output = subprocess.Popen("DISM /Online /Cleanup-Image /RestoreHealth /Source:" + file, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scanstart = math.floor(time.time())
    for line in iter(output.stdout.readline, b''):
        form = line
    print.info("Time spent " + format_time(math.floor(time.time()) - scanstart))

def sysRestore():
    os.system("rstrui.exe")

def launch_sys_res():
    if ( isAdmin() == True ):
        print.ok("Starting System Restore")
        threading.Thread(target=sysRestore, daemon=True).start()
    elif ( isAdmin() == None ):
        print.critical("Can't run prob. Linux")

def launch_dism_rh():
    if ( isAdmin() == True ):
        print.ok("Starting DISM")
        threading.Thread(target=dismRH, daemon=True).start()
    elif ( isAdmin() == False ):
        print.warning("Can't run - no admin rights!")
        threading.Thread(target=dismRH, daemon=True).start()
    elif ( isAdmin() == None ):
        print.critical("Can't run prob. Linux")

def launch_dism_sh():
    if ( isAdmin() == True ):
        print.ok("Starting DISM")
        threading.Thread(target=dismSH, daemon=True).start()
    elif ( isAdmin() == False ):
        print.warning("Can't run - no admin rights!")
        threading.Thread(target=dismSH, daemon=True).start()
    elif ( isAdmin() == None ):
        print.critical("Can't run prob. Linux")

def launch_dism_ch():
    if ( isAdmin() == True ):
        print.ok("Starting DISM")
        threading.Thread(target=dismCH, daemon=True).start()
    elif ( isAdmin() == False ):
        print.warning("Can't run - no admin rights!")
        threading.Thread(target=dismCH, daemon=True).start()
    elif ( isAdmin() == None ):
        print.critical("Can't run prob. Linux")

def launch_sfc():
    if ( isAdmin() == True ):
        print.ok("Starting SFC")
        threading.Thread(target=sfcSN, daemon=True).start()
    elif ( isAdmin() == False ):
        print.warning("Can't run - no admin rights!")
        threading.Thread(target=sfcSN, daemon=True).start()
    elif ( isAdmin() == None ):
        print.critical("Can't run prob. Linux")
######################################################### END OF FUNCTIONS

######################################################### MAIN SCRIPT

# TKinter
root = Tk()
root.geometry('300x400')
root.title('Wixer - aka. Windows Fixer')

canvas = Canvas(root, width = 200, height = 200)
canvas.pack()
a = requests.get("https://static.wikia.nocookie.net/logopedia/images/9/9f/Windows_Installer_icon_%28Windows_11%29.png/revision/latest?cb=20210620182947")
with open(os.path.join(tempfile.gettempdir(), "t.png"), "wb") as t:
    t.write(a.content)
    t.close()
img = Image.open(os.path.join(tempfile.gettempdir(), "t.png"))
img_resize = img.resize((156, 156))
img_resize.save(os.path.join(tempfile.gettempdir(), "t.png"))
img2 = PhotoImage(file=os.path.join(tempfile.gettempdir(), "t.png"))
canvas.create_image(20,20, anchor=NW, image=img2)

lab = Label(text="Wixer")
lab.config(font=("Courier", 16))
lab.pack(side="top") 

but = Button(text="Launch SFC", command=lambda: launch_sfc())
but.pack(side="top")
but = Button(text="Launch DISM CheckHealth", command=lambda: launch_dism_ch())
but.pack(side="top")
but = Button(text="Launch DISM ScanHealth", command=lambda: launch_dism_sh())
but.pack(side="top")
but = Button(text="Launch DISM RestoreHealth (need install.wim)", command=lambda: launch_dism_rh())
but.pack(side="top")
but = Button(text="Launch System Restore", command=lambda: launch_sys_res())
but.pack(side="top")
but = Button(text="Exit", command=lambda: exit())
but.pack(side="top")

lab = Label(master=root, text="BombelekWare 2022")
lab.pack(side='bottom')

root.mainloop()

########################################################## END OF MAIN SCRIPT