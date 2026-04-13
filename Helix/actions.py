import os
import ctypes
import subprocess
import webbrowser
import pyautogui
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
import shutil
import urllib.parse
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def open_site(site, query=None):
    site = site.lower().strip()

    domains = {
        "youtube": "youtube.com",
        "google": "google.com",
        "wikipedia": "wikipedia.org",
        "spotify": "open.spotify.com",
        "pinterest": "pinterest.com",
        "amazon": "amazon.in",
        "github": "github.com"
    }

    domain = domains.get(site, f"{site}.com")

    if query:
        q = urllib.parse.quote(query)
        url = f"https://{domain}/search?q={q}"
    else:
        url = f"https://{domain}"

    webbrowser.open(url)

def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information not available."

    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        return f"Battery is at {percent} percent and charging."
    else:
        return f"Battery is at {percent} percent and not charging."


def set_volume(percent):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)


def volume_up():
    pyautogui.press("volumeup")


def volume_down():
    pyautogui.press("volumedown")


def lock_pc():
    ctypes.windll.user32.LockWorkStation()


def shutdown_pc():
    os.system("shutdown /s /t 5")


def take_screenshot():
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"screenshot_{name}.png"
    pyautogui.screenshot(path)
    return path


def open_app(app_name):
    try:
        subprocess.Popen(app_name)
    except:
        os.system(f"start {app_name}")

def close_app(app_name):
    app_name = app_name.lower()

    closed = False

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()

            if app_name in name:
                proc.kill()
                closed = True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return closed


def app_exists(app):
    return shutil.which(app) is not None


def open_anything(name):
    if app_exists(name):
        os.system(f"start {name}")
        return "app"

    if "." not in name:
        url = f"https://www.google.com/search?q={name}"
    else:
        url = f"https://{name}"

    webbrowser.open(url)
    return "web"