import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# RGB NEON THEME - MANI RAJPUT VIP LOOK
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #ff0000, #0000ff, #00ff00);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main .block-container {
        background: rgba(0, 0, 0, 0.92) !important;
        border: 4px solid #fff;
        box-shadow: 0 0 50px rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 50px !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        text-align: center;
        background: linear-gradient(to right, red, white, green);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255,0,0,0.5);
    }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani';
        font-size: 18px;
        color: #fff;
        background: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(to right, red, blue) !important;
        color: white !important;
    }

    input, textarea {
        background-color: #111 !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
        font-weight: bold !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        height: 55px !important;
        border: 2px solid white !important;
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
            # Email check
            e_res = requests.get('https://mbasic.facebook.com/settings/email/', headers=headers)
            email = re.search(r'mailto:(.*?)"', e_res.text).group(1) if "mailto:" in e_res.text else "Hidden"
            return True, {"Name": name, "UID": uid, "Email": email}
        return False, None
    except: return False, None

# ────────────────────────────────────────────────
# TABS SYSTEM (6 SEPARATE TABS)
# ────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "💬 MESSENGER", 
    "📝 POST COMMENT", 
    "🍪 COOKIE CHECKER", 
    "🔎 UID FINDER", 
    "📂 FILE UPLOADER", 
    "📟 TERMINAL"
])

# 1. Messenger Tab
with t1:
    st.header("🚀 Messenger Attacker")
    m_target = st.text_input("Enter Group/Chat ID")
    m_prefix = st.text_input("Messenger Prefix")
    m_delay = st.number_input("Delay (Sec)", value=5, key="m_d")
    m_cks = st.text_area("Messenger Cookies", key="m_c")
    if st.button("LOCK MESSENGER"): st.success("Messenger Target Locked!")

# 2. Post Comment Tab
with t2:
    st.header("🔥 Post Comment Attacker")
    p_target = st.text_input("Enter Post URL / UID")
    p_prefix = st.text_input("Post Prefix")
    p_delay = st.number_input("Delay (Sec)", value=5, key="p_d")
    p_cks = st.text_area("Post Cookies", key="p_c")
    if st.button("LOCK POST"): st.success("Post Target Locked!")

# 3. Cookie Checker Tab
with t3:
    st.header("🕵️ Cookie Validator")
    v_cks = st.text_area("Paste Cookies to Verify Status")
    if st.button("CHECK ID INFO"):
        ok, info = check_cookie_info(v_cks)
        if ok:
            st.success("✅ Active Session Found!")
            st.table(info)
        else: st.error("❌ Cookies Expired or Invalid")

# 4. UID Finder Tab
with t4:
    st.header("🔍 Extract Post UIDs")
    prof_link = st.text_input("Profile URL")
    scan_cks = st.text_area("Cookies for Scanning", key="s_c")
    if st.button("SCAN TOP 5 POSTS"):
        st.info("Scanning... Post IDs will appear here.")

# 5. File Uploader Tab
with t5:
    st.header("📂 Message Source")
    up_file = st.file_uploader("Upload NP File (.txt)")
    manual_msg = st.text_area("Or Write Manually", height=200)
    if st.button("SAVE MESSAGES"): st.success("Messages Saved Successfully!")

# 6. Terminal Tab
with t6:
    st.header("📟 Control Center")
    col1, col2 = st.columns(2)
    if col1.button("▶ INITIATE ATTACK"): st.info("System Online...")
    if col2.button("🛑 STOP SYSTEM"): st.warning("System Offline.")
    st.write("### Live Attack Logs")
    st.markdown("<div style='background:black; color:lime; padding:10px; border-radius:10px;'>Waiting for Start...</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#fff;'>Mani Rajput © 2026</center>", unsafe_allow_html=True)
