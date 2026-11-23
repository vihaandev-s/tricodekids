import streamlit as st
import urllib.request
import urllib.parse
import json

# Supported languages for translation
LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Telugu": "te"
}

@st.cache_data(show_spinner=False)
def translate_text(text: str, target_lang_code: str) -> str:
    """Translates any English text into the target language code using free Google Translate."""
    if not text or not isinstance(text, str):
        return text
    if target_lang_code == "en":
        return text
    try:
        url = (
            f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang_code}&dt=t&q="
            + urllib.parse.quote(text)
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            return "".join([part[0] for part in data[0] if part and part[0]])
    except Exception:
        return text

def get_text(text: str) -> str:
    """Translates text into the user's currently selected website language."""
    curr_lang = st.session_state.get("current_language", "English")
    # Extract language name before any parenthesis (e.g. 'Gujarati (ગુજરાતી)' -> 'Gujarati')
    lang_name = curr_lang.split(" ")[0].strip() if curr_lang else "English"
    target_code = LANG_CODES.get(lang_name, "en")
    if target_code == "en":
        return text
    return translate_text(text, target_code)

# Short convenient alias
t = get_text
