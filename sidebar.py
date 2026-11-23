import streamlit as st
from lessons import lessons
from themes import render_theme_selector
from ai_tutor import ask_tribot

SITE_LANGUAGES = [
    "English",
    "Hindi (हिन्दी)",
    "Tamil (தமிழ்)",
    "Kannada (ಕನ್ನಡ)",
    "Malayalam (മലയാളം)",
    "Telugu (తెలుగు)"
]

def render_sidebar():
    # 🕹️ Arcade Cabinet Marquee Header
    st.sidebar.markdown(
        """
        <div style="
            text-align: center;
            padding: 8px 4px 4px 4px;
            margin-bottom: 8px;
        ">
            <div style="
                font-size: 1.15rem;
                font-weight: 900;
                letter-spacing: 2px;
                color: var(--theme-accent-gold);
                text-shadow: 0 0 10px var(--theme-accent-gold);
                text-transform: uppercase;
            ">
                🕹️ CONTROL PANEL 🕹️
            </div>
            <div style="
                font-size: 0.75rem;
                letter-spacing: 2.5px;
                color: var(--theme-accent-blue);
                font-weight: 800;
                margin-top: 2px;
            ">
                ● PLAYER 1 ACTIVE ●
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🎨 Render Arcade Theme Selector at the top of the sidebar
    render_theme_selector()

    # 🌐 Website Language Selector Box
    st.sidebar.markdown(
        '<p style="color:var(--theme-accent-gold); font-weight:800; font-size:0.85rem; letter-spacing:1px; margin-top:10px; margin-bottom:4px;">🌐 WEBSITE LANGUAGE</p>',
        unsafe_allow_html=True
    )
    current_site_lang = st.session_state.get("site_language", "English")
    default_lang_idx = SITE_LANGUAGES.index(current_site_lang) if current_site_lang in SITE_LANGUAGES else 0
    selected_site_lang = st.sidebar.selectbox(
        "Website Language:",
        SITE_LANGUAGES,
        index=default_lang_idx,
        label_visibility="collapsed",
        key="site_language_select"
    )
    st.session_state["site_language"] = selected_site_lang
    st.session_state["current_language"] = selected_site_lang.split(" ")[0]

    # 🤖 Tribot AI Tutor Expander
    with st.sidebar.expander("🤖 Ask Tribot (AI Tutor)", expanded=bool(st.session_state.get("tribot_last_answer"))):
        tribot_q = st.text_input(
            "Ask Tribot any coding question:",
            key="tribot_input",
            placeholder="e.g. What is a loop in Python?"
        )
        col_t1, col_t2 = st.columns([3, 2])
        with col_t1:
            ask_btn = st.button("🚀 Ask Tribot", key="tribot_btn")
        with col_t2:
            if st.button("🧹 Clear", key="tribot_clear"):
                st.session_state["tribot_last_answer"] = ""
                st.session_state["tribot_last_question"] = ""
                st.rerun()

        if ask_btn:
            if tribot_q.strip():
                with st.spinner("🤖 Tribot is thinking..."):
                    ans = ask_tribot(tribot_q.strip())
                st.session_state["tribot_last_question"] = tribot_q.strip()
                st.session_state["tribot_last_answer"] = ans
            else:
                st.warning("Please type a question before asking Tribot.")

        if st.session_state.get("tribot_last_answer"):
            st.markdown(f"**Q:** *{st.session_state.get('tribot_last_question')}*")
            st.markdown(st.session_state.get("tribot_last_answer"))

    # 🏆 Calculate Gamer Level & Progress
    score = st.session_state.get("score", 0)
    quizzes_solved = len(st.session_state.get("quiz_solved", set()))
    badges_earned = len(st.session_state.get("bonus_solved", set()))
    progress_pct = min(int((quizzes_solved / 15) * 100), 100)

    if score >= 150:
        gamer_rank = "👑 GRAND CHAMPION"
        rank_color = "var(--theme-accent-gold)"
    elif score >= 80:
        gamer_rank = "⚡ PIXEL MASTER"
        rank_color = "var(--theme-accent-blue)"
    elif score >= 35:
        gamer_rank = "🕹️ ARCADE RUNNER"
        rank_color = "#34d399"
    else:
        gamer_rank = "🐣 ROOKIE CADET"
        rank_color = "#a5b4fc"

    # ⭐ Arcade Player Stats HUD Box
    stats_html = f"""
        <div class="arcade-stats-box" style="position: relative; overflow: hidden; padding: 14px 12px;">
            <div style="
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid var(--theme-accent-blue);
                border-radius: 6px;
                padding: 3px 8px;
                display: inline-block;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 1.2px;
                color: {rank_color};
                margin-bottom: 8px;
            ">
                {gamer_rank}
            </div>
            <div style="
                font-size: 1.75rem; 
                font-weight: 900; 
                color: var(--theme-accent-gold); 
                text-shadow: 0 0 10px var(--theme-accent-gold);
                margin: 2px 0 6px 0;
            ">
                🪙 {score} <span style="font-size: 0.85rem; font-weight: 700;">PTS</span>
            </div>
            <div style="
                display: flex; 
                justify-content: space-around; 
                font-size: 0.86rem; 
                margin-bottom: 8px;
            ">
                <span>🎯 Quizzes: <b>{quizzes_solved}/15</b></span>
                <span>🎖️ Badges: <b>{badges_earned}/3</b></span>
            </div>
            <div style="
                background: rgba(0, 0, 0, 0.45); 
                border-radius: 10px; 
                height: 7px; 
                width: 100%; 
                overflow: hidden; 
                border: 1px solid var(--theme-accent-blue);
            ">
                <div style="
                    background: linear-gradient(90deg, var(--theme-accent-blue), var(--theme-accent-gold)); 
                    height: 100%; 
                    width: {progress_pct}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
    """
    st.sidebar.markdown(stats_html, unsafe_allow_html=True)

    # 🕹️ Arcade Navigation Radio
    st.sidebar.markdown(
        '<p style="color:var(--theme-accent-gold); font-weight:800; font-size:0.9rem; letter-spacing:1px; margin-bottom:4px;">🎮 ARCADE MENU</p>',
        unsafe_allow_html=True
    )
    section = st.sidebar.radio(
        "Navigate Arcade:",
        [
            "⭐ Lessons & Quizzes",
            "🎖️ Badge Showcase & Selector",
            "⭐ Bonus Challenge"
        ],
        label_visibility="collapsed",
        key="arcade_nav_section"
    )

    # 💾 Cartridge (Language) Selection
    st.sidebar.markdown(
        '<p style="color:var(--theme-accent-gold); font-weight:800; font-size:0.9rem; letter-spacing:1px; margin-bottom:4px;">💾 CARTRIDGE (LANG)</p>',
        unsafe_allow_html=True
    )
    language = st.sidebar.selectbox("Language:", list(lessons.keys()), label_visibility="collapsed")

    # 🎯 Mission (Topic) Selection
    st.sidebar.markdown(
        '<p style="color:var(--theme-accent-gold); font-weight:800; font-size:0.9rem; letter-spacing:1px; margin-top:10px; margin-bottom:4px;">🎯 MISSION (TOPIC)</p>',
        unsafe_allow_html=True
    )
    topic_list = list(lessons[language].keys())
    
    solved_set = st.session_state.get("quiz_solved", set())
    formatted_topics = []
    for t in topic_list:
        if "{}_{}".format(language, t) in solved_set:
            formatted_topics.append("✅ " + t)
        else:
            formatted_topics.append("👾 " + t)

    selected_formatted = st.sidebar.selectbox("Topic:", formatted_topics, label_visibility="collapsed")
    topic = selected_formatted.replace("✅ ", "").replace("👾 ", "")

    # 🪙 Bottom Cabinet Footer
    st.sidebar.markdown(
        """
        <div style="
            text-align: center;
            padding: 12px 6px 4px 6px;
            margin-top: 20px;
            border-top: 1px dashed var(--theme-accent-blue);
            font-size: 0.72rem;
            color: var(--theme-accent-gold);
            letter-spacing: 1.5px;
            font-weight: 700;
        ">
            🕹️ FREE PLAY MODE • 1P READY
        </div>
        """,
        unsafe_allow_html=True
    )

    return section, language, topic
