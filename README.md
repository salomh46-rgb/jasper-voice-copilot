# Jasper AI — Live Voice Copilot Desktop & Web Assistant 🎙️⚡

> **Personal Real-Time Voice-Controlled Desktop Assistant (JARVIS)** that listens to Uzbek natural voice commands, controls Windows applications, navigates websites, audits disk storage, and speaks back in live audio.

Developed by **Javohirbek Asqarov (Jasper)**.

---

## ✨ Features

- 🎙️ **Real-Time Uzbek Speech-to-Text & Text-to-Speech**: Seamless bidirectional live speech interaction via Web Speech API and synthesis.
- 💻 **Executive Windows System Control**:
  - Open Applications: *"Kalkulyatorni och"*, *"Bloknotni och"*, *"Chrome'ni yoq"*, *"Telegramni och"*.
  - Open Websites: *"GitHub profilimni och"*, *"YouTube'ni och"*, *"Portfolio saytimni ko'rsat"*.
  - System & Disk Telemetry: *"C diskda qancha joy qoldi?"*, *"D diskdagi loyihalarni ko'rsat"*.
- 🌐 **Futuristic Cyberpunk Glassmorphism UI**: Dynamic Sine Soundwave Visualizer, real-time action logs, and instant command chips.
- ⚡ **1-Click Launcher**: Double-click `run_copilot.bat` to spin up the server and launch the HUD.
- 🧪 **100% Automated Test Coverage**: Comprehensive unittest suite.

---

## 🚀 Quick Start

### Option 1: 1-Click Batch Launcher (Windows)
Double-click: `run_copilot.bat`

### Option 2: Manual Start
```bash
cd D:\ALLProjects\jasper_voice_copilot
pip install -r server/requirements.txt
python -m uvicorn server.main:app --port 8000 --reload
```
Then open `client/index.html` in your browser.

---

## 🧪 Run Automated Tests

```bash
python -m unittest discover tests/
```

---

## 📄 License
MIT License. Created with ❤️ by **Javohirbek Asqarov (Jasper)**.
