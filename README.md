# Facebook-Bulk-Creator
This Automation for Facebook Multi Account Creation

# for Linux need permission before lunch
chmod +x auto-launch.sh
./auto-launch.sh
# requirements
sudo apt install python3-pip libnss3 libatk-bridge2.0-0 libgtk-3-0 patchelf
pip install pyinstaller

# 📦 Facebook Account Creator (GUI + Automation)

**Cross-platform GUI tool to automate Facebook account creation using Gmail OTP, Playwright, and multi-tab logic.**  
Compatible with **Windows 10/11** and **Ubuntu/Linux** — ready for `.exe` and `.AppImage` builds.

---

## 🎯 Features

✅ Streamlit-based clean GUI  
✅ Uses Playwright (mobile view) for stealth automation  
✅ Multi-tab support (up to 5 accounts at once)  
✅ Real-time OTP verification via Gmail  
✅ Retry + fallback system with GUI controls  
✅ Tracks used/unused emails  
✅ Light/Dark theme toggle  
✅ Export logs as `.json` or `.txt`

---

## 🖥️ How to Run

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 3. Start the GUI

```bash
streamlit run dashboard.py
```

---

## 📁 Folder Structure

```
📂 Facebook-Bulk-Creator/
│
├── dashboard.py                  # Streamlit GUI
│
├── controllers/
│   ├── automation.py             # Multi-tab automation logic
│   ├── real_email_loader.py     # Email usage logic + stats
│   ├── export_logs.py           # Exports logs and results
│   └── gmail_otp_reader.py      # OTP fetcher via IMAP
│
├── assets/
│   ├── names.json               # Male/Female name bank
│   └── gmail_address.txt        # Email|App Password combo
│
├── logs/
│   └── used_gmail.txt           # Tracks used emails
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Configuration (inside GUI)

- **🎭 Headless Toggle** – run Playwright in background  
- **🔁 Max Retry Attempts** – how many times to retry OTP  
- **⏱️ Delay Between Retries** – wait time (seconds)  
- **🧪 Fallback Retry** – enable simulated fallback  
- **🗂️ Max Tabs** – how many accounts to create at once  

---

## 📬 Gmail Setup

1. Enable IMAP in Gmail settings  
2. Create an **App Password** (not your main Gmail password)  
3. Save to `assets/gmail_address.txt` in format:

```
yourgmail@gmail.com|abcd efgh ijkl mnop
```

---

## 📦 Packaging

To create `.exe` or `.AppImage`:

```bash
pyinstaller main.spec  # for custom PyInstaller config
```

Use tools like `nuitka` or `appimage-builder` for advanced builds.

---

# For windows 10/11
# ✅ STEP-BY-STEP SETUP FOR FACEBOOK ACCOUNT CREATOR (Windows 11)

# --- 1. Install Python 3.9+ ---
# Download and install from: https://www.python.org/downloads/windows/
# ✅ IMPORTANT: Check "Add Python to PATH" during install

# Verify installation:
python --version
pip --version

# --- 2. Install Git ---
# Download and install from: https://git-scm.com/download/win
# Use default settings.

# Verify installation:
git --version

# --- 3. Install Microsoft C++ Build Tools (required for some Python packages) ---
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# ✅ During install, check:
#   - "C++ build tools"
#   - "Windows 10 SDK"

# --- 4. Install Node.js (Playwright needs it for browser support) ---
# Download from: https://nodejs.org/
# Use LTS version.

# Verify installation:
node -v
npm -v

# --- 5. (Optional but Recommended) Install VS Code ---
# https://code.visualstudio.com/

# --- 6. Clone the Repository ---
mkdir FacebookAccountCreator
cd FacebookAccountCreator
git clone https://github.com/your-username/facebook-account-creator.git
cd facebook-account-creator

# --- 7. Install Python dependencies ---
pip install -r requirements.txt

# --- 8. Install Playwright browsers ---
playwright install

# --- 9. Run the GUI app ---
streamlit run dashboard.py

## 🧑‍💻 Author

Developed by **Rabbit Fighter**  
📬 Telegram: [@uKnowMehedi]

---

**"🤓 Smart work will give you a better opportunity."**