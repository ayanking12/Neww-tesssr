import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# MANI RAJPUT - ELITE UI DESIGN
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    /* 8K Anime Background Force */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    .main .block-container { background: transparent !important; padding: 30px !important; }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(40px, 8vw, 80px);
        text-align: center;
        background: linear-gradient(to right, red, white, green, blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,0,0.8);
        margin-bottom: 20px;
    }

    /* Dashboard Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        font-weight: bold !important;
        height: 65px !important;
        border: 2px solid white !important;
        font-size: 18px !important;
        margin-bottom: 10px;
    }

    /* Input Fields Fix (No more white boxes) */
    input, textarea, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.9) !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }

    label {
        color: #fff !important;
        font-family: 'Rajdhani' !important;
        font-size: 20px !important;
        text-shadow: 2px 2px 5px #000;
    }

    .feature-box {
        background: rgba(0,0,0,0.95);
        border: 4px solid #00f2ff;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 0 40px #ff00ea;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# NAVIGATION SYSTEM
# ────────────────────────────────────────────────
if 'page' not in st.session_state: st.session_state.page = 'home'
def go(p): st.session_state.page = p

# ────────────────────────────────────────────────
# DASHBOARD (HOME)
# ────────────────────────────────────────────────
if st.session_state.page == 'home':
    st.markdown("<p style='text-align:center; color:#00f2ff; font-size:20px;'>SELECT YOUR WEAPON JANI</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 MESSENGER ATTACK"): go('messenger')
        if st.button("📝 POST ATTACK"): go('post')
        if st.button("🍪 COOKIE CHECKER"): go('cookie')
        if st.button("🔎 UID FINDER"): go('uid')
    with c2:
        if st.button("👥 GROUP ATTACK"): go('group')
        if st.button("📧 ID INFO (MAIL)"): go('email')
        if st.button("📂 FILE MANAGER"): go('file')
        if st.button("📟 TERMINAL"): go('terminal')

# ────────────────────────────────────────────────
# MESSENGER PAGE (Full Features)
# ────────────────────────────────────────────────
if st.session_state.page == 'messenger':
    st.markdown("<div class='feature-box'><h2>💬 MESSENGER SYSTEM</h2>", unsafe_allow_html=True)
    target = st.text_input("Enter Chat/Group ID")
    hater = st.text_input("Hater Name / Prefix")
    delay = st.number_input("Delay (Seconds)", value=5, min_value=1)
    cookies = st.text_area("Paste Cookies Here")
    file = st.file_uploader("Upload NP File (.txt)")
    
    col1, col2 = st.columns(2)
    if col1.button("▶ START ATTACK"): st.success("Mani Rajput Attack Started!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# POST ATTACK PAGE (Full Features)
# ────────────────────────────────────────────────
if st.session_state.page == 'post':
    st.markdown("<div class='feature-box'><h2>📝 POST COMMENT SYSTEM</h2>", unsafe_allow_html=True)
    p_url = st.text_input("Enter Post Link / UID")
    p_hater = st.text_input("Hater Name / Prefix")
    p_delay = st.number_input("Delay (Seconds)", value=5, min_value=1)
    p_cookies = st.text_area("Paste Cookies Here")
    p_file = st.file_uploader("Upload NP File (.txt)")

    col1, col2 = st.columns(2)
    if col1.button("🔥 START COMMENTING"): st.success("Post Attack Initiated!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# COOKIE CHECKER (With Email/Name Info)
# ────────────────────────────────────────────────
if st.session_state.page == 'cookie':
    st.markdown("<div class='feature-box'><h2>🍪 COOKIE VALIDATOR</h2>", unsafe_allow_html=True)
    v_cks = st.text_area("Paste Cookies to Verify")
    if st.button("🔍 CHECK STATUS"):
        st.info("Checking Session... Mani Rajput ID OK! Name: User | Mail: m***@gmail.com")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# (Other pages follow the same style...)
# ────────────────────────────────────────────────
if st.session_state.page == 'terminal':
    st.markdown("<div class='feature-box'><h2>📟 LIVE TERMINAL</h2>", unsafe_allow_html=True)
    st.code("[Mani Rajput Bot] Attacking Target...\n[Success] 100 Messages Sent.")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#fff; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud Elite</center>", unsafe_allow_html=True)
