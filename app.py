import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# MANI RAJPUT - DASHBOARD UI DESIGN
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput E2E", layout="wide")

# Custom CSS for Dashboard & Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    .main .block-container {
        background: transparent !important;
        padding: 40px !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 65px;
        text-align: center;
        background: linear-gradient(to right, red, #fff, green);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,0,0.8);
        margin-bottom: 30px;
    }

    /* Dashboard Grid Buttons */
    .dashboard-btn {
        background: rgba(0, 0, 0, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: 0.4s;
        cursor: pointer;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }

    .dashboard-btn:hover {
        border-color: #ff00ea;
        box-shadow: 0 0 35px #ff00ea;
        transform: translateY(-10px);
    }

    .feature-box {
        background: rgba(0,0,0,0.9);
        border: 3px solid;
        border-image: linear-gradient(to bottom, red, blue, green) 1;
        padding: 40px;
        border-radius: 20px;
        margin-top: 20px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        font-weight: bold !important;
        height: 60px !important;
        border: 2px solid white !important;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# SESSION STATE FOR NAVIGATION
# ────────────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to(page_name):
    st.session_state.page = page_name

# ────────────────────────────────────────────────
# HOME DASHBOARD (8 FEATURES)
# ────────────────────────────────────────────────
if st.session_state.page == 'home':
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💬 MESSENGER"): go_to('messenger')
    with col2:
        if st.button("📝 POST ATTACK"): go_to('post')
    with col3:
        if st.button("🍪 COOKIE CHECK"): go_to('cookie')
    with col4:
        if st.button("🔎 UID FINDER"): go_to('uid')

    st.write(" ") # Space

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("👥 GROUP ATTACK"): go_to('group')
    with col6:
        if st.button("📧 EMAIL INFO"): go_to('email')
    with col7:
        if st.button("📂 FILE MANAGER"): go_to('file')
    with col8:
        if st.button("📟 TERMINAL"): go_to('terminal')

# ────────────────────────────────────────────────
# FEATURE PAGES (Hidden until clicked)
# ────────────────────────────────────────────────

# 1. MESSENGER
if st.session_state.page == 'messenger':
    st.markdown("<div class='feature-box'><h2>💬 MESSENGER ATTACKER</h2>", unsafe_allow_html=True)
    m_id = st.text_input("Group/Chat ID")
    m_file = st.file_uploader("Upload NP File (.txt)")
    m_cks = st.text_area("Cookies")
    if st.button("BACK TO HOME"): go_to('home')
    st.markdown("</div>", unsafe_allow_html=True)

# 2. POST ATTACK
if st.session_state.page == 'post':
    st.markdown("<div class='feature-box'><h2>📝 POST COMMENT ATTACKER</h2>", unsafe_allow_html=True)
    p_url = st.text_input("Post URL")
    p_file = st.file_uploader("Upload NP File (.txt)")
    p_cks = st.text_area("Cookies")
    if st.button("BACK TO HOME"): go_to('home')
    st.markdown("</div>", unsafe_allow_html=True)

# 3. COOKIE CHECKER
if st.session_state.page == 'cookie':
    st.markdown("<div class='feature-box'><h2>🍪 COOKIE VALIDATOR</h2>", unsafe_allow_html=True)
    v_cks = st.text_area("Paste Cookies")
    if st.button("CHECK STATUS"):
        st.success("Result: Cookies Active | Name: Mani Rajput | Email: m***@gmail.com")
    if st.button("BACK TO HOME"): go_to('home')
    st.markdown("</div>", unsafe_allow_html=True)

# 4. UID FINDER
if st.session_state.page == 'uid':
    st.markdown("<div class='feature-box'><h2>🔎 POST UID EXTRACTOR</h2>", unsafe_allow_html=True)
    p_link = st.text_input("Profile Link")
    if st.button("SCAN POSTS"): st.code("10002838392\n1029384848\n1029384847")
    if st.button("BACK TO HOME"): go_to('home')
    st.markdown("</div>", unsafe_allow_html=True)

# 8. TERMINAL (Final Example)
if st.session_state.page == 'terminal':
    st.markdown("<div class='feature-box'><h2>📟 SYSTEM TERMINAL</h2>", unsafe_allow_html=True)
    st.write("### Live Logs")
    st.code("[System] Attacking Target 1000484889...\n[System] Sent 50 messages successfully.")
    if st.button("BACK TO HOME"): go_to('home')
    st.markdown("</div>", unsafe_allow_html=True)

# (Baqi pages isi tarah follow honge...)

st.markdown("<br><center style='color:#fff; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud Elite</center>", unsafe_allow_html=True)
