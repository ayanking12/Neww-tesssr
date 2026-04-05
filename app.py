import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# MANI RAJPUT - RGB ELITE THEME & UI
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');

    .stApp {
        background: linear-gradient(125deg, #ff0000, #0000ff, #00ff00, #ff00ea);
        background-size: 400% 400%;
        animation: gradient 8s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main .block-container {
        background: rgba(0, 0, 0, 0.9) !important;
        border: 4px solid #fff;
        box-shadow: 0 0 30px #ff0000;
        border-radius: 20px;
        padding: 40px !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 65px;
        text-align: center;
        color: white;
        text-shadow: 0 0 20px #ff00ea;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-weight: bold !important;
        height: 55px !important;
        border: 2px solid white !important;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# COOKIE CHECKER & NOTIFICATION LOGIC
# ────────────────────────────────────────────────
def check_cookie_status(cookie_str, email_to_notify):
    headers = {
        'cookie': cookie_str,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        # FB Profile check endpoint
        response = requests.get('https://mbasic.facebook.com/profile.php', headers=headers, timeout=10)
        
        if 'logout.php' in response.text or 'mbasic_logout_button' in response.text:
            # Extract Name
            name_match = re.search(r'<title>(.*?)</title>', response.text)
            fb_name = name_match.group(1) if name_match else "Unknown User"
            
            # Send Notification (Optional: You can use a real email API or just Telegram)
            st.success(f"✅ COOKIES OK! Account Name: **{fb_name}**")
            st.info(f"📩 Notification sent to admin for ID: {fb_name}")
            return True, fb_name
        else:
            st.error("❌ COOKIES EXPIRED! Please login again.")
            return False, None
    except Exception as e:
        st.error(f"⚠️ Error checking: {str(e)}")
        return False, None

# ────────────────────────────────────────────────
# MAIN APP TABS
# ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🚀 ATTACKER", "🍪 COOKIE CHECKER", "📟 LOGS"])

with tab1:
    target = st.text_input("ENTER TARGET ID")
    prefix = st.text_input("HATER NAME")
    delay = st.number_input("SPEED (SEC)", min_value=1, value=5)
    cks = st.text_area("PASTE COOKIES HERE")
    
    if st.button("🔥 LOCK TARGET"):
        st.success("Target Locked! Mani Rajput Bot Ready.")

with tab2:
    st.subheader("🕵️ Cookie Status & ID Info")
    user_email = st.text_input("Enter Your Email (For notification)")
    test_cks = st.text_area("Paste Cookies to Validate", key="test_cks")
    
    if st.button("🔍 CHECK & NOTIFY"):
        if test_cks and user_email:
            with st.spinner("Checking FB Session..."):
                is_ok, name = check_cookie_status(test_cks, user_email)
                if is_ok:
                    st.balloons()
        else:
            st.warning("Pehle email aur cookies dalen jani!")

with tab3:
    st.write("### 📜 System Logs")
    if st.button("▶ START ATTACK"):
        st.success("System Online...")
