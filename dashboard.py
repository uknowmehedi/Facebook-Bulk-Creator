# --- Retry & Headless UI Controls Section ---
# Show under sidebar settings to allow user configuration

st.sidebar.markdown("---")  # Separator
st.sidebar.subheader("⚙️ Automation Settings")

st.session_state.headless = st.sidebar.toggle("🎭 Headless Mode", value=True)
st.session_state.max_attempts = st.sidebar.number_input("🔁 Max Retry Attempts", 1, 10, value=3)
st.session_state.delay_seconds = st.sidebar.slider("⏱️ Delay Between Retries (sec)", 5, 60, value=30)
st.session_state.fallback_enabled = st.sidebar.checkbox("🧪 Enable Fallback Retry", value=True)
st.session_state.max_tabs = st.sidebar.slider("🗂️ Max Parallel Tabs", 1, 5, value=3)