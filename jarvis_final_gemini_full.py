import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pyautogui
import datetime
import urllib.request
import re
import tkinter as tk
import time
import random
import math
import warnings
from ctypes import cast, POINTER
from comtypes import CLSCTX_INPROC_SERVER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
try:
    import win32com.client
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False

warnings.filterwarnings("ignore", category=FutureWarning)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
GEMINI_API_KEY = "AIzaSyDalrZNGeDakdA5wExueQVjcZ-bd-qxMAk"

class JarvisAssistant:
    def speak(self, text):
        print(f"\n🤖 JARVIS: {text}")
        self.show_visual_indicator()
        try:
            if WIN32COM_AVAILABLE:
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                voices = speaker.GetVoices()
                if voices.Count > 0:
                    speaker.Voice = voices.Item(0)
                speaker.Speak(text)
            else:
                escaped_text = text.replace("'", "''").replace('"', '\\"')
                subprocess.run(['powershell', f"Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SelectVoice('Microsoft David Desktop'); $s.Speak('{escaped_text}')"], shell=True, check=True, capture_output=True)
        except Exception as e:
            print(f"TTS fallback: {e}")
            self.engine.say(text)
            self.engine.runAndWait()
        self.hide_visual_indicator()

    def show_visual_indicator(self):
        if not hasattr(self, 'visual_indicator') or self.visual_indicator is None:
            self.visual_indicator = tk.Tk()
            self.visual_indicator.attributes("-alpha", 0.7)
            self.visual_indicator.attributes("-topmost", True)
            self.visual_indicator.overrideredirect(True)
            self.visual_indicator.geometry("400x100+100+100")
            self.visual_indicator.configure(bg='black')
            self.canvas = tk.Canvas(self.visual_indicator, width=400, height=100, bg='black')
            self.canvas.pack()
            self.bars = [self.canvas.create_rectangle(20 + i*20, 50, 35 + i*20, 50, fill='cyan') for i in range(18)]
            self.anim_running = True
            self.animate_visual_frame()

    def animate_visual_frame(self):
        if not hasattr(self, 'anim_running') or not self.anim_running:
            return
        if hasattr(self, 'visual_indicator') and self.visual_indicator:
            try:
                for i, bar in enumerate(self.bars):
                    h = random.randint(20, 60)
                    x1, y1, x2, y2 = self.canvas.coords(bar)
                    self.canvas.coords(bar, x1, 50-h//2, x2, 50+h//2)
                self.canvas.update()
                self.visual_indicator.after(80, self.animate_visual_frame)
            except tk.TclError:
                pass

    def hide_visual_indicator(self):
        self.anim_running = False
        if hasattr(self, 'visual_indicator') and self.visual_indicator:
            self.visual_indicator.destroy()
            self.visual_indicator = None
            self.canvas = None
            self.bars = None

    def __init__(self):
        print("🚀 JARVIS FINAL FULL - Gemini 2.5 + All Features")
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)

        self.recognizer = sr.Recognizer()
        self.model = None
        self.volume = None

        # Volume control
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_INPROC_SERVER, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("✅ Volume control ready (pycaw)")
        except Exception as e:
            print(f"pycaw failed: {e}")

        # Gemini
        if GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ GEMINI 2.5 FLASH READY!")
            except Exception as e:
                print(f"Gemini error: {e}")

        self.speak("JARVIS full capabilities online. Say help for commands!")

    def volume_up(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new = min(current + 0.1, 1.0)
            self.volume.SetMasterVolumeLevelScalar(new, None)
            self.speak(f"Volume {int(new*100)}%")
        else:
            pyautogui.press('volumeup')
            self.speak("Volume up!")

    def volume_down(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new = max(current - 0.1, 0.0)
            self.volume.SetMasterVolumeLevelScalar(new, None)
            self.speak(f"Volume {int(new*100)}%")
        else:
            pyautogui.press('volumedown')
            self.speak("Volume down!")

    def chat_gemini(self, query):
        if not self.model:
            return "Gemini offline"
        try:
            response = self.model.generate_content(query)
            return response.text.strip()
        except:
            return "Gemini error"

    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    def get_date(self):
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y")

    def open_app(self, app):
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
            # Add more...
        }
        if app in apps:
            subprocess.Popen(apps[app])
            self.speak(f"Opening {app}")

    def process(self, text):
        text = text.lower().strip()
        print(f"Processing: '{text}'")

        # Precise command matching
        volume_up_phrases = ['volume up', 'turn up', 'louder']
        volume_down_phrases = ['volume down', 'turn down', 'quieter']
        if any(p in text for p in volume_up_phrases):
            self.volume_up()
            return True
        if any(p in text for p in volume_down_phrases):
            self.volume_down()
            return True
        if 'mute' in text:
            pyautogui.press('volumemute')
            self.speak("Muted")
            return True
        if 'help' in text:
            self.speak("Volume control, apps, YouTube, time, Gemini ready!")
            return True
        if 'time' in text:
            self.speak(self.get_time())
            return True
        if 'date' in text:
            self.speak(self.get_date())
            return True
        if text.startswith('open '):
            self.open_app(text[5:])
            return True
        if any(x in text for x in ['bye', 'goodbye']):
            self.speak("Goodbye!")
            return False

        # Gemini fallback
        self.speak("Gemini...")
        answer = self.chat_gemini(text)
        print(f"💡 {answer}")
        self.speak(answer[:150])
        return True

    def listen(self):
        print("🎤 Listening or type...")
        try:
            with sr.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, 0.5)
                audio = self.recognizer.listen(mic, timeout=5, phrase_time_limit=6)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Voice: {text}")
                return text
        except:
            print("📝 Type: ", end="")
            return input().lower().strip()

    def run(self):
        print("\n🎯 JARVIS FULL LIVE!")
        print("Commands: volume up/down, mute, help, time, date, open chrome, bye")
        print("Or ask Gemini anything!")
        while True:
            text = self.listen()
            if text and not self.process(text):
                break

if __name__ == "__main__":
        jarvis = JarvisAssistant()
        jarvis.run()

