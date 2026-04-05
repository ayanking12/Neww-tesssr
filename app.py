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
import re

# ────────────────────────────────────────────────
# PRO ULTRA NEON THEME (Mani Rajput Special)
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", page_icon="🔥", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Permanent+Marker&display=swap');

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images8.alphacoders.com/105/1053155.jpg');
        background-size: cover !important;
        background-position: center;
    }

    .main .block-container {
        background: rgba(10, 10, 20, 0.9);
        border: 3px solid #00f2ff;
        box-shadow: 0 0 50px rgba(0, 242, 255, 0.3);
        border-radius: 30px;
        padding: 50px !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 70px;
        text-align: center;
        background: linear-gradient(to right, #ff00ea, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 5px 5px 20px rgba(255, 0, 234, 0.5);
        margin-bottom: 5px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #ff00ea);
        color: white !important;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        font-family: 'Orbitron';
        height: 55px;
        box-shadow: 0 0 20px #ff00ea;
    }

    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.05) !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { background: transparent; }
    .stTabs [data-baseweb="tab"] { color: #fff; font-family: 'Orbitron'; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #ff00ea !important; border-bottom-color: #ff00ea !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ────────────────────────────────────────────────
# LOGIC & EXTRACTION
# ────────────────────────────────────────────────
if 'bot_state' not in st.session_state:
    st.session_state.bot_state = {'running': False, 'logs': [], 'count': 0}

def extract_post_uids(profile_url, cookies):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    post_ids = []
    
    try:
        driver.get("https://www.facebook.com")
        if cookies:
            for c in cookies.split(';'):
                if '=' in c:
                    name, val = c.strip().split('=', 1)
                    driver.add_cookie({'name': name, 'value': val, 'domain': '.facebook.com'})
        
        driver.get(profile_url)
        time.sleep(5)
        
        # Finding post links/IDs (Facebook mobile or desktop structures)
        elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/posts/') or contains(@href, '/photos/') or contains(@href, 'permalink')]")
        
        for el in elements:
            href = el.get_attribute("href")
            # Cleaning the URL to get ID
            match = re.search(r'(\d{10,})', href)
            if match and match.group(1) not in post_ids:
                post_ids.append(match.group(1))
            if len(post_ids) >= 5: break
            
        return post_ids
    except Exception as e:
        return [f"Error: {str(e)}"]
    finally:
        driver.quit()

# ────────────────────────────────────────────────
# UI INTERFACE
# ────────────────────────────────────────────────
st.markdown("<h1 class='mani-title'>Mani Rajput</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00f2ff; font-family:Orbitron;'>MULTIFUNCTIONAL FB ATTACKER</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 ATTACKER", "💎 POST UID FINDER", "📟 LOGS"])

with tab1:
    mode = st.radio("SELECT TARGET", ["Messenger", "Post Comment"])
    target = st.text_input("Enter Target Link / Post ID")
    prefix = st.text_input("Hater Name / Prefix")
    delay = st.number_input("Speed (Delay Seconds)", min_value=1, value=5)
    
    st.markdown("### 📜 Message Source")
    file = st.file_uploader("Upload NP File (.txt)")
    manual = st.text_area("Or Write Manually")
    msgs = file.read().decode() if file else manual
    
    cks = st.text_area("Cookies (Required for Post/Extraction)")
    
    if st.button("🔥 LOCK TARGET"):
        st.session_state.config = {'target': target, 'prefix': prefix, 'delay': delay, 'messages': msgs, 'cookies': cks}
        st.success("Target Locked! Ready for Attack.")

with tab2:
    st.subheader("🕵️ Target Profile Post Extractor")
    prof_url = st.text_input("Paste Profile URL (e.g. facebook.com/mani.rajput)")
    cookie_for_ext = st.text_area("Paste Cookies (Required to see private/protected posts)", key="ext_cookie")
    
    if st.button("Extract Top 5 Post IDs"):
        if prof_url and cookie_for_ext:
            with st.spinner("Scanning Profile..."):
                results = extract_post_uids(prof_url, cookie_for_ext)
                if results:
                    st.write("### ✅ Top 5 Posts Found:")
                    for r in results:
                        st.code(r)
                else:
                    st.error("No posts found. Check cookies or link.")
        else:
            st.warning("Please provide both Profile URL and Cookies.")

with tab3:
    state = st.session_state.bot_state
    c1, c2 = st.columns(2)
    if c1.button("▶ START SYSTEM"):
        # Yahan automation function call hoga (pichle code wala logic)
        state['running'] = True
        st.info("System Initiated...")
    if c2.button("🛑 KILL SYSTEM"):
        state['running'] = False
        st.error("System Stopped.")
    
    st.metric("ATTACK COUNT", state['count'])
    st.text_area("Console", value="\n".join(state['logs'][-10:]), height=200)

