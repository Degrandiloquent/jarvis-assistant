import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pyautogui
import datetime
import urllib.request
import re
import tkinter as tk
import threading
import time
import random
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_INPROC_SERVER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
try:
    import win32com.client
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False

import warnings
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
        try:
            self.show_visual_indicator()
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
        finally:
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
        print("🚀 JARVIS FINAL - Gemini 2.5 Flash FIXED")
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 180)
        
        self.recognizer = sr.Recognizer()
        self.model = None
        
        # FIXED Gemini - use gemini-2.5-flash (available per list_models)
        if GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                print("Trying Gemini 2.5 Flash...")
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ GEMINI 2.5 FLASH READY - ASK ANYTHING!")
            except Exception as e1:
                try:
                    print("Fallback to gemini-2.0-flash...")
                    self.model = genai.GenerativeModel('gemini-2.0-flash')
                    print("✅ GEMINI 2.0 Flash READY!")
                except Exception as e2:
                    print(f"All Gemini models failed: {e1}, {e2}")
        
        self.speak("JARVIS with working Gemini ready. Test me!")

    def chat_gemini(self, query):
        if not self.model:
            return "Gemini offline. Commands: help, volume up/down, mute, goodbye"
        try:
            response = self.model.generate_content(query)
            return response.text.strip()
        except Exception as e:
            return f"Gemini API error: {str(e)}[:50]. Try simple query."

    def listen(self):
        print("🎤 Listening (timeout 4s) or type...")
        try:
            with sr.Microphone() as mic:
                r = self.recognizer
                r.adjust_for_ambient_noise(mic, 0.3)
                audio = r.listen(mic, timeout=4, phrase_time_limit=6)
                text = r.recognize_google(audio).lower()
                print(f"Voice: {text}")
                return text
        except:
            print("📝 Type: ", end="")
            return input()

    def process(self, text):
        text = text.lower().strip()
        print(f"Processing: '{text}'")
        
        # Quick commands
        if any(x in text for x in ['volume up', 'turn volume up', 'louder']):
            pyautogui.press('volumeup')
            self.speak("Volume up!")
            return True
        if any(x in text for x in ['volume down', 'turn volume down', 'quieter']):
            pyautogui.press('volumedown')
            self.speak("Volume down!")
            return True
        if 'mute' in text or 'toggle mute' in text:
            pyautogui.press('volumemute')
            self.speak("Muted")
            return True
        if any(x in text for x in ['help', 'what can you do']):
            self.speak("Gemini chat + volume control ready!")
            return True
        if any(x in text for x in ['bye', 'goodbye', 'exit', 'quit']):
            self.speak("Goodbye sir!")
            return False

        # Gemini for all queries
        self.speak("Gemini...")
        answer = self.chat_gemini(text)
        print(f"💡 {answer}")
        self.speak(answer[:100])  # Short speak
        return True

    def run(self):
        print("\n🎯 JARVIS FINAL LIVE!")
        print("Type/say ANY question - Gemini answers!")
        print("Or: volume up/down, mute, help, goodbye")
        print("-" * 50)
        while True:
            text = self.listen()
            if not text:
                continue
            if not self.process(text):
                break

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
