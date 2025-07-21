import streamlit as st
import json
import os
import time
from datetime import datetime
from utils.retry_stats import load_stats, reset_stats, save_stats
from utils.fb_helper import run_bulk_creation

CONFIG_FILE = "config.json"
LOG_FILE = "logs/log.txt"

default_config = {
    "headless": True,
    "max_attempts": 3,
    "delay_seconds": 30,
    "fallback_enabled": True,
    "max_tabs": 3
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def log_message(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

st.set_page_config(page_title="Facebook Bulk Creator", layout="wide")
st.sidebar.title("📱 Facebook Bulk Creator")
page = st.sidebar.radio("📂 Navigate", [
    "Create New Account", "Retry Stats", "Logs", "Settings", "About Me"
])

config = load_config()

if page == "Create New Account":
    st.title("🚀 Facebook Account Automation")
    st.success("Ready to run bulk account creation!")
    st.subheader("⚙️ Current Settings")
    for k, v in config.items():
        st.write(f"**{k.replace('_', ' ').capitalize()}**: `{v}`")

    if st.button("▶️ Run Automation Now"):
        st.info("Starting automation...")
        progress = st.progress(0)
        log_message("Automation started.")
        result = run_bulk_creation(config, st=st, progress=progress)
        save_stats(result["stats"])
        st.success("✅ Automation completed!")
        log_message("Automation completed.")

elif page == "Retry Stats":
    st.title("📊 Retry Tracker")
    stats = load_stats()
    for module, info in stats.items():
        st.subheader(f"🔧 {module.capitalize()}")
        st.write(f"✅ Success: {info['success']}")
        st.write(f"❌ Failure: {info['failure']}")
        st.write(f"⚠️ Last Error: `{info['last_error']}`")
    if st.button("🔄 Reset Stats"):
        reset_stats()
        st.success("Retry stats reset.")

elif page == "Logs":
    st.title("📜 Real-Time Logs")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.read().splitlines()[-50:]
            for line in logs:
                st.text(line)
    else:
        st.info("No logs yet.")

    st.subheader("📧 Gmail Usage Status")
    col1, col2, col3 = st.columns(3)

    def show_list(path, label):
        if os.path.exists(path):
            with open(path) as f:
                lines = f.read().splitlines()
            st.markdown(f"**{label} ({len(lines)}):**")
            st.code("\n".join(lines[-5:]) if lines else "None")
        else:
            st.markdown(f"**{label} (0):**")

    with col1:
        show_list("assets/gmail_address.txt", "Unused")
    with col2:
        show_list("assets/used_gmails.txt", "Used")
    with col3:
        show_list("assets/failed_gmails.txt", "Failed")

elif page == "Settings":
    st.title("⚙️ Automation Settings")
    config['headless'] = st.toggle("🎭 Headless Mode", value=config.get("headless", True))
    config['max_attempts'] = st.number_input("📩 Max Retry Attempts", 1, 10, value=config.get("max_attempts", 3))
    config['delay_seconds'] = st.slider("⏱ Delay Between Retries (sec)", 5, 60, value=config.get("delay_seconds", 30))
    config['fallback_enabled'] = st.checkbox("🛟 Enable Fallback Retry", value=config.get("fallback_enabled", True))
    config['max_tabs'] = st.slider("📁 Max Parallel Tabs", 1, 5, value=config.get("max_tabs", 3))
    if st.button("💾 Save Settings"):
        save_config(config)
        st.success("Settings saved successfully!")

elif page == "About Me":
    st.title("👤 About Developer")
    st.markdown("""
    **Rabbit Fighter**  
    🧠 Automation Enthusiast | Telegram Bot Builder  
    📬 Telegram: [@uKnowMehedi](https://t.me/uKnowMehedi)
    """)
    st.caption("Facebook Bulk Creator GUI | Powered by Streamlit")