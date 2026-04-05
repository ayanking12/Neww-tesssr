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
# RGB NEON ANIME THEME - MANI RAJPUT 8K
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", page_icon="🔥", layout="wide")

# RGB Neon Styling
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Permanent+Marker&display=swap');

    /* Background Fix with Overlay */
    .stApp {
        background: linear-gradient(45deg, rgba(255,0,0,0.4), rgba(0,0,255,0.4), rgba(0,255,0,0.4)), 
                    url('https://wallpaperaccess.com/full/1311053.jpg') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    /* Multi-Color Neon Border Container */
    .main .block-container {
        background: rgba(0, 0, 0, 0.85) !important;
        border: 5px solid;
        border-image: linear-gradient(45deg, red, blue, green, yellow, magenta) 1;
        box-shadow: 0 0 40px rgba(255, 0, 234, 0.6);
        border-radius: 20px;
        padding: 40px !important;
        margin-top: 20px;
    }

    /* Mani Rajput Multi-Color Header */
    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 75px;
        text-align: center;
        font-weight: 900;
        background: linear-gradient(to right, #ff0000, #0000ff, #00ff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 15px rgba(255,255,255,0.3);
        margin-bottom: 0;
    }

    /* Buttons Style RGB */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron' !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        height: 55px !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(255,255,255,0.4) !important;
    }

    /* Input Fields Customization */
    input, textarea, .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #00f2ff !important;
        border: 2px solid #00ff00 !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    label {
        color: #ff00ea !important;
        font-size: 20px !important;
        font-family: 'Orbitron' !important;
        text-shadow: 1px 1px 5px black;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 30, 0.95) !important;
        border-right: 2px solid #ff0000;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# BACKEND LOGIC
# ────────────────────────────────────────────────
if 'bot_state' not in st.session_state:
    st.session_state.bot_state = {'running': False, 'logs': [], 'count': 0}

def get_top_5_post_uids(profile_url, cookies):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    ids = []
    try:
        driver.get("https://www.facebook.com")
        for c in cookies.split(';'):
            if '=' in c:
                n, v = c.strip().split('=', 1)
                driver.add_cookie({'name': n, 'value': v, 'domain': '.facebook.com'})
        driver.get(profile_url)
        time.sleep(7)
        # Regex to find post IDs in links
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = str(link.get_attribute("href"))
            match = re.search(r'/posts/(\d+)|permalink/(\d+)', href)
            if match:
                pid = match.group(1) or match.group(2)
                if pid and pid not in ids: ids.append(pid)
            if len(ids) >= 5: break
        return ids
    except Exception as e: return [f"Error: {str(e)}"]
    finally: driver.quit()

# ────────────────────────────────────────────────
# UI MAIN
# ────────────────────────────────────────────────
st.markdown("<h1 class='mani-title'>MANI RAJPUT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#fff; font-family:Orbitron; letter-spacing:5px;'>ELITE FB MULTI-ATTACKER</p>", unsafe_allow_html=True)

# Sidebar for Cookie Help
with st.sidebar:
    st.header("🍪 COOKIE ASSISTANT")
    st.write("Jani, login system se ID block hoti hai, isliye ye tareeqa best hai:")
    st.markdown("""
    1. Kiwi Browser download karein.
    2. FB login karke 'Get Cookie' extension chalayen.
    3. Copy karke yahan paste karein.
    """)
    if st.button("Logout"):
        st.session_state.bot_state['running'] = False
        st.rerun()

tab1, tab2, tab3 = st.tabs(["🔥 ATTACKER", "🕵️ POST FINDER", "📟 TERMINAL"])

with tab1:
    mode = st.radio("CHOOSE MODE", ["Messenger", "Post Comment"])
    target_id = st.text_input("TARGET (Chat ID / Post UID)")
    prefix = st.text_input("HATER NAME (Prefix)")
    delay = st.number_input("SPEED (Seconds)", min_value=1, value=5)
    
    st.markdown("### 📄 MESSAGES")
    file_up = st.file_uploader("Upload NP File (.txt)")
    txt_area = st.text_area("Or Type Messages (one per line)")
    
    final_msgs = file_up.read().decode() if file_up else txt_area
    cookies_main = st.text_area("PASTE COOKIES HERE", key="main_cks")

    if st.button("🚀 INITIATE ATTACK"):
        st.session_state.config = {
            'target': target_id, 'prefix': prefix, 'delay': delay, 
            'messages': final_msgs, 'cookies': cookies_main
        }
        st.success("Target Locked! Go to Terminal to Start.")

with tab2:
    st.subheader("🔍 Get Top 5 Post IDs")
    prof_url = st.text_input("Profile Link (fb.com/username)")
    ext_cks = st.text_area("Cookies for Scanning", key="ext_cks_tab")
    if st.button("SCAN PROFILE"):
        with st.spinner("Mani Rajput Bot Scanning..."):
            uids = get_top_5_post_uids(prof_url, ext_cks)
            st.write("### ✅ Post IDs Found:")
            for u in uids: st.code(u)

with tab3:
    state = st.session_state.bot_state
    c1, c2 = st.columns(2)
    if c1.button("▶ START ATTACK"):
        state['running'] = True
        st.info("Automation Running in Background...")
        # (Yahan aapka selenium loop thread mein chalega)
    if c2.button("🛑 STOP SYSTEM"):
        state['running'] = False
        st.warning("Attack Terminated.")

    st.metric("SUCCESS HITS", state['count'])
    st.markdown(f"<div class='console-box'>{''.join(state['logs'][-10:])}</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#00ff00; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud</center>", unsafe_allow_html=True)
