import os
import streamlit as st
from dotenv import load_dotenv

# Load from all possible .env locations
load_dotenv()
load_dotenv(".streamlit/.env")
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), ".streamlit", ".env"))

def get_tribot_fallback_answer(question: str) -> str:
    """Friendly built-in tech tutor answers when API key is not yet configured."""
    q = question.lower().strip()
    
    # Cybersecurity & Safety
    if any(k in q for k in ["cybersecurity", "cyber security", "safety"]):
        return (
            "🤖 **Tribot says:** Cybersecurity is like a digital lock and alarm system for computers! "
            "It protects your games, accounts, and private photos from bad hackers.\n\n"
            "**Tribot's Top Rules:**\n"
            "1. 🔒 Use strong passwords with numbers & symbols!\n"
            "2. 🎣 Never click weird links from strangers.\n"
            "3. 🛡️ Keep your apps updated!"
        )
    if any(k in q for k in ["hacker", "hacking"]):
        return (
            "🤖 **Tribot says:** Hacking means figuring out how computer systems work behind the scenes!\n\n"
            "- **Black Hat Hackers:** Break rules and steal data (the villains).\n"
            "- **White Hat Hackers:** Help fix security flaws to protect everyone (the superheroes)!"
        )
    if any(k in q for k in ["firewall"]):
        return (
            "🤖 **Tribot says:** A firewall is like an arcade bouncer standing at the door of your Wi-Fi! "
            "It checks every packet of data and kicks out anything suspicious."
        )
    if any(k in q for k in ["python"]):
        return (
            "🤖 **Tribot says:** Python is one of the friendliest coding languages ever! It reads like plain English.\n\n"
            "```python\n"
            "# Try this in the sandbox:\n"
            "print('Hello from Tribot!')\n"
            "```"
        )
    if any(k in q for k in ["java ", "what is java", "java language"]):
        return (
            "🤖 **Tribot says:** Java is a super-popular, fast language famous for 'Write Once, Run Anywhere'! "
            "Fun fact: the original Minecraft game was programmed in Java! ⛏️"
        )
    if any(k in q for k in ["javascript", "js"]):
        return (
            "🤖 **Tribot says:** JavaScript is the superpower behind web browsers! It makes buttons click, "
            "animations fly, and browser arcade games run."
        )
    if any(k in q for k in ["variable"]):
        return (
            "🤖 **Tribot says:** A variable is like a labeled treasure chest in a game. "
            "You give it a name like `coins` and store a value like `100` inside!"
        )
    if any(k in q for k in ["loop"]):
        return (
            "🤖 **Tribot says:** A loop repeats code for you automatically so you don't have to retype it! "
            "Think of a game repeating levels until you reach the boss."
        )
    if any(k in q for k in ["operating system", "os "]):
        return (
            "🤖 **Tribot says:** The Operating System (like Windows, macOS, Android, or Linux) is the master boss program "
            "that lets apps, memory, screens, and games work together!"
        )

    return (
        f"🤖 **Tribot says:** That's a fantastic coding question about *'{question}'*!\n\n"
        "In computer programming, the best way to learn is by experimenting. "
        "Try typing a small example into the **Interactive Code Sandbox** right on this page and click **▶️ Run Code** to see what happens!"
    )

def ask_tribot(user_question: str) -> str:
    """Sends a kid-friendly coding question to Tribot (Google GenAI) and returns the answer."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "your_actual" in api_key.lower():
        if hasattr(st, "secrets"):
            try:
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                pass

    if api_key and "your_actual" not in api_key.lower():
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_question,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Tribot, a fun, encouraging, and friendly AI coding tutor for kids "
                        "on the Tricodekids website. Explain Python, Java, and JavaScript concepts, "
                        "cybersecurity, and technology using simple language, short examples, and a playful arcade-style vibe."
                    )
                )
            )
            if response and response.text:
                return response.text
        except Exception as e:
            # Fall back smoothly if network / key error occurs
            return get_tribot_fallback_answer(user_question)

    return get_tribot_fallback_answer(user_question)
