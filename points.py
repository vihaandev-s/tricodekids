import streamlit as st
from accounts import load_user_progress, save_user_progress

PROGRESS_FILE = "tricodekids_progress.json"

def load_progress():
    current_user = st.session_state.get("current_user")
    return load_user_progress(current_user)

def save_progress(quiz_id=None, points_earned=None):
    """Saves quiz completion and session state to the logged-in user's account."""
    if quiz_id:
        if "completed_quizzes" not in st.session_state:
            st.session_state.completed_quizzes = set()
        st.session_state.completed_quizzes.add(quiz_id)
        if "quiz_solved" not in st.session_state:
            st.session_state.quiz_solved = set()
        st.session_state.quiz_solved.add(quiz_id)
    if points_earned:
        st.session_state.score = st.session_state.get("score", 0) + points_earned
        
    data = {
        "score": st.session_state.get("score", 0),
        "quiz_solved": list(st.session_state.get("quiz_solved", set())),
        "first_try_solved": list(st.session_state.get("first_try_solved", set())),
        "completed": list(st.session_state.get("completed", set())),
        "bonus_solved": list(st.session_state.get("bonus_solved", set())),
        "quiz_attempts": st.session_state.get("quiz_attempts", {})
    }
    current_user = st.session_state.get("current_user")
    save_user_progress(current_user, data)

def init_session_state():
    """Initializes session state variables and loads saved progress."""
    if "initialized" not in st.session_state:
        saved = load_progress()
        if saved:
            st.session_state.score = saved["score"]
            st.session_state.quiz_solved = saved["quiz_solved"]
            st.session_state.first_try_solved = saved["first_try_solved"]
            st.session_state.completed = saved["completed"]
            st.session_state.bonus_solved = saved["bonus_solved"]
            st.session_state.quiz_attempts = saved["quiz_attempts"]
        else:
            st.session_state.score = 0
            st.session_state.quiz_solved = set()
            st.session_state.first_try_solved = set()
            st.session_state.completed = set()
            st.session_state.bonus_solved = set()
            st.session_state.quiz_attempts = {}
        st.session_state.welcomed = False
        st.session_state.last_awarded = 0
        st.session_state.initialized = True

def render_score_box(points_awarded=0):
    """Renders the top Master Arcade Score HUD."""
    score = st.session_state.get("score", 0)
    solved_count = len(st.session_state.get("quiz_solved", set()))
    
    score_html = f"""
        <div class="arcade-hud-box">
            <h4 style="margin: 0;">⭐ CURRENT SCORE: {score} pts ⭐</h4>
            <p style="margin: 6px 0 0; font-size: 1.1rem;">
                Quizzes Solved: <b>{solved_count}/15</b> &nbsp;|&nbsp; +{points_awarded} Points Earned on last challenge!
            </p>
        </div>
    """
    st.markdown(score_html, unsafe_allow_html=True)

def render_score_hud(palette):
    """Alternative Score HUD compatible with custom palettes."""
    score = st.session_state.get("score", 0)
    completed = len(st.session_state.get("quiz_solved", set()))

    st.markdown(
        f"""
        <div style="
            background: {palette.get('card', '#1e293b')};
            border: 2px solid {palette.get('accent', '#fde047')};
            border-radius: 10px;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        ">
            <div>
                <span style="font-weight: 800; color: {palette.get('accent', '#fde047')};">🕹️ MASTER ARCADE HUD</span>
            </div>
            <div>
                <span style="margin-right: 20px;">⭐ Score: <strong>{score} pts</strong></span>
                <span>🏆 Levels Cleared: <strong>{completed}/15</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_badges_page():
    """Renders the Arcade Badge Showcase."""
    st.header("🎖️ Arcade Badge Showcase")
    st.write("Complete quizzes and Elite Bonus Challenges to unlock glowing arcade trophies!")

    col1, col2, col3 = st.columns(3)
    badges = [
        ("Python", "🐍 Python Master", col1),
        ("Java", "☕ Java Champion", col2),
        ("JavaScript", "⚡ JS Ninja", col3)
    ]

    for lang, title, col in badges:
        unlocked = lang in st.session_state.get("bonus_solved", set())
        border = "#fde047" if unlocked else "#334155"
        glow = "0 0 25px rgba(253, 224, 71, 0.7)" if unlocked else "none"
        status_text = "⭐ UNLOCKED! ⭐" if unlocked else "🔒 Locked (Complete Bonus Challenge)"
        status_color = "#fde047" if unlocked else "#94a3b8"

        with col:
            card_html = f"""
                <div class="arcade-badge-card" style="border: 3px solid {border}; box-shadow: {glow};">
                    <h2 style="margin-top:0;">{title}</h2>
                    <p style="font-size:1.1rem; font-weight:700; color:{status_color}; margin-bottom:0;">{status_text}</p>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
