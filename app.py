import streamlit as st
import threading
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ────────────────────────────────────────────────
# MANI RAJPUT - AI RGB DASHBOARD
# ────────────────────────────────────────────────
st.set_page_config(page_title="Mani Rajput AI Elite", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Rajdhani:wght@700&display=swap');

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.alphacoders.com/131/1311053.png') no-repeat center center fixed !important;
        background-size: cover !important;
    }

    .mani-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(40px, 8vw, 80px);
        text-align: center;
        background: linear-gradient(to right, red, #fff, green, blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,0,0.8);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff0000, #0000ff, #00ff00) !important;
        color: white !important;
        font-family: 'Orbitron';
        font-weight: bold !important;
        height: 60px !important;
        border: 2px solid white !important;
        border-radius: 15px !important;
    }

    input, textarea {
        background-color: rgba(0, 0, 0, 0.9) !important;
        color: #00f2ff !important;
        border: 2px solid #ff00ea !important;
        font-weight: bold !important;
    }

    .ai-box {
        background: rgba(255, 0, 234, 0.1);
        border: 2px dashed #00f2ff;
        padding: 20px;
        border-radius: 15px;
        margin-top: 10px;
    }
</style>
<h1 class="mani-title">MANI RAJPUT</h1>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'
def go(p): st.session_state.page = p

# ────────────────────────────────────────────────
# HOME DASHBOARD
# ────────────────────────────────────────────────
if st.session_state.page == 'home':
    st.markdown("<p style='text-align:center; color:#00f2ff; font-size:20px;'>ELITE AI WEAPON SYSTEM ONLINE</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 MESSENGER AI"): go('messenger')
        if st.button("📝 POST AI ATTACK"): go('post')
        if st.button("🤖 AI AUTO-REPLY"): go('ai_reply')
        if st.button("🍪 COOKIE CHECKER"): go('cookie')
    with c2:
        if st.button("🔎 UID FINDER"): go('uid')
        if st.button("📂 FILE MANAGER"): go('file')
        if st.button("📧 ID INFO"): go('email')
        if st.button("📟 TERMINAL"): go('terminal')

# ────────────────────────────────────────────────
# AI AUTO-REPLY PAGE (New Feature)
# ────────────────────────────────────────────────
if st.session_state.page == 'ai_reply':
    st.markdown("<div style='background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border:3px solid #ff00ea;'>", unsafe_allow_html=True)
    st.header("🤖 AI SMART COUNTER-ATTACK")
    st.write("Ye bot khud hi bande ka naam [Name] lekar usay savage reply dega.")
    
    ai_lines = st.text_area("Savage Lines (Ek line mein ek, [Name] lazmi likhen)", 
                            value="Oye [Name], Mani Rajput ke bot se panga mat le!\nBeta [Name], teri auqat nahi Mani Rajput se baat karne ki.\nSuno [Name], gaali dena band kar warna system hang kar doonga!")
    
    status = st.toggle("Activate AI Smart Defender")
    if status: st.success("Mani Rajput AI Defender is ACTIVE! 🔥")
    
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# MESSENGER PAGE (Full AI Integrated)
# ────────────────────────────────────────────────
if st.session_state.page == 'messenger':
    st.markdown("<div style='background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border:3px solid #00f2ff;'>", unsafe_allow_html=True)
    st.header("💬 MESSENGER SYSTEM")
    t_id = st.text_input("Target ID")
    h_name = st.text_input("Hater Name")
    dly = st.number_input("Speed (Delay Sec)", value=5)
    file = st.file_uploader("Upload NP File (.txt)")
    cks = st.text_area("Cookies")
    
    col1, col2 = st.columns(2)
    if col1.button("▶ START ATTACK"): st.success("Mani Rajput Bot Initiated!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# POST PAGE
# ────────────────────────────────────────────────
if st.session_state.page == 'post':
    st.markdown("<div style='background:rgba(0,0,0,0.9); padding:30px; border-radius:20px; border:3px solid #00ff00;'>", unsafe_allow_html=True)
    st.header("📝 POST COMMENT SYSTEM")
    p_url = st.text_input("Post Link / UID")
    p_hater = st.text_input("Hater Name")
    p_dly = st.number_input("Delay", value=5, key="p_d")
    p_file = st.file_uploader("Upload File", key="p_f")
    p_cks = st.text_area("Cookies", key="p_c")

    col1, col2 = st.columns(2)
    if col1.button("🔥 START COMMENTING"): st.success("Post Attack Online!")
    if col2.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# TERMINAL
# ────────────────────────────────────────────────
if st.session_state.page == 'terminal':
    st.markdown("<div style='background:black; padding:30px; border-radius:20px; border:2px solid #fff;'>", unsafe_allow_html=True)
    st.header("📟 SYSTEM LOGS")
    st.code("[AI] Target detected: Pappu\n[AI] Pappu ne bad-tameezi ki, counter line sent.\n[Success] 150 Attacks Delivered.")
    if st.button("🏠 BACK TO HOME"): go('home')
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#fff; font-family:Orbitron;'>© 2026 Mani Rajput X Yamdhud Elite</center>", unsafe_allow_html=True)
