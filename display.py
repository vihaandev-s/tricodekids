import streamlit as st

def render_display_mode():
    """Renders the display mode toggle buttons in the sidebar."""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    st.sidebar.subheader("🕹️ DISPLAY MODE 🕹️")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state.dark_mode = True
            st.rerun()
    with col2:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state.dark_mode = False
            st.rerun()