import streamlit as st
import threading
import time
import re
import requests
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# MANI RAJPUT - ELITE UI & RGB THEME
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput AI Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    /* Force Anime Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed !important;
        background-size: cover !important;
    }

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

    /* Glowing Dashboard Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        font-weight: bold !important;
        height: 70px !important;
        border: 2px solid white !important;
        border-radius: 15px !important;
        font-size: 18px !important;
        margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }

    /* RGB Neon Inputs */
    input, textarea, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.95) !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }

    label { color: #fff !important; font-family: 'Rajdhani'; font-size: 20px; }

    .feature-box {
        background: rgba(0,0,0,0.95);
        border: 3px solid #00f2ff;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 0 40px #ff00ea;
    }
    
    .console-box {
        background: #000;
        color: #39FF14;
        padding: 15px;
        border: 1px solid #00f2ff;
        border-radius: 10px;
        font-family: monospace;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# SHARED LOGIC (Cookies, Attack, Extraction)
# ────────────────────────────────────────────────
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'bot_state' not in st.session_state: st.session_state.bot_state = {'running': False, 'logs': [], 'count': 0}

def go(p): st.session_state.page = p

def repair_cookie(raw):
    clean = ""
    for item in ['c_user', 'xs', 'fr', 'datr']:
        match = re.search(f"{item}=(.*?);", raw + ";")
        if match: clean += f"{item}={match.group(1)}; "
    return clean if clean else raw

def check_fb_session(cks):
    try:
        h = {'cookie': cks, 'user-agent': 'Mozilla/5.0'}
        res = requests.get('https://mbasic.facebook.com/profile.php', headers=h, timeout=10)
        if 'logout.php' in res.text:
            name = re.search(r'<title>(.*?)</title>', res.text).group(1)
            uid = re.search(r'target_id=(\d+)', res.text).group(1)
            return True, name, uid
        return False, None, None
    except: return False, None, None

# ────────────────────────────────────────────────
# 1. HOME DASHBOARD
# ────────────────────────────────────────────────
if st.session_state.page == 'home':
    st.markdown("<p style='text-align:center; color:#00f2ff; font-size:20px;'>SELECT YOUR ELITE WEAPON</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 MESSENGER ATTACK"): go('messenger')
        if st.button("📝 POST ATTACK"): go('post')
        if st.button("🤖 AI AUTO-REPLY"): go('ai_reply')
        if st.button("🍪 COOKIE CHECKER"): go('cookie')
    with c2:
        if st.button("🔎 UID FINDER"): go('uid')
        if st.button("📂 FILE MANAGER"): go('file')
        if st.button("👥 GROUP ATTACK"): go('group')
        if st.button("📟 TERMINAL"): go('terminal')

# ────────────────────────────────────────────────
# 2. MESSENGER PAGE
# ────────────────────────────────────────────────
if st.session_state.page == 'messenger':
    st.markdown("<div class='feature-box'><h2>💬 MESSENGER SYSTEM</h2>", unsafe_allow_html=True)
    target = st.text_input("Enter Chat/Group ID")
    hater = st.text_input("Hater Name / Prefix")
    delay = st.number_input("Delay (Seconds)", value=5, min_value=1)
    cookies = st.text_area("Paste Cookies Here")
    file = st.file_uploader("Upload NP File (.txt)")
    
    col1, col2 = st.columns(2)
    if col1.button("▶ START ATTACK"): st.success("Mani Rajput Messenger Attack Started!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 3. POST ATTACK PAGE
# ────────────────────────────────────────────────
if st.session_state.page == 'post':
    st.markdown("<div class='feature-box'><h2>📝 POST COMMENT SYSTEM</h2>", unsafe_allow_html=True)
    p_url = st.text_input("Enter Post Link / UID")
    p_hater = st.text_input("Hater Name")
    p_delay = st.number_input("Delay", value=5, key="p_d")
    p_cookies = st.text_area("Paste Cookies Here", key="p_c")
    p_file = st.file_uploader("Upload File", key="p_f")

    col1, col2 = st.columns(2)
    if col1.button("🔥 START COMMENTING"): st.success("Post Attack Initiated!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 4. AI AUTO-REPLY PAGE
# ────────────────────────────────────────────────
if st.session_state.page == 'ai_reply':
    st.markdown("<div class='feature-box'><h2>🤖 AI SMART COUNTER-ATTACK</h2>", unsafe_allow_html=True)
    ai_lines = st.text_area("Savage Lines (Use [Name] for target's name)", 
                            value="Oye [Name], Mani Rajput ke bot se panga mat le!")
    st.toggle("Activate AI Smart Defender")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 5. COOKIE CHECKER
# ────────────────────────────────────────────────
if st.session_state.page == 'cookie':
    st.markdown("<div class='feature-box'><h2>🍪 COOKIE REPAIR & CHECK</h2>", unsafe_allow_html=True)
    raw_cks = st.text_area("Paste Cookies (Via/Chrome/Yandex)")
    if st.button("🔍 VALIDATE & GET INFO"):
        clean = repair_cookie(raw_cks)
        ok, name, uid = check_fb_session(clean)
        if ok:
            st.success(f"✅ Active! Name: {name} | UID: {uid}")
            st.code(clean)
        else: st.error("❌ Invalid or Expired Cookie!")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 6. UID FINDER
# ────────────────────────────────────────────────
if st.session_state.page == 'uid':
    st.markdown("<div class='feature-box'><h2>🔎 POST UID EXTRACTOR</h2>", unsafe_allow_html=True)
    prof = st.text_input("Target Profile Link")
    if st.button("EXTRACT TOP 5 POSTS"): st.code("Scanning... (Requires active cookies)")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 7. TERMINAL
# ────────────────────────────────────────────────
if st.session_state.page == 'terminal':
    st.markdown("<div class='feature-box'><h2>📟 LIVE TERMINAL</h2>", unsafe_allow_html=True)
    state = st.session_state.bot_state
    st.metric("SUCCESSFUL HITS", state['count'])
    st.markdown("<div class='console-box'>[Mani Rajput Bot] System Online... Ready for command.</div>", unsafe_allow_html=True)
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#fff; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud Elite</center>", unsafe_allow_html=True)
