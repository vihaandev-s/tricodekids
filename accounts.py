import hashlib
import json
import os
import secrets
import streamlit as st

ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tricodekids_accounts.json")


def default_progress() -> dict:
    return {
        "score": 0,
        "quiz_solved": [],
        "first_try_solved": [],
        "completed": [],
        "bonus_solved": [],
        "quiz_attempts": {},
    }


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def load_accounts() -> dict:
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    return {}


def save_accounts(accounts: dict) -> None:
    try:
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=2)
    except Exception:
        pass


def apply_progress_to_session(progress: dict | None) -> None:
    p = progress or default_progress()
    st.session_state.score = p.get("score", 0)
    st.session_state.quiz_solved = set(p.get("quiz_solved", []))
    st.session_state.first_try_solved = set(p.get("first_try_solved", []))
    st.session_state.completed = set(p.get("completed", []))
    st.session_state.bonus_solved = set(p.get("bonus_solved", []))
    st.session_state.quiz_attempts = dict(p.get("quiz_attempts", {}))
    st.session_state.last_awarded = 0
    st.session_state.welcomed = False
    st.session_state.bonus_tip_shown = False
    st.session_state.champion_toast_shown = False
    for k in list(st.session_state.keys()):
        if k.startswith("quiz_feedback_") or k.startswith("radio_"):
            del st.session_state[k]


def load_user_progress(username: str | None) -> dict | None:
    if not username or username == "__guest__":
        return None
    accounts = load_accounts()
    user_record = accounts.get(username.lower())
    if not user_record:
        return None
    p = user_record.get("progress", default_progress())
    return {
        "score": p.get("score", 0),
        "quiz_solved": set(p.get("quiz_solved", [])),
        "first_try_solved": set(p.get("first_try_solved", [])),
        "completed": set(p.get("completed", [])),
        "bonus_solved": set(p.get("bonus_solved", [])),
        "quiz_attempts": p.get("quiz_attempts", {}),
    }


def save_user_progress(username: str | None, progress_data: dict) -> None:
    if not username or username == "__guest__":
        return
    accounts = load_accounts()
    key = username.lower()
    if key not in accounts:
        return
    accounts[key]["progress"] = progress_data
    save_accounts(accounts)


def register_user(username: str, password: str) -> tuple[bool, str]:
    clean_name = username.strip()
    if len(clean_name) < 2:
        return False, "Username must be at least 2 characters."
    if not clean_name.replace("_", "").replace("-", "").isalnum():
        return False, "Username can only contain letters, numbers, '-' or '_'."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."

    accounts = load_accounts()
    key = clean_name.lower()
    if key in accounts:
        return False, "That username is already taken! Try another or log in."

    salt = secrets.token_hex(8)
    accounts[key] = {
        "display_name": clean_name,
        "salt": salt,
        "password_hash": _hash_password(password, salt),
        "progress": default_progress(),
    }
    save_accounts(accounts)
    st.session_state.current_user = key
    st.session_state.current_display_name = clean_name
    apply_progress_to_session(default_progress())
    return True, f"Welcome, {clean_name}! Account created."


def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    key = username.strip().lower()
    if not key or not password:
        return False, "Please enter both username and password."

    accounts = load_accounts()
    user_record = accounts.get(key)
    if not user_record:
        return False, "Account not found. Check your username or create a new account."

    expected_hash = user_record.get("password_hash", "")
    salt = user_record.get("salt", "")
    if _hash_password(password, salt) != expected_hash:
        return False, "Incorrect password. Please try again."

    st.session_state.current_user = key
    st.session_state.current_display_name = user_record.get("display_name", key)
    apply_progress_to_session(user_record.get("progress", default_progress()))
    return True, f"Welcome back, {st.session_state.current_display_name}!"


def login_as_guest() -> None:
    st.session_state.current_user = "__guest__"
    st.session_state.current_display_name = "Guest"
    apply_progress_to_session(default_progress())


def logout_user() -> None:
    st.session_state.pop("current_user", None)
    st.session_state.pop("current_display_name", None)
    apply_progress_to_session(default_progress())


def render_auth_screen() -> None:
    """Renders the player login / sign-up screen so every student keeps their own score and badges."""
    st.markdown(
        """
        <div class="arcade-hud-box" style="max-width: 620px; margin: 20px auto;">
            <h1 style="margin: 0 0 8px 0;">🕹️ TriCodeKids Player Login</h1>
            <p style="margin: 0; font-size: 1.05rem;">
                Log in or create your own player account so your points, quizzes, and badges are saved just for you!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["🔑 Log In", "✨ Create Account"])

    with tab_login:
        with st.form("login_form"):
            login_user = st.text_input("Player Username", placeholder="e.g. alex_coder")
            login_pass = st.text_input("Password", type="password")
            submitted = st.form_submit_button("🚀 Log In & Play", use_container_width=True)
            if submitted:
                ok, msg = authenticate_user(login_user, login_pass)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with tab_signup:
        with st.form("signup_form"):
            new_user = st.text_input("Choose a Username", placeholder="e.g. maya_dev")
            new_pass = st.text_input("Choose a Password (min 4 chars)", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            created = st.form_submit_button("⭐ Create Account & Start", use_container_width=True)
            if created:
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                else:
                    ok, msg = register_user(new_user, new_pass)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    st.divider()
    if st.button("🕹️ Play as Guest (Session Only)", use_container_width=True):
        login_as_guest()
        st.rerun()
