import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

# ────────────────────────────────────────────────
# DATABASE & AUTH SYSTEM
# ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, 
                  chat_id TEXT, post_url TEXT, name_prefix TEXT, delay INTEGER, cookies TEXT, messages TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ────────────────────────────────────────────────
# ADVANCED UI & NEON ANIME THEME
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", page_icon="🔥", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.alphacoders.com/131/1311053.png');
        background-size: cover;
        background-attachment: fixed;
    }

    h1, h2, h3, label, .stMetric {
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff !important;
        text-shadow: 2px 2px 10px #00f2ff;
        font-weight: 900 !important;
        text-transform: uppercase;
    }

    .main-header {
        text-align: center;
        padding: 30px;
        border: 4px solid #ff00ea;
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.8);
        box-shadow: 0 0 30px #ff00ea;
        margin-bottom: 25px;
    }

    .mani-name {
        font-size: 50px;
        color: #fff;
        text-shadow: 0 0 10px #ff00ea, 0 0 20px #ff00ea, 0 0 40px #ff00ea;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff00ea, #00f2ff);
        color: white !important;
        font-weight: bold;
        font-size: 20px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 0, 234, 0.4);
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #00f2ff;
    }

    .console-box {
        background: rgba(0, 0, 0, 0.9);
        color: #0f0;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        font-weight: bold;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# AUTOMATION ENGINE (Universal: Chat + Post)
# ────────────────────────────────────────────────
class BotState:
    def __init__(self):
        self.running = False
        self.logs = []
        self.count = 0

if 'bot_state' not in st.session_state: st.session_state.bot_state = BotState()

def run_attack(config, mode):
    state = st.session_state.bot_state
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.facebook.com")
        for c in config['cookies'].split(';'):
            if '=' in c:
                name, val = c.strip().split('=', 1)
                driver.add_cookie({'name': name, 'value': val, 'domain': '.facebook.com'})
        
        target = config['chat_id'] if mode == "Messenger" else config['post_url']
        driver.get(target)
        time.sleep(10)
        
        msgs = config['messages'].split('\n')
        i = 0
        while state.running:
            text = f"{config['prefix']} {msgs[i % len(msgs)]}"
            
            if mode == "Messenger":
                driver.execute_script("let e = document.querySelector('div[role=\"textbox\"]'); if(e){ e.focus(); document.execCommand('insertText', false, arguments[0]); }", text)
                time.sleep(1)
                driver.execute_script("let b = document.querySelector('div[aria-label=\"Press enter to send\"]'); if(b) b.click();")
            else: # Post Comment Mode
                driver.execute_script("let e = document.querySelector('div[aria-label=\"Write a comment...\"], textarea'); if(e){ e.focus(); document.execCommand('insertText', false, arguments[0]); }", text)
                time.sleep(1)
                driver.execute_script("let b = document.querySelector('div[aria-label=\"Comment\"]'); if(b) b.click();")
            
            state.count += 1
            state.logs.append(f"🔥 [{mode}] Sent: {text[:20]}...")
            i += 1
            time.sleep(config['delay'])
    except Exception as e:
        state.logs.append(f"❌ Error: {str(e)}")
    finally:
        driver.quit()
        state.running = False

# ────────────────────────────────────────────────
# MAIN UI
# ────────────────────────────────────────────────
st.markdown("<div class='main-header'><div class='mani-name'>Mani Rajput</div><p style='color:#00f2ff'>8K ANIME EDITION - FB MULTI TOOL</p></div>", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Enter The Matrix"):
        if u and p: 
            st.session_state.logged_in = True
            st.rerun()
else:
    # Sidebar - Extra Tools
    with st.sidebar:
        st.header("🛠 TOOLS")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        st.subheader("🍪 Cookie Extractor")
        st.info("Direct Login system under maintenance. Use Laptop/Kiwi for now.")

    # Tabs
    t1, t2 = st.tabs(["🚀 SETTINGS", "📟 TERMINAL"])

    with t1:
        mode = st.radio("Choose Target Mode", ["Messenger", "Post Comment"])
        cid = st.text_input("Target (Chat ID or Post URL)")
        pre = st.text_input("Hater Name / Prefix")
        dly = st.number_input("Delay (Seconds)", min_value=1, value=5)
        
        st.markdown("### 📝 MESSAGES")
        file = st.file_uploader("Upload NP File (.txt)", type="txt")
        manual_msg = st.text_area("Or Type Manually (one per line)")
        
        final_msgs = ""
        if file:
            final_msgs = file.read().decode("utf-8")
        else:
            final_msgs = manual_msg
            
        cks = st.text_area("Paste Cookies Here")
        
        if st.button("Save & Prepare Attack"):
            st.session_state.config = {
                'chat_id': cid if mode == "Messenger" else cid,
                'post_url': cid if mode == "Post Comment" else "",
                'prefix': pre,
                'delay': dly,
                'messages': final_msgs,
                'cookies': cks
            }
            st.success("Configuration Saved!")

    with t2:
        state = st.session_state.bot_state
        if st.button("▶ START ATTACK", disabled=state.running):
            state.running = True
            threading.Thread(target=run_attack, args=(st.session_state.config, mode)).start()
            st.rerun()
        
        if st.button("🛑 STOP ATTACK", disabled=not state.running):
            state.running = False
            st.rerun()
            
        st.metric("SUCCESSFUL HITS", state.count)
        log_txt = "\n".join(state.logs[-15:])
        st.markdown(f"<div class='console-box'>{log_txt}</div>", unsafe_allow_html=True)
