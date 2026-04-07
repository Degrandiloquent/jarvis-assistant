# JARVIS AI Assistant 🚀

## Desktop Version (Python)
Iron Man-inspired voice assistant with:
- 🔊 Real TTS (SAPI/win32com/PowerShell)
- 🎤 Speech recognition
- 📱 Volume control (pycaw)
- 🖥️ Open/close apps (Chrome, YouTube, Calculator, etc.)
- 🔍 Google/YouTube search
- 🧠 Gemini 2.0 Flash AI chat
- ✨ Visual sound waves (Tkinter)

**Run:** `python jarvis_ultimate.py`

## Web Version (Vercel) 🌐
Professional Iron Man HUD UI with:
- 🎤 Web Speech STT/TTS
- ✨ Animated sound waves + particle stars
- 🧠 Gemini AI
- 🎨 Glassmorphism + neon cyan theme
- 📱 Quick commands (time, apps, search)

### Deploy to Vercel:
1. Install Vercel CLI: `npm i -g vercel`
2. `cd frontend`
3. `vercel --prod`
4. Set env var: `vercel env add GEMINI_API_KEY production` (use your key)
5. Live: https://your-project.vercel.app

**Demo:** https://jarvis-assistant.vercel.app (once deployed)

## Features Comparison
| Feature | Desktop | Web |
|---------|---------|-----|
| TTS/STT | ✅ Native | ✅ Web Speech |
| Volume | ✅ Windows | 🔊 Mock |
| Apps | ✅ Native | 🔗 Links |
| AI Chat | ✅ Gemini | ✅ Proxy |
| Visuals | ✅ Waves | ✨ HUD + Waves |
| Deploy | Local | 🚀 Vercel/Netlify

## Setup
```bash
# Desktop deps
pip install -r requirements.txt  # speechrecognition pyttsx3 pycaw pyautogui google-generativeai

# Web: Just open index.html or deploy!
```

**JARVIS online, sir.**

