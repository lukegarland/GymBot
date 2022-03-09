# GymBot®
from __future__ import print_function
import os.path
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Iac01Bot import Iac01Bot
import signal
import sys
from GymBotGUI import GymBotGUI
import datetime
from Calendar import Calendar
from os import path
from tkinter import PhotoImage
from Settings import Settings

version = "v0.25"

OS = platform.system()
if OS == "Windows":
    from win10toast import ToastNotifier


def signal_handler(sig, frame):
    driver.quit()
    gui.exit_all()
    pass


if getattr(sys, 'frozen', False):  # Running as compiled
    running_dir = sys._MEIPASS + "/files/"  # Same path name than pyinstaller option
else:
    running_dir = "./"  # Path name when run with Python interpreter

# Define paths
if OS == "Windows":
    localPath = path.expandvars(r'%LOCALAPPDATA%\GymBot') + '\\'
else:
    localPath = os.path.join(path.expanduser("~"), ".GymBot")

iconFileName = running_dir + 'GymBot.ico'
pngFileName = running_dir + 'GymBot.png'
lightFileName = running_dir + 'GymBot_light.png'
darkFileName = running_dir + 'GymBot_dark.png'

if OS == "Linux":
    driverFileName = running_dir + 'chromedriver_linux64'
elif OS == "Darwin":
    driverFileName = running_dir + 'chromedriver_mac64'
else:
    driverFileName = running_dir + 'chromedriver.exe'

credsFileName = running_dir + 'credentials.json'
tokenFileName = localPath + 'GymBotToken.json'
configFileName = localPath + 'GymBotUserConfig.json'
login_url = "https://iac01.ucalgary.ca/CamRecWebBooking/Login.aspx"
default_url = "https://iac01.ucalgary.ca/CamRecWebBooking/default.aspx"

if not os.path.exists(localPath):
    os.makedirs(localPath)

if __name__ == "__main__":
    print(f"GymBot® {version}")

    # Define objects
    ser = Service(driverFileName)
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument('--log-level=3')
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ser, options=op)  # webdriver
    iac01bot = Iac01Bot(driver)                         # iac01bot
    iac01bot.login_url = login_url                      # iac01bot: login url
    iac01bot.default_url = default_url                  # iac01bot: default url
    signal.signal(signal.SIGINT, signal_handler)        # signal handler
    settings = Settings(version)                        # settings
    settings.config_path = configFileName               # settings: config
    calendar = Calendar(settings)                       # calendar
    calendar.credsFileName = credsFileName              # calendar: credentials
    calendar.tokenFileName = tokenFileName              # calendar: token
    settings = Settings(version)                        # settings
    settings.config_path = configFileName               # settings: config

    if OS == "Windows":
        toaster = ToastNotifier()                       # notifier
        toaster.icon = iconFileName                     # notifier: icon
        gui = GymBotGUI(iac01bot,                       # interface
                        calendar,
                        settings,
                        toaster=toaster)
    else:
        gui = GymBotGUI(iac01bot,                       # interface
                        calendar,
                        settings)

    gui.icon_photo = PhotoImage(file=pngFileName)       # interface: png
    gui.light_photo = PhotoImage(file=lightFileName)    # interface: light png
    gui.dark_photo = PhotoImage(file=darkFileName)      # interface: dark png

    # Version check for local data
    settings.version_check()

    # Start process
    gui.set_theme_mode()
    gui.create_main_window()

    # Cleanup
    driver.quit()
    gui.exit_all()
