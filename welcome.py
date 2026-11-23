import streamlit as st
import os
from translation import get_text

def play_audio(audio_file):
    if os.path.exists(audio_file):
        try:
            st.audio(audio_file, format="audio/mp3", autoplay=True)
        except Exception:
            st.audio(audio_file, format="audio/mp3")

def render_welcome():
    welcome_title = get_text("⭐ WELCOME TO THE ARCADE CODING ACADEMY! ⭐")
    welcome_sub = get_text("Ready to level up your programming skills? Pick a language, conquer coding challenges, and unlock elite arcade badges across Python, Java, and JavaScript!")
    st.markdown(
        f"""
        <div class="arcade-welcome-box">
            <h2 style="margin-top: 0;">{welcome_title}</h2>
            <p style="font-size: 1.1rem; margin-bottom: 0;">
                {welcome_sub}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Play welcome audio only once per session
    if not st.session_state.get("welcomed", False):
        welcome_file = "welcome.m4a" if os.path.exists("welcome.m4a") else ("welcome.mp3" if os.path.exists("welcome.mp3") else None)
        if welcome_file:
            play_audio(welcome_file)
        st.session_state.welcomed = True
