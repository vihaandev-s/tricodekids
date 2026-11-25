import streamlit as st

THEMES = {
    "⭐ Cosmic Galaxy": {
        "bg_primary": "#0a0f1d",
        "bg_secondary": "#151e34",
        "accent_blue": "#38bdf8",
        "accent_gold": "#fde047",
        "text_color": "#f8fafc"
    },
    "🟢 Matrix Hacker": {
        "bg_primary": "#021a12",
        "bg_secondary": "#063726",
        "accent_blue": "#22c55e",
        "accent_gold": "#a3e635",
        "text_color": "#ecfdf5"
    },
    "🎸 Retro Synthwave": {
        "bg_primary": "#180326",
        "bg_secondary": "#2e0854",
        "accent_blue": "#ec4899",
        "accent_gold": "#fde047",
        "text_color": "#ffffff"
    },
    "🪵 Retro Amber / Brown": {
        "bg_primary": "#1c140d",
        "bg_secondary": "#2e1e12",
        "accent_blue": "#f59e0b",
        "accent_gold": "#fbbf24",
        "text_color": "#fef3c7"
    },
    "🍂 Ginger Gold": {
        "bg_primary": "#19120c",
        "bg_secondary": "#302014",
        "accent_blue": "#c5803a",
        "accent_gold": "#f6ad55",
        "text_color": "#fdf8f2"
    },
    "🔮 Royal Indigo": {
        "bg_primary": "#120d2b",
        "bg_secondary": "#1d1445",
        "accent_blue": "#6366f1",
        "accent_gold": "#a78bfa",
        "text_color": "#f5f3ff"
    },
    "🔥 Crimson Arcade": {
        "bg_primary": "#1c0909",
        "bg_secondary": "#331212",
        "accent_blue": "#ef4444",
        "accent_gold": "#fca5a5",
        "text_color": "#fff5f5"
    },
    "⚡ Electric Cobalt": {
        "bg_primary": "#050a24",
        "bg_secondary": "#0c174d",
        "accent_blue": "#3b82f6",
        "accent_gold": "#fde047",
        "text_color": "#f0f4ff"
    }
}

LIGHT_THEMES = {
    "⭐ Cosmic Galaxy": {
        "bg_primary": "#f0f7ff",
        "bg_secondary": "#dbeafe",
        "accent_blue": "#0284c7",
        "accent_gold": "#b45309",
        "text_color": "#0f172a"
    },
    "🟢 Matrix Hacker": {
        "bg_primary": "#f0fdf4",
        "bg_secondary": "#dcfce7",
        "accent_blue": "#15803d",
        "accent_gold": "#047857",
        "text_color": "#052e16"
    },
    "🎸 Retro Synthwave": {
        "bg_primary": "#fdf4ff",
        "bg_secondary": "#fae8ff",
        "accent_blue": "#c026d3",
        "accent_gold": "#9333ea",
        "text_color": "#3b0764"
    },
    "🪵 Retro Amber / Brown": {
        "bg_primary": "#fffbeb",
        "bg_secondary": "#fef3c7",
        "accent_blue": "#d97706",
        "accent_gold": "#92400e",
        "text_color": "#451a03"
    },
    "🍂 Ginger Gold": {
        "bg_primary": "#fdf8f0",
        "bg_secondary": "#faecd8",
        "accent_blue": "#b45309",
        "accent_gold": "#9a3412",
        "text_color": "#431407"
    },
    "🔮 Royal Indigo": {
        "bg_primary": "#f5f3ff",
        "bg_secondary": "#ede9fe",
        "accent_blue": "#4f46e5",
        "accent_gold": "#6d28d9",
        "text_color": "#1e1b4b"
    },
    "🔥 Crimson Arcade": {
        "bg_primary": "#fef2f2",
        "bg_secondary": "#fee2e2",
        "accent_blue": "#dc2626",
        "accent_gold": "#991b1b",
        "text_color": "#450a0a"
    },
    "⚡ Electric Cobalt": {
        "bg_primary": "#eff6ff",
        "bg_secondary": "#dbeafe",
        "accent_blue": "#2563eb",
        "accent_gold": "#1d4ed8",
        "text_color": "#172554"
    }
}

def get_current_theme():
    theme_name = st.session_state.get("selected_theme", "⭐ Cosmic Galaxy")
    is_dark = st.session_state.get("dark_mode", True)
    palette = THEMES if is_dark else LIGHT_THEMES
    return palette.get(theme_name, palette["⭐ Cosmic Galaxy"])

def render_theme_selector():
    """Renders the arcade theme picker in the sidebar and injects the dynamic CSS."""
    is_dark = st.session_state.get("dark_mode", True)
    palette = THEMES if is_dark else LIGHT_THEMES
    curr_t = get_current_theme()

    st.sidebar.markdown(
        f'<p style="color:{curr_t["accent_gold"]}; font-weight:700; font-size:1.05rem;">🎨 ARCADE THEME</p>',
        unsafe_allow_html=True
    )
    theme_name = st.sidebar.selectbox(
        "Theme Selector:", 
        list(THEMES.keys()), 
        index=0,
        key="selected_theme",
        label_visibility="collapsed"
    )
    
    t = palette[theme_name]
    
    theme_css = f"""
        <style>
        /* Dynamic Theme Palette */
        :root, .stApp {{
            --theme-bg-primary: {t['bg_primary']};
            --theme-bg-secondary: {t['bg_secondary']};
            --theme-accent-blue: {t['accent_blue']};
            --theme-accent-gold: {t['accent_gold']};
            --theme-text-color: {t['text_color']};
        }}

        /* Application Canvas */
        .stApp, .main {{
            background-color: {t['bg_primary']} !important;
            color: {t['text_color']} !important;
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border-right: 3px solid {t['accent_blue']} !important;
            box-shadow: 6px 0 25px {t['accent_blue']}33 !important;
        }}

        /* Sidebar Arcade Push-Button Radio Navigation */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_blue']} !important;
            border-radius: 10px !important;
            padding: 9px 12px !important;
            margin-bottom: 8px !important;
            box-shadow: 0 3px 0 {t['accent_blue']}88, 0 0 10px {t['accent_blue']}22 !important;
            transition: all 0.15s ease-in-out !important;
            display: flex !important;
            align-items: center !important;
            cursor: pointer !important;
        }}

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {{
            border-color: {t['accent_gold']} !important;
            box-shadow: 0 3px 0 {t['accent_gold']}aa, 0 0 14px {t['accent_gold']}55 !important;
            transform: translateY(-2px) !important;
            color: {t['accent_gold']} !important;
        }}

        /* Headings */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
            color: {t['accent_gold']} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {t['bg_secondary']} !important;
            border: 2px solid {t['accent_blue']} !important;
            color: {t['accent_blue']} !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease-in-out;
        }}
        .stButton > button:hover, .stButton > button:focus {{
            border-color: {t['accent_gold']} !important;
            box-shadow: 0 0 15px {t['accent_gold']}aa !important;
            background-color: {t['bg_primary']} !important;
            color: {t['accent_gold']} !important;
        }}

        /* Code Editors & Inputs */
        .stTextArea textarea {{
            background-color: {t['bg_secondary']} !important;
            color: {t['text_color']} !important;
            border: 2px solid {t['accent_blue']} !important;
            border-radius: 10px !important;
            box-shadow: 0 0 12px {t['accent_blue']}40 !important;
            font-family: monospace !important;
            font-size: 1.15rem !important;
        }}
        .stTextArea textarea:focus {{
            border-color: {t['accent_gold']} !important;
            box-shadow: 0 0 20px {t['accent_gold']}aa !important;
        }}

        /* Dropdowns */
        .stSelectbox div[data-baseweb="select"] {{
            background-color: {t['bg_secondary']} !important;
            border: 2px solid {t['accent_blue']} !important;
            border-radius: 10px !important;
            color: {t['text_color']} !important;
        }}

        /* Radio Options */
        .stRadio label {{
            color: {t['text_color']} !important;
        }}
        .stRadio label:hover {{
            color: {t['accent_gold']} !important;
            background-color: {t['bg_secondary']} !important;
        }}

        /* Universal Themed Content Boxes */
        .arcade-hud-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_gold']} !important;
            box-shadow: 0 0 22px {t['accent_gold']}60 !important;
            padding: 16px;
            border-radius: 12px;
            color: {t['text_color']} !important;
            text-align: center;
            margin: 15px 0;
        }}

        .arcade-tip-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_gold']} !important;
            box-shadow: 0 0 20px {t['accent_gold']}50 !important;
            padding: 12px 18px;
            border-radius: 10px;
            color: {t['text_color']} !important;
            text-align: center;
            margin: 10px 0 20px 0;
        }}

        .colorful-history-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['accent_blue']}33 100%) !important;
            border: 3px solid {t['accent_gold']} !important;
            box-shadow: 0 0 25px {t['accent_gold']}50 !important;
            padding: 22px;
            border-radius: 14px;
            color: {t['text_color']} !important;
            margin-bottom: 20px;
        }}

        .arcade-welcome-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['accent_blue']}33 100%) !important;
            padding: 24px;
            border-radius: 14px;
            border: 3px solid {t['accent_blue']} !important;
            box-shadow: 0 0 25px {t['accent_blue']}50 !important;
            color: {t['text_color']} !important;
            text-align: center;
            margin-bottom: 20px;
        }}

        .arcade-briefing-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_blue']} !important;
            box-shadow: 0 0 18px {t['accent_blue']}40 !important;
            padding: 18px 22px;
            border-radius: 12px;
            color: {t['text_color']} !important;
            font-size: 1.15rem;
            margin-bottom: 15px;
        }}

        .arcade-stats-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_gold']} !important;
            box-shadow: 0 0 15px {t['accent_gold']}50 !important;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            color: {t['text_color']} !important;
        }}

        .arcade-quiz-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_blue']} !important;
            box-shadow: 0 0 18px {t['accent_blue']}40 !important;
            padding: 16px 20px;
            border-radius: 12px;
            margin: 20px 0 15px 0;
            color: {t['text_color']} !important;
        }}

        .arcade-video-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px dashed {t['accent_blue']} !important;
            box-shadow: 0 0 15px {t['accent_blue']}30 !important;
            padding: 18px;
            border-radius: 12px;
            color: {t['text_color']} !important;
            text-align: center;
        }}

        .arcade-badge-card {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            padding: 25px;
            border-radius: 14px;
            text-align: center;
            color: {t['text_color']} !important;
        }}

        .arcade-box {{
            background: linear-gradient(135deg, {t['bg_secondary']} 0%, {t['bg_primary']} 100%) !important;
            border: 2px solid {t['accent_blue']} !important;
            box-shadow: 0 0 15px {t['accent_blue']}40 !important;
            padding: 16px 20px;
            border-radius: 12px;
            color: {t['text_color']} !important;
            text-align: center;
        }}
        </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
    return theme_name
