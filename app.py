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
# DATABASE SYSTEM (User Management)
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
            if not username or not password: return False, "Fields cannot be empty!"
            conn = sqlite3.connect('users.db', check_same_thread=False)
            c = conn.cursor()
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users (username, password, chat_id, name_prefix, delay, cookies, messages, is_running) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (username, hashed_pw, '', '', 5, '', '', False))
            conn.commit()
            return True, "👑 Account Created! Now Login."
        except sqlite3.IntegrityError:
            return False, "❌ Username already exists!"
        except Exception as e:
            return False, f"Error: {str(e)}"

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

init_db()
db = Database()

# ────────────────────────────────────────────────
# SETTINGS & THEME
# ────────────────────────────────────────────────
ADMIN_PASSWORD = "Rkraja"
MY_NUMBER = "60143153573" # Aapka Updated Number
TELEGRAM_BOT_TOKEN = "8782762466:AAGh2AOb7Cj2EdG09_sD-graYMzeN4LNm88"

st.set_page_config(page_title="E2E ⚜️9MAN⚜️", page_icon="👑", layout="wide")

st.markdown("""
<style>
    .stApp { background: #1a0033; color: #ffd700; }
    .main-header { text-align: center; border: 2px solid #ffd700; border-radius: 20px; padding: 20px; background: #2a0055; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #b8860b, #ffd700); color: black; font-weight: bold; border-radius: 10px; border:none; }
    .console-box { background: #000; color: #0f0; padding: 15px; font-family: monospace; border: 1px solid #ffd700; border-radius: 10px; max-height: 300px; overflow-y: auto; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# AUTOMATION ENGINE (Selenium)
# ────────────────────────────────────────────────
class State:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []

if 'state' not in st.session_state: st.session_state.state = State()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def run_automation(config, state, user_id):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=options)
        state.logs.append("🌐 Browser Started...")
        driver.get("https://www.facebook.com")
        
        if config['cookies']:
            for c in config['cookies'].split(';'):
                if '=' in c:
                    name, val = c.strip().split('=', 1)
                    driver.add_cookie({'name': name, 'value': val, 'domain': '.facebook.com'})
        
        driver.get(f"https://www.facebook.com/messages/t/{config['chat_id']}")
        time.sleep(10)
        
        msgs = [m.strip() for m in config['messages'].split('\n') if m.strip()]
        if not msgs: msgs = ["Hello from 9MAN"]
        
        i = 0
        while state.running:
            text = f"{config['name_prefix']} {msgs[i % len(msgs)]}"
            # Type Message
            driver.execute_script("""
                let e = document.querySelector('div[role="textbox"]');
                if(e){ e.focus(); document.execCommand('insertText', false, arguments[0]); }
            """, text)
            time.sleep(1)
            # Click Send
            driver.execute_script("""
                let b = document.querySelector('div[aria-label="Press enter to send"]');
                if(b) b.click();
            """)
            
            state.message_count += 1
            state.logs.append(f"✅ Sent: {text[:20]}...")
            i += 1
            time.sleep(config['delay'])
            
    except Exception as e:
        state.logs.append(f"❌ Error: {str(e)}")
    finally:
        if 'driver' in locals(): driver.quit()
        state.running = False
        db.set_automation_running(user_id, False)

# ────────────────────────────────────────────────
# UI - LOGIN & MAIN APP
# ────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        st.markdown("<div class='main-header'><h1>👑 9MAN ROYAL SYSTEM 👑</h1></div>", unsafe_allow_html=True)
        tab_log, tab_sign = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab_log:
            u = st.text_input("Username", key="l_u")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("Access Kingdom"):
                uid = db.verify_user(u, p)
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.uid = uid
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Wrong Username or Password!")
        
        with tab_sign:
            nu = st.text_input("New Username", key="s_u")
            np = st.text_input("New Password", type="password", key="s_p")
            if st.button("Create Account"):
                s, m = db.create_user(nu, np)
                if s: st.success(m)
                else: st.error(m)
    else:
        # Main App After Login
        st.sidebar.markdown(f"### 👑 Welcome: {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        config = db.get_user_config(st.session_state.uid)
        t_set, t_run = st.tabs(["⚙️ Settings", "🚀 Automation Control"])
        
        with t_set:
            cid = st.text_input("Target Chat ID", value=config['chat_id'])
            pre = st.text_input("Hater Name / Prefix", value=config['name_prefix'])
            dly = st.number_input("Delay (Seconds)", value=config['delay'], min_value=1)
            msg = st.text_area("Messages (One per line)", value=config['messages'], height=150)
            cks = st.text_area("Cookies (Paste here)", value=config['cookies'], height=100)
            
            if st.button("💾 Save Settings"):
                db.update_user_config(st.session_state.uid, cid, pre, dly, cks, msg)
                st.success("Settings Updated!")

        with t_run:
            state = st.session_state.state
            col1, col2 = st.columns(2)
            
            if col1.button("▶ START ATTACK", disabled=state.running):
                if not config['chat_id']: st.error("Set Chat ID first!")
                else:
                    state.running = True
                    db.set_automation_running(st.session_state.uid, True)
                    threading.Thread(target=run_automation, args=(db.get_user_config(st.session_state.uid), state, st.session_state.uid)).start()
                    st.rerun()

            if col2.button("🛑 STOP ATTACK", disabled=not state.running):
                state.running = False
                st.rerun()

            st.divider()
            st.metric("Total Messages Sent", state.message_count)
            
            st.write("### 📜 Live Logs")
            log_html = "".join([f"<div>{l}</div>" for l in state.logs[-15:]])
            st.markdown(f"<div class='console-box'>{log_html}</div>", unsafe_allow_html=True)
            
            # Admin WhatsApp Link
            wa_link = f"https://api.whatsapp.com/send?phone={MY_NUMBER}&text=Jani%20Mera%20Approve%20Krdo%20Key"
            st.markdown(f"<br><center><a href='{wa_link}' style='color:#ffd700; text-decoration:none;'>👑 MESSAGE ADMIN ON WHATSAPP</a></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
