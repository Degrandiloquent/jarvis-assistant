import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pyautogui
import datetime
import urllib.request
import urllib.parse
import re
import tkinter as tk
import threading
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
        except:
            self.engine.say(text)
            self.engine.runAndWait()
        self.hide_visual_indicator()

    def show_visual_indicator(self):
        if self.visual_indicator is None:
            self.visual_indicator = tk.Tk()
            self.visual_indicator.attributes("-alpha", 0.8)
            self.visual_indicator.attributes("-topmost", True)
            self.visual_indicator.overrideredirect(True)
            self.visual_indicator.geometry("500x120+50+50")
            self.visual_indicator.configure(bg='black')
            self.canvas = tk.Canvas(self.visual_indicator, width=500, height=120, bg='black', highlightthickness=0)
            self.canvas.pack()
            self.bars = []
            num_bars = 20
            for i in range(num_bars):
                x1 = i * 25 + 20
                bar = self.canvas.create_rectangle(x1, 60, x1+20, 60, fill='#00BFFF')
                self.bars.append(bar)
            self.animation_running = True
            self.visual_indicator.after(50, self.animate_visual_frame)

    def animate_visual_frame(self):
        if self.animation_running and self.visual_indicator:
            try:
                for i in range(len(self.bars)):
                    h = random.randint(10, 50)
                    x1, y1, x2, y2 = self.canvas.coords(self.bars[i])
                    self.canvas.coords(self.bars[i], x1, 60-h//2, x2, 60+h//2)
                self.canvas.update()
                self.visual_indicator.after(80, self.animate_visual_frame)
            except tk.TclError:
                self.hide_visual_indicator()

    def hide_visual_indicator(self):
        self.animation_running = False
        if self.visual_indicator:
            self.visual_indicator.destroy()
            self.visual_indicator = None
            self.canvas = None
            self.bars = None

    def __init__(self):
        print("=" * 60)
        print("🤖 JARVIS ULTIMATE - ALL FEATURES + GEMINI 2.5 FLASH")
        print("=" * 60)

        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 200)

        self.recognizer = sr.Recognizer()
        self.model = None

        # Volume control (pycaw)
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_INPROC_SERVER, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("✅ Advanced volume control ready")
        except Exception as e:
            print(f"Volume control: {e}")
            self.volume = None

        # Gemini 2.5 Flash
        if GEMINI_AVAILABLE:
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ GEMINI 2.5 FLASH - Ask anything!")
            except:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ GEMINI 1.5 FLASH ready")

        self.visual_indicator = None
        self.speak("JARVIS Ultimate online with all capabilities")

    def volume_up(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new = min(current + 0.1, 1.0)
            self.volume.SetMasterVolumeLevelScalar(new, None)
            self.speak(f"Volume {int(new*100)}%")
        else:
            pyautogui.press('volumeup')
            self.speak("Volume up")

    def volume_down(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new = max(current - 0.1, 0.0)
            self.volume.SetMasterVolumeLevelScalar(new, None)
            self.speak(f"Volume {int(new*100)}%")
        else:
            pyautogui.press('volumedown')
            self.speak("Volume down")

    def mute_toggle(self):
        if self.volume:
            self.volume.SetMute(1, None)
            self.speak("Muted")
        else:
            pyautogui.press('volumemute')
            self.speak("Muted")

    def open_application(self, app_name):
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'youtube': [r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'https://www.youtube.com'],
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
            'explorer': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'whatsapp': r'C:\Users\xihlu\AppData\Local\WhatsApp\WhatsApp.exe',
            'outlook': 'outlook.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'paint': 'mspaint.exe',
        }
        if app_name in apps:
            if isinstance(apps[app_name], list):
                subprocess.Popen(apps[app_name])
            else:
                subprocess.Popen(apps[app_name])
            self.speak(f"Opening {app_name}")
            return True
        return False

    def close_application(self, app_name):
        close_map = {
            'chrome': 'chrome.exe',
            'youtube': 'chrome.exe',
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
            'explorer': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'whatsapp': 'WhatsApp.exe',
            'outlook': 'outlook.exe',
            'edge': 'msedge.exe',
            'paint': 'mspaint.exe',
        }
        app_key = app_name.lower().strip()
        if app_key in close_map:
            try:
                subprocess.run(['taskkill', '/f', '/im', close_map[app_key]], check=True)
                self.speak(f"Closing {app_name}")
                return True
            except subprocess.CalledProcessError:
                self.speak(f"Could not close {app_name}, might not be running")
            except Exception:
                self.speak(f"Error closing {app_name}")
        else:
            self.speak(f"{app_name} not in supported apps")
        return False

    def get_youtube_url(self, song):
        try:
            search = song.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req).read().decode()
            match = re.search(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
            if match:
                return f"https://www.youtube.com/watch?v={match.group(1)}"
        except:
            pass
        return f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"

    def get_time(self):
        return datetime.datetime.now().strftime("%I:%M %p")

    def get_date(self):
        return datetime.datetime.now().strftime("%A, %B %d, %Y")

    def chat_gemini(self, query):
        if not self.model:
            return "Gemini unavailable"
        try:
            response = self.model.generate_content(query)
            return response.text[:200]
        except:
            return "Gemini error"

    def process_command(self, text):
        text = text.lower().strip()
        print(f"Processing: '{text}'")

        # Trigger
        if text.startswith('jarvis') or 'hey jarvis' in text:
            self.speak("sir")
            text = re.sub(r'(jarvis|hey jarvis)', '', text).strip()
            if not text:
                return True

        # Volume
        if any(p in text for p in ['volume up', 'turn up volume', 'louder']):
            self.volume_up()
            return True
        if any(p in text for p in ['volume down', 'turn down', 'quieter']):
            self.volume_down()
            return True
        if 'mute' in text:
            self.mute_toggle()
            return True

        # Apps & Search
        if 'open ' in text:
            app = text.split('open ', 1)[1].strip()
            self.open_application(app)
            return True
        elif 'close ' in text:
            app = text.split('close ', 1)[1].strip()
            self.close_application(app)
            return True
        elif 'search ' in text:
            query = text.split('search ', 1)[1].strip()
            if 'google' in text or not any(x in text for x in ['youtube', 'yt']):
                search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', search_url])
                self.speak(f"Searching Google for {query}")
            else:
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', search_url])
                self.speak(f"Searching YouTube for {query}")
            return True

        # YouTube
        if 'youtube' in text or 'yt ' in text:
            if 'play ' in text:
                song = text.split('play ', 1)[1].replace(' on youtube', '')
                url = self.get_youtube_url(song)
                subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', url])
                self.speak(f"Playing {song}")
                return True
            subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'https://www.youtube.com'])
            self.speak("YouTube opened")
            return True

        # Time/Date
        if 'time' in text:
            self.speak(self.get_time())
            return True
        if 'date' in text:
            self.speak(self.get_date())
            return True

        # Help
        if 'help' in text:
            self.speak("Commands: volume up/down/mute, open/close [chrome calculator notepad explorer task manager whatsapp outlook edge paint], search [query], play [song], time/date, Gemini. bye/exit to quit.")
            return True

        # Goodbye
        if any(x in text for x in ['goodbye', 'bye', 'exit']):
            self.speak("Goodbye sir!")
            return False

        # Gemini
        answer = self.chat_gemini(f"JARVIS assistant: {text}")
        print(f"💡 Gemini: {answer}")
        self.speak(str(answer))
        return True

    def listen(self):
        print("🎤 Listening (5s timeout) or type...")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, 0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                return self.recognizer.recognize_google(audio).lower()
        except:
            print("📝 Type: ", end="")
            return input(">> ").lower().strip()

    def run(self):
        print("\n" + "=" * 60)
        print("🤖 JARVIS ULTIMATE LIVE - ALL FEATURES!")
        print("Commands: volume up/down/mute, open/close [chrome/calculator/notepad/explorer/task manager/whatsapp/outlook/edge/paint], search [query], play [song], time/date, help, bye")
        print("=" * 60)
        while True:
            try:
                text = self.listen()
                if text and self.process_command(text):
                    continue
                break
            except KeyboardInterrupt:
                break
        self.speak("JARVIS offline.")

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
