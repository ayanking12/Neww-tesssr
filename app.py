import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# RGB NEON ANIME THEME - MANI RAJPUT SPECIAL
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    /* Background Image Fix */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    /* Vertical Section Styling */
    .main .block-container {
        background: rgba(0, 0, 0, 0.88) !important;
        border-left: 10px solid;
        border-right: 10px solid;
        border-image: linear-gradient(to bottom, red, blue, green, yellow, magenta) 1 !important;
        box-shadow: 0 0 50px rgba(255, 255, 255, 0.1);
        border-radius: 0px;
        padding: 60px !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 80px;
        text-align: center;
        background: linear-gradient(to right, red, #fff, green);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,0,0.8);
        margin-bottom: 50px;
    }

    .section-box {
        border: 2px solid #00f2ff;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 40px;
        background: rgba(255, 255, 255, 0.03);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }

    h2 {
        color: #ff00ea !important;
        font-family: 'Orbitron' !important;
        text-transform: uppercase;
        border-bottom: 2px solid #fff;
        padding-bottom: 10px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        font-weight: bold !important;
        height: 60px !important;
        font-size: 20px !important;
        border: 2px solid white !important;
    }

    input, textarea, .stFileUploader {
        background-color: #111 !important;
        color: #00f2ff !important;
        border: 1px solid #00ff00 !important;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# LOGIC FUNCTIONS
# ────────────────────────────────────────────────
def check_cookie_info(cks):
    headers = {'cookie': cks, 'user-agent': 'Mozilla/5.0'}
    try:
        res = requests.get('https://mbasic.facebook.com/profile.php', headers=headers, timeout=10)
        if 'logout.php' in res.text:
            name = re.search(r'<title>(.*?)</title>', res.text).group(1)
            uid = re.search(r'target_id=(\d+)', res.text).group(1)
            e_res = requests.get('https://mbasic.facebook.com/settings/email/', headers=headers)
            email = re.search(r'mailto:(.*?)"', e_res.text).group(1) if "mailto:" in e_res.text else "Hidden"
            return True, {"Name": name, "UID": uid, "Email": email}
        return False, None
    except: return False, None

# ────────────────────────────────────────────────
# VERTICAL SECTIONS (Up to Down)
# ────────────────────────────────────────────────

# SECTION 1: COOKIE CHECKER
with st.container():
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.header("🍪 1. COOKIE VALIDATOR & ID INFO")
    v_cks = st.text_area("Paste Cookies to Verify", key="v_cks")
    if st.button("🔍 CHECK ID & GET INFO"):
        ok, info = check_cookie_info(v_cks)
        if ok:
            st.success("✅ Active Session!")
            st.table(info)
        else: st.error("❌ Invalid Cookies")
    st.markdown("</div>", unsafe_allow_html=True)

# SECTION 2: MESSENGER ATTACKER
with st.container():
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.header("💬 2. MESSENGER ATTACKER")
    m_target = st.text_input("Group/Chat ID", key="m_t")
    m_prefix = st.text_input("Hater Name", key="m_p")
    m_delay = st.number_input("Speed (Sec)", value=5, key="m_d")
    m_file = st.file_uploader("Upload NP File (.txt)", key="m_f")
    m_cks = st.text_area("Messenger Cookies", key="m_c")
    if st.button("🚀 LOCK MESSENGER"): st.success("Messenger Target Locked!")
    st.markdown("</div>", unsafe_allow_html=True)

# SECTION 3: POST ATTACKER
with st.container():
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.header("🔥 3. POST COMMENT ATTACKER")
    p_target = st.text_input("Post URL / UID", key="p_t")
    p_prefix = st.text_input("Post Prefix", key="p_p")
    p_delay = st.number_input("Speed (Sec)", value=5, key="p_d")
    p_file = st.file_uploader("Upload NP File (.txt)", key="p_f")
    p_cks = st.text_area("Post Cookies", key="p_c")
    if st.button("🎯 LOCK POST"): st.success("Post Target Locked!")
    st.markdown("</div>", unsafe_allow_html=True)

# SECTION 4: UID FINDER
with st.container():
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.header("🔍 4. GET TOP 5 POST UIDs")
    prof_link = st.text_input("Target Profile URL", key="u_l")
    scan_cks = st.text_area("Cookies for Scanning", key="u_c")
    if st.button("🔎 SCAN POSTS"): st.info("Scan results will appear here...")
    st.markdown("</div>", unsafe_allow_html=True)

# SECTION 5: TERMINAL
with st.container():
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.header("📟 5. CONTROL CENTER (TERMINAL)")
    c1, c2 = st.columns(2)
    if c1.button("▶ INITIATE ATTACK"): st.info("Mani Rajput Bot Online...")
    if c2.button("🛑 KILL SYSTEM"): st.warning("System Offline.")
    st.write("### Live Console Logs")
    st.markdown("<div style='background:black; color:lime; padding:15px; border-radius:10px; font-family:monospace;'>[System] Waiting for user command...</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#fff; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud Elite</center>", unsafe_allow_html=True)
