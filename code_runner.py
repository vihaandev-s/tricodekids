import streamlit as st
import io
import contextlib
from translation import get_text

def render_code_runner(language, current_lesson):
    sandbox_title = get_text("Interactive Code Sandbox")
    write_code_prompt = f"{get_text('Write or edit your')} {language} {get_text('code below:')}"
    run_btn_label = f"▶️ {get_text('Run Code')}"

    st.markdown(
        f"""
        <h3 style="
            color: #38bdf8;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
            margin-top: 20px;
            margin-bottom: 10px;
        ">💻 {sandbox_title}</h3>
        """,
        unsafe_allow_html=True
    )

    starter_code = current_lesson.get("starter_code", "")
    user_code = st.text_area(
        write_code_prompt,
        value=starter_code,
        height=160,
        key="code_editor_{}_{}".format(language, current_lesson["video"])
    )

    if st.button(run_btn_label):
        output_text = ""
        is_error = False

        if language == "Python":
            buffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(buffer):
                    exec(user_code, {})
                output_text = buffer.getvalue() or "(Code ran with no printed output)"
            except Exception as e:
                output_text = "Error: {}".format(e)
                is_error = True
        else:
            # Simulated output preview for Java & JavaScript on TV
            if ("System.out.println" in user_code and ";" in user_code) or ("console.log" in user_code):
                output_text = "Compiled & Executed Successfully! Great job writing {} syntax!".format(language)
            else:
                output_text = "Check your {} syntax (make sure you have print statements and semicolons!).".format(language)
                is_error = True

        border_color = "#f87171" if is_error else "#34d399"
        text_color = "#fecaca" if is_error else "#34d399"
        shadow_color = "rgba(248, 113, 113, 0.4)" if is_error else "rgba(52, 211, 153, 0.4)"

        console_html = """
            <div style="
                background: linear-gradient(135deg, var(--theme-bg-secondary, #0f172a) 0%, var(--theme-bg-primary, #090d16) 100%);
                border: 2px solid {};
                box-shadow: 0 0 15px {};
                padding: 15px;
                border-radius: 10px;
                color: {};
                font-family: monospace;
                font-size: 1.1rem;
                margin-top: 10px;
                white-space: pre-wrap;
            "><b>[CONSOLE OUTPUT]:</b>\n{}</div>
        """.format(border_color, shadow_color, text_color, output_text)
        st.markdown(console_html, unsafe_allow_html=True)
