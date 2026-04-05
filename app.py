import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import json
import urllib.parse
import sqlite3
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

# ────────────────────────────────────────────────
# DATABASE SYSTEM
# ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, 
                  chat_id TEXT, name_prefix TEXT, delay INTEGER, cookies TEXT, messages TEXT, 
                  is_running BOOLEAN)''')
    conn.commit()
    conn.close()

class Database:
    @staticmethod
    def create_user(username, password):
        try:
            conn = sqlite3.connect('users.db', check_same_thread=False)
            c = conn.cursor()
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users (username, password, chat_id, name_prefix, delay, cookies, messages, is_running) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (username, hashed_pw, '', '', 5, '', '', False))
            conn.commit()
            return True, "Account created!"
        except:
            return False, "Username already exists!"

    @staticmethod
    def verify_user(username, password):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_pw))
        result = c.fetchone()
        return result[0] if result else None

    @staticmethod
    def get_user_config(user_id):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = c.fetchone()
        return dict(row) if row else None

    @staticmethod
    def update_user_config(user_id, chat_id, prefix, delay, cookies, messages):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET chat_id=?, name_prefix=?, delay=?, cookies=?, messages=? WHERE id=?",
                  (chat_id, prefix, delay, cookies, messages, user_id))
        conn.commit()

    @staticmethod
    def set_automation_running(user_id, status):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("UPDATE users SET is_running=? WHERE id=?", (status, user_id))
        conn.commit()

    @staticmethod
    def get_automation_running(user_id):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT is_running FROM users WHERE id=?", (user_id,))
        res = c.fetchone()
        return res[0] if res else False

init_db()
db = Database()

# ────────────────────────────────────────────────
# SETTINGS & THEME
# ────────────────────────────────────────────────
ADMIN_PASSWORD = "Rkraja"
MY_NUMBER = "60143153573" # Aapka Updated Number
TELEGRAM_BOT_TOKEN = "8782762466:AAGh2AOb7Cj2EdG09_sD-graYMzeN4LNm88"

st.set_page_config(page_title="E2E ⚜️9MAN⚜️", page_icon="👑", layout="wide")

# (CSS for Royal Theme)
st.markdown("""
<style>
    .stApp { background: #1a0033; color: #ffd700; }
    .main-header { text-align: center; border: 2px solid #ffd700; border-radius: 20px; padding: 20px; background: #2a0055; }
    .stButton>button { background: linear-gradient(45deg, #b8860b, #ffd700); color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# AUTOMATION ENGINE
# ────────────────────────────────────────────────
def run_fb_automation(config, state, user_id):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.facebook.com")
        # Add Cookies
        if config['cookies']:
            for c in config['cookies'].split(';'):
                if '=' in c:
                    name, val = c.strip().split('=', 1)
                    driver.add_cookie({'name': name, 'value': val, 'domain': '.facebook.com'})
        
        driver.get(f"https://www.facebook.com/messages/t/{config['chat_id']}")
        time.sleep(8)
        
        msgs = [m.strip() for m in config['messages'].split('\n') if m.strip()]
        i = 0
        while state.running:
            text = f"{config['name_prefix']} {msgs[i % len(msgs)]}"
            driver.execute_script("let e = document.querySelector('div[role=\"textbox\"]'); if(e){ e.focus(); document.execCommand('insertText', false, arguments[0]); }", text)
            time.sleep(1)
            driver.execute_script("let b = document.querySelector('div[aria-label=\"Press enter to send\"]'); if(b) b.click();")
            
            state.message_count += 1
            i += 1
            time.sleep(config['delay'])
    except Exception as e:
        state.logs.append(f"Error: {str(e)}")
    finally:
        driver.quit()
        state.running = False
        db.set_automation_running(user_id, False)

# ────────────────────────────────────────────────
# UI LOGIC
# ────────────────────────────────────────────────
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'state' not in st.session_state:
    st.session_state.state = type('obj', (object,), {'running': False, 'message_count': 0, 'logs': []})

def main():
    if not st.session_state.logged_in:
        st.markdown("<div class='main-header'><h1>👑 ROYAL LOGIN 👑</h1></div>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            uid = db.verify_user(u, p)
            if uid:
                st.session_state.logged_in, st.session_state.uid, st.session_state.user = True, uid, u
                st.rerun()
    else:
        st.sidebar.write(f"Welcome, {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        config = db.get_user_config(st.session_state.uid)
        t1, t2 = st.tabs(["Settings", "Control"])
        
        with t1:
            cid = st.text_input("Target Chat ID", value=config['chat_id'])
            pre = st.text_input("Prefix", value=config['name_prefix'])
            dly = st.number_input("Delay", value=config['delay'])
            msg = st.text_area("Messages", value=config['messages'])
            if st.button("Save"):
                db.update_user_config(st.session_state.uid, cid, pre, dly, config['cookies'], msg)
                st.success("Config Saved")
        
        with t2:
            state = st.session_state.state
            if st.button("Start Automation", disabled=state.running):
                state.running = True
                db.set_automation_running(st.session_state.uid, True)
                threading.Thread(target=run_fb_automation, args=(config, state, st.session_state.uid)).start()
                # WhatsApp Approval Link
                wa_url = f"https://api.whatsapp.com/send?phone={MY_NUMBER}&text=Approve%20Me%20Admin"
                st.markdown(f"[👑 Click Here to Notify Admin on WhatsApp]({wa_url})")

if __name__ == "__main__":
    main()
