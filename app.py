import streamlit as st
import os
import time
from sidebar import render_sidebar
from points import init_session_state, render_badges_page, save_progress, render_score_box, PROGRESS_FILE
from code_runner import render_code_runner
from quiz import render_quiz
from welcome import render_welcome, play_audio
from history import get_language_history
from lessons import lessons
from translation import get_text

st.set_page_config(page_title="TriCodeKids - Pro Edition", page_icon="⭐", layout="wide")

init_session_state()

# ⏱️ Native Time-based Pop-up Logic (Shows for 30s every 60s)
if "last_toggle_time" not in st.session_state:
    st.session_state.last_toggle_time = time.time()
if "tip_visible" not in st.session_state:
    st.session_state.tip_visible = True

current_time = time.time()
elapsed = current_time - st.session_state.last_toggle_time

# Toggle visibility every 30 seconds
if st.session_state.tip_visible and elapsed > 30:
    st.session_state.tip_visible = False
    st.session_state.last_toggle_time = current_time
elif not st.session_state.tip_visible and elapsed > 60:
    st.session_state.tip_visible = True
    st.session_state.last_toggle_time = current_time

# 🏆 MASTER ARCADE SCORE HUD AT THE VERY TOP
render_score_box(points_awarded=st.session_state.get("last_awarded", 0))

# 🏆 Check completion status
all_quizzes_solved = len(st.session_state.get("quiz_solved", set())) >= 15
all_bonuses_solved = len(st.session_state.get("bonus_solved", set())) >= 3
is_grand_champion = all_quizzes_solved and all_bonuses_solved

# 🔔 Pop-up notification
if is_grand_champion:
    if not st.session_state.get("champion_toast_shown", False):
        st.toast("🏆 You have earned all 3 elite badges, well done!", icon="⭐")
        st.session_state.champion_toast_shown = True
else:
    if not st.session_state.get("bonus_tip_shown", False):
        st.toast("🎖️ Solve the three bonus challenges to earn the three elite badges!", icon="⭐")
        st.session_state.bonus_tip_shown = True

if st.session_state.tip_visible:
    if is_grand_champion:
        st.markdown(
            """
            <div class="arcade-tip-box">
                <span style="font-weight: bold; font-size: 1.15rem;">🏆 CONGRATULATIONS:</span> 
                You have earned all 3 elite badges, well done!
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="arcade-tip-box">
                <span style="font-weight: bold;">⭐ ARCADE RULES:</span> 
                Quiz Scoring: 🥇 1st Try = <b>15 pts</b> | 🥈 2nd Try = <b>10 pts</b> | 🥉 3rd Try = <b>5 pts</b>!
                <br><span style="opacity: 0.9; font-size: 0.95rem;">(Solve all 3 Bonus Challenges to unlock the Elite Badges!)</span>
            </div>
            """,
            unsafe_allow_html=True
        )

col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=90)
    else:
        st.markdown(
            '<div style="font-size: 3.5rem; text-align: center; text-shadow: 0 0 20px #fde047;">⭐</div>',
            unsafe_allow_html=True
        )

with col_title:
    st.markdown(
        """
        <h1 style="
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8 0%, #60a5fa 45%, #fde047 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
            margin: 0px 0px 5px 0px;
        ">TriCodeKids Pro</h1>
        """,
        unsafe_allow_html=True
    )
    
    subtitle_text = get_text("⭐ Interactive Coding Academy for Grade 5 — Python, Java & JavaScript ⭐")
    subtitle_html = f"""
        <p style="
            font-size: 1.25rem;
            font-weight: 600;
            color: #38bdf8;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
            margin: 0px 0px 15px 0px;
            letter-spacing: 0.5px;
        ">{subtitle_text}</p>
    """
    st.markdown(subtitle_html, unsafe_allow_html=True)

st.divider()

section, language, topic = render_sidebar()

all_quizzes_solved = len(st.session_state.get("quiz_solved", set())) >= 15
all_bonuses_solved = len(st.session_state.get("bonus_solved", set())) >= 3

if all_quizzes_solved and all_bonuses_solved:
    st.balloons()
    st.toast("🏆 You have earned all 3 elite badges, well done!", icon="⭐")
    champion_banner = (
        '<div style="background: linear-gradient(135deg, #713f12 0%, #854d0e 100%); '
        'border: 3px solid #fde047; box-shadow: 0 0 35px rgba(253, 224, 71, 0.9); '
        'padding: 30px; border-radius: 15px; color: #ffffff; text-align: center; margin: 20px 0;">'
        '<h1 style="color: #fde047; text-shadow: 0 0 20px #fde047; margin-top: 0;">🏆 You have earned all 3 elite badges, well done! 🏆</h1>'
        '<p style="font-size: 1.3rem; margin-top: 15px; color: #fef08a;">'
        'Incredible job! You have mastered all 15 quizzes and unlocked all 3 Elite Bonus Badges across Python, Java, and JavaScript! You are a true coding legend.'
        '</p></div>'
    )
    st.markdown(champion_banner, unsafe_allow_html=True)
    
    reset_header = (
        '<h3 style="color: #fde047; text-shadow: 0 0 12px rgba(253, 224, 71, 0.7); '
        'margin-top: 15px; margin-bottom: 15px;">🔄 Do you want to start over?</h3>'
    )
    st.markdown(reset_header, unsafe_allow_html=True)

    col_reset1, col_reset2 = st.columns(2)
    with col_reset1:
        if st.button("🔄 Yes, Start Over Fresh!"):
            st.session_state.score = 0
            st.session_state.quiz_solved = set()
            st.session_state.first_try_solved = set()
            st.session_state.completed = set()
            st.session_state.bonus_solved = set()
            st.session_state.quiz_attempts = {}
            st.session_state.welcomed = False
            st.session_state.last_awarded = 0
            st.session_state.last_toggle_time = time.time()
            st.session_state.tip_visible = True
            st.session_state.bonus_tip_shown = False
            st.session_state.champion_toast_shown = False
            for k in list(st.session_state.keys()):
                if k.startswith("quiz_feedback_") or k.startswith("radio_"):
                    del st.session_state[k]
            
            if os.path.exists(PROGRESS_FILE):
                try:
                    os.remove(PROGRESS_FILE)
                except Exception:
                    pass
            
            st.success("Progress reset successfully! Restarting app...")
            st.rerun()
    with col_reset2:
        reset_info = (
            '<div class="arcade-box">'
            '<span style="font-size: 1.2rem;">⭐</span> '
            '<b>Keep exploring or view your badges in the sidebar anytime!</b></div>'
        )
        st.markdown(reset_info, unsafe_allow_html=True)
    st.stop()

language_history = get_language_history()

if section == "🎖️ Badge Showcase & Selector":
    render_badges_page()

elif section == "⭐ Bonus Challenge":
    st.header("⭐ Elite Bonus Challenges (+25 Points Each!)")
    st.write("Choose a language and write a custom code snippet using a **Global Variable** to earn your exclusive badge!")
    
    bonus_lang = st.selectbox("Select Bonus Challenge Language:", ["Python", "Java", "JavaScript"])
    
    bonus_starter = ""
    if bonus_lang == "Python":
        st.subheader("🐍 Python Elite Bonus: Global Variable Challenge")
        bonus_starter = '# TODO: Create a global variable and use it inside your code\n\n'
    elif bonus_lang == "Java":
        st.subheader("☕ Java Master Bonus: Global Variable Challenge")
        bonus_starter = 'public class Main {\n  // TODO: Create a static/global variable here\n  \n  public static void main(String[] args) {\n    // Use your global variable here\n    \n  }\n}'
    elif bonus_lang == "JavaScript":
        st.subheader("⚡ JS Ninja Bonus: Global Variable Challenge")
        bonus_starter = '// TODO: Create a global variable outside any function\n\n'

    user_bonus_code = st.text_area("Write your Bonus Code:", value=bonus_starter, height=180)
    
    if st.button("⭐ Submit " + bonus_lang + " Bonus"):
        if bonus_lang in st.session_state.bonus_solved:
            already_msg = (
                '<div class="arcade-box" style="margin: 15px 0;">'
                '<h3>⭐ ALREADY CONQUERED! ⭐</h3>'
                '<p style="font-size: 1.1rem; margin-top: 8px; margin-bottom: 0;">You have already unlocked this Badge!</p>'
                '</div>'
            )
            st.markdown(already_msg, unsafe_allow_html=True)
        else:
            success_condition = False
            if bonus_lang == "Python":
                success_condition = ("global " in user_bonus_code or ("=" in user_bonus_code and "def " not in user_bonus_code)) and len(user_bonus_code.strip()) > len(bonus_starter.strip())
            elif bonus_lang == "Java":
                success_condition = "static" in user_bonus_code and len(user_bonus_code.strip()) > len(bonus_starter.strip())
            elif bonus_lang == "JavaScript":
                success_condition = ("var " in user_bonus_code or "let " in user_bonus_code or "const " in user_bonus_code) and len(user_bonus_code.strip()) > len(bonus_starter.strip())

            if success_condition:
                st.session_state.score += 25
                st.session_state.bonus_solved.add(bonus_lang)
                st.session_state.last_awarded = 25
                save_progress()
                st.balloons()
                success_msg = (
                    '<div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); '
                    'border: 2px solid #34d399; box-shadow: 0 0 20px rgba(52, 211, 153, 0.6); '
                    'padding: 20px; border-radius: 12px; color: #ffffff; text-align: center; margin: 15px 0;">'
                    '<h3 style="margin: 0; color: #a7f3d0; text-shadow: 0 0 10px #34d399;">🎖️ ELITE BONUS UNLOCKED! 🎖️</h3>'
                    '<p style="font-size: 1.1rem; margin-top: 8px; margin-bottom: 0;">Amazing work! You earned (+25 Bonus Points)!</p>'
                    '</div>'
                )
                st.markdown(success_msg, unsafe_allow_html=True)
                
                bonus_audio_file = "bonus_audio.m4a" if os.path.exists("bonus_audio.m4a") else ("bonus_audio.mp3" if os.path.exists("bonus_audio.mp3") else None)
                if bonus_audio_file:
                    play_audio(bonus_audio_file)
                st.rerun()
            else:
                fail_msg = (
                    '<div style="background: linear-gradient(135deg, #7f1d1d 0%, #b91c1c 100%); '
                    'border: 2px solid #f87171; box-shadow: 0 0 20px rgba(248, 113, 113, 0.6); '
                    'padding: 20px; border-radius: 12px; color: #ffffff; text-align: center; margin: 15px 0;">'
                    '<h3 style="margin: 0; color: #fee2e2; text-shadow: 0 0 10px #f87171;">⚠️ GLITCH IN THE MATRIX! ⚠️</h3>'
                    '<p style="font-size: 1.1rem; margin-top: 8px; margin-bottom: 0;">Not quite! Make sure your code declares a global variable and prints/logs it properly.</p>'
                    '</div>'
                )
                st.markdown(fail_msg, unsafe_allow_html=True)

else:
    render_welcome()

    hist = language_history[language]
    history_title = get_text("Fun History of")
    created_by_str = get_text("Created by")
    in_str = get_text("in")
    story_translated = get_text(hist['story'])
    history_html = (
        f'<div class="colorful-history-box">'
        f'<h3 style="color: #fde047; text-shadow: 0 0 12px rgba(253, 224, 71, 0.7); margin-top: 0;">📜 {history_title} {language}</h3>'
        f'<p style="font-size: 1.05rem; line-height: 1.5; margin-bottom: 0;">'
        f'{created_by_str} <b>{hist["creator"]}</b> {in_str} <b>{hist["year"]}</b>! {story_translated}'
        f'</p></div>'
    )
    st.markdown(history_html, unsafe_allow_html=True)

    selected_label = get_text("Selected:")
    st.header(f"{selected_label} {language} - {topic}")
    current_lesson = lessons[language][topic]
    summary_text = get_text(current_lesson["summary"])
    challenge_text = get_text(current_lesson["challenge"])
    video_filename = current_lesson["video"]

    col_main, col_vid = st.columns([2, 1])
    with col_main:
        briefing_label = get_text("LESSON BRIEFING:")
        challenge_label = get_text("Challenge:")
        summary_html = (
            f'<div class="arcade-briefing-box">'
            f'<strong>💡 {briefing_label}</strong><br>{summary_text}'
            f'</div>'
        )
        st.markdown(summary_html, unsafe_allow_html=True)
        st.write(f"### {challenge_label} {challenge_text}")

    with col_vid:
        is_web_url = isinstance(video_filename, str) and (video_filename.startswith("http://") or video_filename.startswith("https://"))
        if is_web_url or os.path.exists(video_filename):
            st.video(video_filename)
            st.caption(get_text("Lets learn from W3Schools video tutorial"))
        else:
            video_html = (
                '<div class="arcade-video-box">'
                '<div style="font-size: 1.2rem; font-weight: 700;">🎥 VIDEO TUTORIAL</div>'
                '<p style="margin: 8px 0 0 0; font-size: 0.95rem;">Coming soon! (<code>{}</code>)</p>'
                '</div>'
            ).format(video_filename)
            st.markdown(video_html, unsafe_allow_html=True)

    render_code_runner(language, current_lesson)
    render_quiz(language, topic, current_lesson)