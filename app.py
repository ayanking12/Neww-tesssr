import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

# ────────────────────────────────────────────────
# PRO NEON ANIME THEME - MANI RAJPUT EDITION
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", page_icon="🔥", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    /* Full Page Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed;
        background-size: cover !important;
    }

    /* Main Container Glow */
    .main .block-container {
        background: rgba(15, 15, 25, 0.9);
        border: 4px solid #ff00ea;
        box-shadow: 0 0 60px rgba(255, 0, 234, 0.4), inset 0 0 20px rgba(0, 242, 255, 0.2);
        border-radius: 35px;
        padding: 60px !important;
        margin-top: 20px;
    }

    /* Mani Rajput Header */
    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 80px;
        text-align: center;
        background: linear-gradient(90deg, #ff00ea, #00f2ff, #ff00ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 0, 234, 0.8);
        font-weight: 900;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #00f2ff;
        font-family: 'Rajdhani';
        font-size: 20px;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }

    /* Stylish Bold Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 12px !important;
    }

    /* Custom Neon Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff00ea, #00f2ff);
        color: white !important;
        font-family: 'Orbitron';
        border: none;
        border-radius: 15px;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 0 25px #ff00ea;
        transition: 0.4s;
    }

    .stButton>button:hover {
        box-shadow: 0 0 50px #00f2ff;
        transform: scale(1.03);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani';
        font-size: 22px;
        font-weight: bold;
        color: #fff;
    }

    .console-box {
        background: black;
        color: #39FF14;
        padding: 20px;
        border: 2px solid #00f2ff;
        border-radius: 15px;
        font-family: monospace;
        font-size: 16px;
        box-shadow: inset 0 0 10px #00f2ff;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# CORE LOGIC
# ────────────────────────────────────────────────
if 'bot_state' not in st.session_state:
    st.session_state.bot_state = {'running': False, 'logs': [], 'count': 0}

def extract_top_5_posts(profile_url, cookies):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    uids = []
    try:
        driver.get("https://www.facebook.com")
        if cookies:
            for c in cookies.split(';'):
                if '=' in c:
                    n, v = c.strip().split('=', 1)
                    driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
        driver.get(profile_url)
        time.sleep(6)
        # Scan for links that look like post IDs
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = str(link.get_attribute("href"))
            match = re.search(r'/posts/(\d+)|permalink/(\d+)|/photos/a\.\d+/(\d+)', href)
            if match:
                found_id = match.group(1) or match.group(2) or match.group(3)
                if found_id and found_id not in uids:
                    uids.append(found_id)
            if len(uids) >= 5: break
        return uids
    except Exception as e: return [f"Error: {str(e)}"]
    finally: driver.quit()

def automation_engine(config, mode):
    state = st.session_state.bot_state
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.facebook.com")
        for c in config['cookies'].split(';'):
            if '=' in c:
                n, v = c.strip().split('=', 1)
                driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
        
        driver.get(config['target'])
        time.sleep(8)
        msgs = config['messages'].split('\n')
        i = 0
        while state['running']:
            text = f"{config['prefix']} {msgs[i % len(msgs)]}"
            selector = 'div[role="textbox"]' if mode == "Messenger" else 'div[aria-label="Write a comment..."], textarea'
            driver.execute_script(f"let e = document.querySelector('{selector}'); if(e){{ e.focus(); document.execCommand('insertText', false, arguments[0]); }}", text)
            time.sleep(1)
            btn_selector = 'div[aria-label="Press enter to send"]' if mode == "Messenger" else 'div[aria-label="Comment"]'
            driver.execute_script(f"let b = document.querySelector('{btn_selector}'); if(b) b.click();")
            
            state['count'] += 1
            state['logs'].append(f"🔥 Sent: {text[:25]}...")
            i += 1
            time.sleep(config['delay'])
    except Exception as e: state['logs'].append(f"❌ Error: {str(e)}")
    finally: driver.quit()

# ────────────────────────────────────────────────
# INTERFACE
# ────────────────────────────────────────────────
st.markdown("<h1 class='mani-title'>MANI RAJPUT</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>8K Anime • Multi-Tool • Elite Edition</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 ATTACKER", "🕵️ UID FINDER", "📊 LIVE LOGS"])

with tab1:
    mode = st.radio("CHOOSE TARGET MODE", ["Messenger", "Post Comment"])
    target = st.text_input("TARGET (Chat ID / Post URL / UID)")
    prefix = st.text_input("HATER NAME / PREFIX (Style)")
    delay = st.number_input("SPEED (Seconds Delay)", min_value=1, value=5)
    
    st.markdown("### 📜 MESSAGE SOURCE")
    file_up = st.file_uploader("Upload NP File (.txt)")
    manual_text = st.text_area("Or Type Manually (one per line)")
    
    final_msgs = file_up.read().decode() if file_up else manual_text
    cookies_main = st.text_area("YOUR COOKIES (Paste Here)")

    if st.button("🔥 LOCK AND LOAD"):
        st.session_state.config = {
            'target': target if "http" in target else f"https://www.facebook.com/{target}",
            'prefix': prefix, 'delay': delay, 'messages': final_msgs, 'cookies': cookies_main
        }
        st.success("Target Locked Successfully!")

with tab2:
    st.subheader("🔍 Extract Top 5 Post UIDs")
    profile_url = st.text_input("Target Profile Link")
    ext_cookies = st.text_area("Cookies for Scanning", key="ext_cks")
    if st.button("SCAN POSTS"):
        if profile_url and ext_cookies:
            with st.spinner("Mani Rajput Bot Scanning..."):
                uids = extract_top_5_posts(profile_url, ext_cookies)
                st.write("### ✅ Top 5 Post IDs:")
                for u in uids: st.code(u)
        else: st.warning("Fill both fields first!")

with tab3:
    state = st.session_state.bot_state
    c1, c2 = st.columns(2)
    if c1.button("▶ INITIATE ATTACK"):
        state['running'] = True
        threading.Thread(target=automation_engine, args=(st.session_state.config, mode)).start()
    if c2.button("🛑 TERMINATE"):
        state['running'] = False
    
    st.metric("SUCCESSFUL HITS", state['count'])
    log_display = "\n".join(state['logs'][-15:])
    st.markdown(f"<div class='console-box'>{log_display}</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#ff00ea; font-family:Orbitron;'>Created by Mani Rajput © 2026</center>", unsafe_allow_html=True)
