import streamlit as st
import streamlit.components.v1 as components
import os
import time
import random
import math
from sidebar import render_sidebar
from points import init_session_state, render_badges_page, save_progress, render_score_box
from code_runner import render_code_runner
from quiz import render_quiz
from welcome import render_welcome, play_audio
from history import get_language_history
from lessons import lessons
from translation import get_text
from accounts import render_auth_screen

st.set_page_config(page_title="TriCodeKids - Pro Edition", page_icon="⭐", layout="wide")

def run_boot_sequence():
    """Renders a sleek Hyundai-infotainment-style boot splash overlay with a custom SVG emblem once per session."""
    st.markdown(
        """
        <style>
        @keyframes hyundai-emblem-in {
            0% { opacity: 0; transform: scale(0.88); filter: drop-shadow(0 0 0px #38bdf8); }
            45% { opacity: 1; transform: scale(1.0); filter: drop-shadow(0 0 22px rgba(56, 189, 248, 0.75)); }
            100% { opacity: 1; transform: scale(1.02); filter: drop-shadow(0 0 30px rgba(125, 211, 252, 0.9)); }
        }
        @keyframes hyundai-sweep {
            0% { transform: translateX(-120%); opacity: 0; }
            30% { opacity: 1; }
            100% { transform: translateX(120%); opacity: 0; }
        }
        @keyframes hyundai-text-in {
            0%, 20% { opacity: 0; letter-spacing: 14px; }
            65%, 100% { opacity: 1; letter-spacing: 8px; }
        }
        @keyframes hyundai-line {
            0% { width: 0%; opacity: 0.4; }
            100% { width: 100%; opacity: 1; }
        }
        @keyframes boot-overlay-fade {
            0%, 82% { opacity: 1; visibility: visible; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; }
        }
        .tri-boot-overlay {
            position: fixed;
            inset: 0;
            z-index: 999999;
            background: radial-gradient(ellipse at 50% 42%, #0f1b2e 0%, #05080f 65%, #020408 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            overflow: hidden;
            animation: boot-overlay-fade 3.4s ease-in-out forwards;
        }
        .hyundai-horizon {
            position: relative;
            width: 340px;
            height: 2px;
            background: rgba(56, 189, 248, 0.18);
            margin-top: 26px;
            overflow: hidden;
            border-radius: 999px;
        }
        .hyundai-horizon-fill {
            height: 100%;
            background: linear-gradient(90deg, transparent, #38bdf8, #e0f2fe, #38bdf8, transparent);
            box-shadow: 0 0 14px #38bdf8;
            animation: hyundai-line 2.4s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
        .hyundai-beam {
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(125, 211, 252, 0.65), transparent);
            animation: hyundai-sweep 2.2s ease-in-out forwards;
            pointer-events: none;
        }
        </style>
        <div class="tri-boot-overlay">
            <div class="hyundai-beam"></div>
            <div style="animation: hyundai-emblem-in 2.2s ease-out forwards;">
                <svg width="190" height="108" viewBox="0 0 190 108" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="chromeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#f8fafc"/>
                            <stop offset="45%" stop-color="#94a3b8"/>
                            <stop offset="75%" stop-color="#e2e8f0"/>
                            <stop offset="100%" stop-color="#38bdf8"/>
                        </linearGradient>
                        <linearGradient id="innerGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#0ea5e9"/>
                            <stop offset="50%" stop-color="#7dd3fc"/>
                            <stop offset="100%" stop-color="#0ea5e9"/>
                        </linearGradient>
                    </defs>
                    <!-- Sleek automotive-style oval emblem -->
                    <ellipse cx="95" cy="54" rx="86" ry="44" fill="rgba(14, 165, 233, 0.08)" stroke="url(#chromeGrad)" stroke-width="4.5"/>
                    <ellipse cx="95" cy="54" rx="76" ry="36" fill="none" stroke="rgba(125, 211, 252, 0.35)" stroke-width="1.2"/>
                    <!-- Stylized coding chevrons & spark inside emblem -->
                    <path d="M 64 38 L 44 54 L 64 70" fill="none" stroke="url(#chromeGrad)" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M 126 38 L 146 54 L 126 70" fill="none" stroke="url(#chromeGrad)" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M 103 31 L 87 77" fill="none" stroke="url(#innerGlow)" stroke-width="5.5" stroke-linecap="round"/>
                </svg>
            </div>
            <h1 style="
                font-size: 2.1rem;
                font-weight: 600;
                margin: 22px 0 4px 0;
                background: linear-gradient(90deg, #94a3b8 0%, #f8fafc 50%, #7dd3fc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
                animation: hyundai-text-in 2.1s ease-out forwards;
            ">TRICODEKIDS</h1>
            <div class="hyundai-horizon">
                <div class="hyundai-horizon-fill"></div>
            </div>
            <p style="
                color: #7dd3fc;
                font-size: 0.78rem;
                font-weight: 500;
                margin-top: 14px;
                letter-spacing: 4px;
                opacity: 0.85;
            ">INITIALIZING CODING COCKPIT</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.boot_done = True

# 🚀 Arcade Boot Logo Splash Screen (shown once per session on startup)
if not st.session_state.get("boot_done", False):
    run_boot_sequence()

# ✨ Initialize Session State for Dark/Light Mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to arcade dark mode

# 🕹️ Sidebar Toggle for Light/Dark Mode
st.sidebar.subheader("🕹️ DISPLAY MODE 🕹️")
col_mode1, col_mode2 = st.sidebar.columns(2)
with col_mode1:
    if st.button("🌙 Dark", use_container_width=True):
        st.session_state.dark_mode = True
        st.rerun()
with col_mode2:
    if st.button("☀️ Light", use_container_width=True):
        st.session_state.dark_mode = False
        st.rerun()

# ✨ Arcade glow animation (colors come dynamically from the selected theme & mode)
st.markdown("""
<style>
.arcade-stats-box, .arcade-briefing-box, .arcade-video-box, .arcade-tip-box, .colorful-history-box {
    animation: arcade-glow 2s infinite alternate;
}
@keyframes arcade-glow {
    from { box-shadow: 0 0 10px var(--theme-accent-blue); }
    to { box-shadow: 0 0 22px var(--theme-accent-gold); }
}
</style>
""", unsafe_allow_html=True)


init_session_state()

if not st.session_state.get("current_user"):
    from themes import render_theme_selector
    render_theme_selector()
    render_auth_screen()
    st.stop()

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
            
            save_progress()
            
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

WHEEL_LANGS = ["Python", "Java", "JavaScript"]
LANG_WHEEL_SLICES = [
    ("Python", "#38bdf8", "#0f172a"),
    ("Java", "#f97316", "#0f172a"),
    ("JavaScript", "#fde047", "#0f172a"),
]

def build_spin_wheel_html(wheel_prefix, slice_specs, selected_idx, spin_id, animate_now, waiting_text, revealed_text, size=320):
    """Builds an animated SVG spin-the-wheel HTML snippet that reveals its result only after spinning."""
    n = len(slice_specs)
    step = 360 / n
    center_offset = step / 2
    target_angle = (360 * (4 + (spin_id % 3))) + (360 - (selected_idx * step + center_offset))
    start_angle = (target_angle - 1080) if animate_now else (0 if spin_id == 0 else target_angle)

    if spin_id == 0:
        initial_banner = waiting_text
    elif animate_now:
        initial_banner = "🌀 Spinning..."
    else:
        initial_banner = revealed_text

    svg_parts = []
    radius = 112
    label_radius = 68 if n > 3 else 62
    for idx, (label, fill_color, txt_color) in enumerate(slice_specs):
        a0 = math.radians(idx * step - 90)
        a1 = math.radians((idx + 1) * step - 90)
        amid = math.radians(idx * step + center_offset - 90)
        x0, y0 = radius * math.cos(a0), radius * math.sin(a0)
        x1, y1 = radius * math.cos(a1), radius * math.sin(a1)
        lx, ly = label_radius * math.cos(amid), label_radius * math.sin(amid)
        rot_deg = idx * step + center_offset
        large_arc = 1 if step > 180 else 0
        svg_parts.append(
            f'<path d="M 0 0 L {x0:.2f} {y0:.2f} A {radius} {radius} 0 {large_arc} 1 {x1:.2f} {y1:.2f} Z" '
            f'fill="{fill_color}" stroke="#0f172a" stroke-width="2"/>'
        )
        svg_parts.append(
            f'<text x="{lx:.2f}" y="{ly:.2f}" fill="{txt_color}" font-size="14" font-weight="800" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'transform="rotate({rot_deg} {lx:.2f} {ly:.2f})">{label}</text>'
        )
    svg_content = "\n        ".join(svg_parts)
    elem_id = f"{wheel_prefix}_{spin_id}"
    banner_id = f"{wheel_prefix}_banner_{spin_id}"
    reveal_script = ""
    if animate_now:
        reveal_script = f"""
        <script>
          setTimeout(function() {{
            var w = document.getElementById("{elem_id}");
            if (w) {{ w.style.transform = "rotate({target_angle}deg)"; }}
          }}, 50);
          setTimeout(function() {{
            var b = document.getElementById("{banner_id}");
            if (b) {{ b.textContent = {revealed_text!r}; }}
          }}, 2250);
        </script>
        """
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:8px; font-family:sans-serif;">
      <div id="{banner_id}" style="
        width: 92%;
        padding: 12px 16px;
        margin-bottom: 12px;
        border-radius: 12px;
        border: 2px solid #38bdf8;
        background: rgba(15, 23, 42, 0.85);
        color: #fde047;
        font-size: 18px;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.45);
      ">{initial_banner}</div>
      <div style="font-size:34px; line-height:1; margin-bottom:-8px; z-index:10; filter:drop-shadow(0 0 6px #fde047);">🔻</div>
      <div id="{elem_id}" style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        border: 6px solid #fde047;
        box-shadow: 0 0 26px rgba(253, 224, 71, 0.8);
        overflow: hidden;
        transform: rotate({start_angle}deg);
        transition: transform 2.2s cubic-bezier(0.17, 0.67, 0.12, 0.99);
      ">
        <svg viewBox="-115 -115 230 230" width="{size}" height="{size}" style="display:block;">
          {svg_content}
          <circle cx="0" cy="0" r="24" fill="#0f172a" stroke="#fde047" stroke-width="3"/>
          <text x="0" y="2" font-size="18" text-anchor="middle" dominant-baseline="middle">⭐</text>
        </svg>
      </div>
    </div>
    {reveal_script}
    """

if section == "📺 Language Introduction":
    st.markdown("# 📺 Language Introduction Videos")
    st.markdown("Welcome commanders! Watch your language introduction cartridge below:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🐍 Python Intro")
        if os.path.exists("python_intro.mp4"):
            st.video("python_intro.mp4")
            st.caption(get_text("Disclaimer: This video tutorial is from W3Schools."))
        else:
            st.info("🚧 Please place `python_intro.mp4` in your project folder.")
        
    with col2:
        st.markdown("### ☕ Java Intro")
        if os.path.exists("java_intro.mp4"):
            st.video("java_intro.mp4")
            st.caption(get_text("Disclaimer: This video tutorial is from W3Schools."))
        else:
            st.info("🚧 Please place `java_intro.mp4` in your project folder.")
        
    with col3:
        st.markdown("### 🌐 JavaScript Intro")
        if os.path.exists("js_intro.mp4"):
            st.video("js_intro.mp4")
            st.caption(get_text("Disclaimer: This video tutorial is from W3Schools."))
        else:
            st.info("🚧 Please place `js_intro.mp4` in your project folder.")

    st.markdown(
        """
        <div style="
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 25px;
            font-size: 0.95rem;
            text-align: center;
        ">
            <b>ℹ️ W3Schools Video Disclaimer:</b> All introductory video walkthroughs featured here are sourced from W3Schools tutorials to help students explore the fundamentals of Python, Java, and JavaScript safely in an arcade learning environment.
        </div>
        """,
        unsafe_allow_html=True
    )

elif section == "🎖️ Badge Showcase & Selector":
    render_badges_page()

elif section == "⭐ Bonus Challenge":
    st.header("⭐ Elite Bonus Challenges (+25 Points Each!)")
    st.write("Spin the **Language Wheel** and **Topic Wheel** to roll your coding challenge, then write your code to earn your exclusive badge!")

    WHEEL_TOPICS = [
        "1. Print Commands",
        "2. Syntax & Comments",
        "3. Variables",
        "4. Loops",
        "5. Global Variables",
    ]

    if "bonus_wheel_lang" not in st.session_state:
        st.session_state.bonus_wheel_lang = "Python"
    if "bonus_lang_spin_id" not in st.session_state:
        st.session_state.bonus_lang_spin_id = 0
    if "bonus_wheel_topic" not in st.session_state:
        st.session_state.bonus_wheel_topic = "5. Global Variables"
    if "bonus_wheel_spin_id" not in st.session_state:
        st.session_state.bonus_wheel_spin_id = 0
    if "last_spun_wheel" not in st.session_state:
        st.session_state.last_spun_wheel = None

    col_lang_wheel, col_topic_wheel = st.columns(2)

    with col_lang_wheel:
        if st.button("🎡 Spin Language Wheel!", use_container_width=True):
            st.session_state.bonus_wheel_lang = random.choice(WHEEL_LANGS)
            st.session_state.bonus_lang_spin_id += 1
            st.session_state.last_spun_wheel = "lang"
            st.rerun()
        bonus_lang = st.session_state.bonus_wheel_lang
        lang_html = build_spin_wheel_html(
            "lang_wheel",
            LANG_WHEEL_SLICES,
            WHEEL_LANGS.index(bonus_lang),
            st.session_state.bonus_lang_spin_id,
            animate_now=(st.session_state.last_spun_wheel == "lang" and st.session_state.bonus_lang_spin_id > 0),
            waiting_text="❓ Language: Spin to reveal!",
            revealed_text=f"💾 Language: {bonus_lang}",
            size=320,
        )
        components.html(lang_html, height=455)

    with col_topic_wheel:
        if st.button("🎡 Spin Topic Wheel!", use_container_width=True):
            st.session_state.bonus_wheel_topic = random.choice(WHEEL_TOPICS)
            st.session_state.bonus_wheel_spin_id += 1
            st.session_state.last_spun_wheel = "topic"
            st.rerun()
        selected_topic = st.session_state.bonus_wheel_topic
        topic_slices = [
            ("Print", "#38bdf8", "#0f172a"),
            ("Syntax", "#f7558b", "#ffffff"),
            ("Variables", "#22c55e", "#0f172a"),
            ("Loops", "#f97316", "#0f172a"),
            ("Global", "#ec4899", "#ffffff"),
        ]
        topic_html = build_spin_wheel_html(
            "topic_wheel",
            topic_slices,
            WHEEL_TOPICS.index(selected_topic),
            st.session_state.bonus_wheel_spin_id,
            animate_now=(st.session_state.last_spun_wheel == "topic" and st.session_state.bonus_wheel_spin_id > 0),
            waiting_text="❓ Topic: Spin to reveal!",
            revealed_text=f"🎯 Topic: {selected_topic}",
            size=320,
        )
        components.html(topic_html, height=455)

    BONUS_PROMPTS = {
        "1. Print Commands": {
            "Python": ("🖨️ Python Bonus: Print Command Challenge", '# TODO: Use print() to display a cool arcade message!\n\n'),
            "Java": ("🖨️ Java Bonus: Print Command Challenge", 'public class Main {\n  public static void main(String[] args) {\n    // TODO: Use System.out.println() to print a message\n    \n  }\n}'),
            "JavaScript": ("🖨️ JS Bonus: Print Command Challenge", '// TODO: Use console.log() to display a cool message!\n\n'),
        },
        "2. Syntax & Comments": {
            "Python": ("💬 Python Bonus: Comments & Syntax Challenge", '# TODO: Add a # comment and write a valid Python line below\n'),
            "Java": ("💬 Java Bonus: Comments & Syntax Challenge", 'public class Main {\n  public static void main(String[] args) {\n    // TODO: Add a comment and a valid Java statement\n  }\n}'),
            "JavaScript": ("💬 JS Bonus: Comments & Syntax Challenge", '// TODO: Add a // comment and write a valid JS line below\n'),
        },
        "3. Variables": {
            "Python": ("📦 Python Bonus: Variables Challenge", '# TODO: Create a variable (e.g. score = 100) and print it\n\n'),
            "Java": ("📦 Java Bonus: Variables Challenge", 'public class Main {\n  public static void main(String[] args) {\n    // TODO: Declare a variable (e.g. int score = 100;)\n    \n  }\n}'),
            "JavaScript": ("📦 JS Bonus: Variables Challenge", '// TODO: Declare a variable with let or const\n\n'),
        },
        "4. Loops": {
            "Python": ("🔁 Python Bonus: Loops Challenge", '# TODO: Write a for or while loop!\n\n'),
            "Java": ("🔁 Java Bonus: Loops Challenge", 'public class Main {\n  public static void main(String[] args) {\n    // TODO: Write a for or while loop\n    \n  }\n}'),
            "JavaScript": ("🔁 JS Bonus: Loops Challenge", '// TODO: Write a for or while loop!\n\n'),
        },
        "5. Global Variables": {
            "Python": ("🐍 Python Elite Bonus: Global Variable Challenge", '# TODO: Create a global variable and use it inside your code\n\n'),
            "Java": ("☕ Java Master Bonus: Global Variable Challenge", 'public class Main {\n  // TODO: Create a static/global variable here\n  \n  public static void main(String[] args) {\n    // Use your global variable here\n    \n  }\n}'),
            "JavaScript": ("⚡ JS Ninja Bonus: Global Variable Challenge", '// TODO: Create a global variable outside any function\n\n'),
        },
    }

    if st.session_state.bonus_lang_spin_id == 0 or st.session_state.bonus_wheel_spin_id == 0:
        st.markdown(
            '<div class="arcade-box" style="margin-top: 10px;">'
            '<h3>🎡 Spin Both Wheels Above!</h3>'
            '<p style="margin: 6px 0 0 0;">Spin the <b>Language Wheel</b> and the <b>Topic Wheel</b> to reveal your surprise coding challenge!</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        subheader_text, bonus_starter = BONUS_PROMPTS[selected_topic][bonus_lang]
        st.subheader(subheader_text)

        user_bonus_code = st.text_area("Write your Bonus Code:", value=bonus_starter, height=180, key=f"bonus_code_{bonus_lang}_{selected_topic}")
        
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
                has_new_code = len(user_bonus_code.strip()) > len(bonus_starter.strip())
                success_condition = False
                if selected_topic == "1. Print Commands":
                    if bonus_lang == "Python":
                        success_condition = "print(" in user_bonus_code and has_new_code
                    elif bonus_lang == "Java":
                        success_condition = "System.out.print" in user_bonus_code and has_new_code
                    elif bonus_lang == "JavaScript":
                        success_condition = "console.log(" in user_bonus_code and has_new_code
                elif selected_topic == "2. Syntax & Comments":
                    if bonus_lang == "Python":
                        success_condition = "#" in user_bonus_code and has_new_code
                    else:
                        success_condition = ("//" in user_bonus_code or "/*" in user_bonus_code) and has_new_code
                elif selected_topic == "3. Variables":
                    if bonus_lang == "Python":
                        success_condition = "=" in user_bonus_code and has_new_code
                    elif bonus_lang == "Java":
                        success_condition = any(t in user_bonus_code for t in ["int ", "String ", "double ", "boolean "]) and "=" in user_bonus_code and has_new_code
                    elif bonus_lang == "JavaScript":
                        success_condition = any(k in user_bonus_code for k in ["let ", "const ", "var "]) and "=" in user_bonus_code and has_new_code
                elif selected_topic == "4. Loops":
                    success_condition = ("for " in user_bonus_code or "for(" in user_bonus_code or "while " in user_bonus_code or "while(" in user_bonus_code) and has_new_code
                else:
                    if bonus_lang == "Python":
                        success_condition = ("global " in user_bonus_code or ("=" in user_bonus_code and "def " not in user_bonus_code)) and has_new_code
                    elif bonus_lang == "Java":
                        success_condition = "static" in user_bonus_code and has_new_code
                    elif bonus_lang == "JavaScript":
                        success_condition = ("var " in user_bonus_code or "let " in user_bonus_code or "const " in user_bonus_code) and has_new_code

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
                        '<p style="font-size: 1.1rem; margin-top: 8px; margin-bottom: 0;">Not quite! Make sure your code solves the spun challenge properly.</p>'
                        '</div>'
                    )
                    st.markdown(fail_msg, unsafe_allow_html=True)

else:
    render_welcome()

    with st.expander("🎡 Not sure what to learn first? Spin the Language Wheel!", expanded=True):
        if "home_wheel_lang" not in st.session_state:
            st.session_state.home_wheel_lang = "Python"
        if "home_lang_spin_id" not in st.session_state:
            st.session_state.home_lang_spin_id = 0
        if "home_wheel_animate" not in st.session_state:
            st.session_state.home_wheel_animate = False

        if st.button("🎡 Spin to Pick Your First Language!", use_container_width=True):
            st.session_state.home_wheel_lang = random.choice(WHEEL_LANGS)
            st.session_state.home_lang_spin_id += 1
            st.session_state.home_wheel_animate = True
            st.rerun()

        home_lang = st.session_state.home_wheel_lang
        animate_home = st.session_state.home_wheel_animate and st.session_state.home_lang_spin_id > 0
        st.session_state.home_wheel_animate = False

        home_wheel_html = build_spin_wheel_html(
            "home_lang_wheel",
            LANG_WHEEL_SLICES,
            WHEEL_LANGS.index(home_lang),
            st.session_state.home_lang_spin_id,
            animate_now=animate_home,
            waiting_text="❓ Language: Spin to see what to learn first!",
            revealed_text=f"🚀 Start with: {home_lang}!",
            size=320,
        )
        components.html(home_wheel_html, height=455)

    if st.session_state.home_lang_spin_id > 0 and language and topic:
        hist = language_history[language]
        history_title = get_text("Fun History of")
        created_by_str = get_text("Created by")
        in_str = get_text("in")
        story_translated = get_text(hist["story"])
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
                f'<div class="colorful-history-box">'
                f'<strong>💡 {briefing_label}</strong><br>{summary_text}'
                f'</div>'
            )
            st.markdown(summary_html, unsafe_allow_html=True)
            st.write(f"### {challenge_label} {challenge_text}")

        with col_vid:
            is_web_url = isinstance(video_filename, str) and (video_filename.startswith("http://") or video_filename.startswith("https://"))
            if is_web_url or os.path.exists(video_filename):
                st.video(video_filename)
                st.caption(get_text("Disclaimer: This video tutorial is from W3Schools."))
            else:
                video_html = (
                    '<div class="colorful-history-box">'
                    '<div style="font-size: 1.2rem; font-weight: 700;">🎥 VIDEO TUTORIAL</div>'
                    '<p style="margin: 8px 0 0 0; font-size: 0.95rem;">Coming soon! (<code>{}</code>)</p>'
                    '</div>'
                ).format(video_filename)
                st.markdown(video_html, unsafe_allow_html=True)

        render_code_runner(language, current_lesson)
        render_quiz(language, topic, current_lesson)
    else:
        st.markdown(
            '<div class="arcade-box" style="margin-top: 12px;">'
            '<h3>🎡 Spin the Language Wheel Above!</h3>'
            '<p style="margin: 6px 0 0 0;">Your coding language, topics, history, videos, and quizzes will appear automatically after you spin!</p>'
            '</div>',
            unsafe_allow_html=True
        )