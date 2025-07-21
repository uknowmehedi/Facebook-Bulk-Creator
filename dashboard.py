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

config = load_config()
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
    🧠 Automation Builder  
    📬 Telegram: [@uKnowMehedi](https://t.me/uKnowMehedi)
    """)
    st.caption("Facebook Bulk Creator GUI | Powered by Streamlit")
