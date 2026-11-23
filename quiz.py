import streamlit as st
import os
from points import save_progress
from welcome import play_audio
from translation import get_text

def render_quiz(language, topic, current_lesson):
    quiz_title_label = get_text("Arcade Quiz")
    first_ch = get_text("1st Chance")
    second_ch = get_text("2nd Chance")
    third_ch = get_text("3rd Chance")
    st.markdown(
        f"""
        <div class="arcade-quiz-box">
            <h3 style="margin: 0;">🎯 {language} {quiz_title_label}: {topic}</h3>
            <div style="
                background: rgba(0, 0, 0, 0.25);
                border: 1px solid var(--theme-accent-blue);
                border-radius: 8px;
                padding: 10px 14px;
                margin-top: 12px;
                display: flex;
                justify-content: space-around;
                text-align: center;
                font-size: 0.95rem;
            ">
                <span>🥇 <b>{first_ch}:</b> <strong style="color: var(--theme-accent-gold);">15 pts</strong></span>
                <span>🥈 <b>{second_ch}:</b> <strong style="color: var(--theme-accent-blue);">10 pts</strong></span>
                <span>🥉 <b>{third_ch}:</b> <strong style="color: #34d399;">5 pts</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state tracking keys
    if "quiz_attempts" not in st.session_state:
        st.session_state.quiz_attempts = {}
    if "quiz_solved" not in st.session_state:
        st.session_state.quiz_solved = set()
    if "first_try_solved" not in st.session_state:
        st.session_state.first_try_solved = set()

    quiz_key = f"{language}_{topic}"

    # Fallback/dynamic quiz structure from lesson dictionary
    quiz_data = current_lesson.get("quiz", {
        "question": f"What is a key concept when working with {topic} in {language}?",
        "options": [
            f"Use proper syntax and follow {language} rules",
            "Ignore all syntax errors and run random text",
            "Only use uppercase letters for all commands",
            "Delete the main script after writing code"
        ],
        "correct": f"Use proper syntax and follow {language} rules"
    })

    question = quiz_data.get("question", "Choose the correct option:")
    options = quiz_data.get("options", ["Option A", "Option B", "Option C", "Option D"])
    correct_answer = quiz_data.get("correct", options[0])

    translated_question = get_text(question)

    # Render radio button options with index=None so nothing is pre-selected
    user_choice = st.radio(
        translated_question, 
        options, 
        index=None, 
        key=f"radio_{quiz_key}"
    )

    feedback_key = f"quiz_feedback_{quiz_key}"

    submit_label = f"🚀 {get_text('Submit Answer')}"
    if st.button(submit_label, key=f"submit_{quiz_key}"):
        if user_choice is None:
            st.warning("⚠️ Please select an answer before submitting!")
        else:
            # Increment attempt counter
            attempts = st.session_state.quiz_attempts.get(quiz_key, 0) + 1
            st.session_state.quiz_attempts[quiz_key] = attempts

            if user_choice == correct_answer:
                if attempts == 1:
                    points_earned = 15
                    chance_label = "1st Chance"
                elif attempts == 2:
                    points_earned = 10
                    chance_label = "2nd Chance"
                else:
                    points_earned = 5
                    chance_label = f"{attempts}rd Chance"
                
                already_solved = quiz_key in st.session_state.quiz_solved
                if not already_solved:
                    st.session_state.quiz_solved.add(quiz_key)
                    if attempts == 1:
                        st.session_state.first_try_solved.add(quiz_key)
                    
                    st.session_state.score += points_earned
                    st.session_state.last_awarded = points_earned
                    save_progress()

                st.session_state[feedback_key] = {
                    "status": "correct",
                    "points": points_earned if not already_solved else 0,
                    "already_solved": already_solved,
                    "chance_label": chance_label
                }
                # Rerun immediately so Score HUD & Sidebar update on this single click!
                st.rerun()
            else:
                next_chance = attempts + 1
                if next_chance == 2:
                    next_text = "2nd Chance for 10 points"
                elif next_chance == 3:
                    next_text = "3rd Chance for 5 points"
                else:
                    next_text = "last chance for 5 points"

                st.session_state[feedback_key] = {
                    "status": "incorrect",
                    "next_text": next_text
                }
                st.rerun()

    # Render feedback message (persists after rerun so score updates in 1 click!)
    feedback = st.session_state.get(feedback_key)
    if feedback:
        if feedback["status"] == "correct":
            if feedback.get("already_solved"):
                msg_text = "Already solved! Great arcade practice!"
            else:
                msg_text = f'Solved on your <b>{feedback["chance_label"]}</b>! You earned <b>+{feedback["points"]} Points</b>!'

            success_msg = (
                f'<div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); '
                f'border: 2px solid #34d399; box-shadow: 0 0 20px rgba(52, 211, 153, 0.6); '
                f'padding: 20px; border-radius: 12px; color: #ffffff; text-align: center; margin: 15px 0;">'
                f'<h3 style="margin: 0; color: #a7f3d0; text-shadow: 0 0 10px #34d399;">🏆 CORRECT ANSWER! 🏆</h3>'
                f'<p style="font-size: 1.15rem; margin-top: 8px; margin-bottom: 0;">'
                f'{msg_text}'
                f'</p></div>'
            )
            st.markdown(success_msg, unsafe_allow_html=True)
            st.balloons()

            audio_file = "success_audio.m4a" if os.path.exists("success_audio.m4a") else ("success_audio.mp3" if os.path.exists("success_audio.mp3") else None)
            if audio_file:
                play_audio(audio_file)
        elif feedback["status"] == "incorrect":
            fail_msg = (
                f'<div style="background: linear-gradient(135deg, #7f1d1d 0%, #b91c1c 100%); '
                f'border: 2px solid #f87171; box-shadow: 0 0 20px rgba(248, 113, 113, 0.6); '
                f'padding: 20px; border-radius: 12px; color: #ffffff; text-align: center; margin: 15px 0;">'
                f'<h3 style="margin: 0; color: #fee2e2; text-shadow: 0 0 10px #f87171;">⚠️ NOT QUITE! ⚠️</h3>'
                f'<p style="font-size: 1.1rem; margin-top: 8px; margin-bottom: 0;">'
                f'Don\'t worry! Try again on your <b>{feedback["next_text"]}</b>!'
                f'</p></div>'
            )
            st.markdown(fail_msg, unsafe_allow_html=True)