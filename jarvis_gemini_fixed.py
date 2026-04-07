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

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
GEMINI_API_KEY = "AIzaSyDalrZNGeDakdA5wExueQVjcZ-bd-qxMAk"

class JarvisAssistant:
    def speak(self, text):
        print(f"\nJARVIS: {text}")
        self.show_visual_indicator()
        try:
            if WIN32COM_AVAILABLE:
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                voices = speaker.GetVoices()
                if voices.Count > 0:
                    speaker.Voice = voices.Item(0)
                speaker.Speak(text)
            else:
                escaped_text = text.replace("'", "''")
                subprocess.run(['powershell', '-c', f"Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.SelectVoice('Microsoft David Desktop'); $speak.Speak('{escaped_text}')"], check=True)
        except Exception as e:
            print(f"TTS fallback error: {e}")
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
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
            self.animation_thread = threading.Thread(target=self.animate_bars, daemon=True)
            self.animation_thread.start()

    def animate_bars(self):
        while self.animation_running:
            for i, bar in enumerate(self.bars):
                height = random.randint(10, 50)
                x1 = self.canvas.coords(bar)[0]
                self.canvas.coords(bar, x1, 60-height, x1+20, 60+height)
            self.canvas.update()
            time.sleep(0.1)
            if not self.animation_running:
                break

    def hide_visual_indicator(self):
        self.animation_running = False
        if self.visual_indicator:
            self.visual_indicator.destroy()
            self.visual_indicator = None

    def __init__(self):
        print("=" * 60)
        print("🔥 JARVIS - FIXED GEMINI + Voice Assistant")
        print("=" * 60)
        
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        self.volume = None
        self.model = None
        self.visual_indicator = None
        self.animation_running = False

        # FIXED Gemini with fallback model
        if GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                # Try multiple models - gemini-1.5-flash-exp first (common), fallback to gemini-pro
                try:
                    self.model = genai.GenerativeModel('gemini-1.5-flash-exp')
                    print("✅ Gemini 1.5 Flash Experimental READY")
                except:
                    try:
                        self.model = genai.GenerativeModel('gemini-pro')
                        print("✅ Gemini Pro READY (stable fallback)")
                    except:
                        print("❌ Gemini models unavailable")
            except Exception as e:
                print(f"Gemini setup error: {e}")

        now = datetime.datetime.now().hour
        greeting = "Good morning sir!" if now < 12 else "Good afternoon sir!" if now < 18 else "Good evening sir!"
        print(f"JARVIS ready! {greeting}")
        self.speak(greeting)

    def gemini_chat(self, query):
        """Robust Gemini with model list check"""
        if not self.model:
            return "Gemini not available - use commands: volume up, help"
        try:
            response = self.model.generate_content(query)
            return response.text[:200]  # Limit length
        except Exception as e:
            # List available models on error
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                return f"Gemini error. Available: {models[:3]}. Try 'help'"
            except:
                return f"Gemini temporarily unavailable: {str(e)[:100]}. Say 'help'"

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You: {command}")
                return command
        except:
            print("💬 Type anything:")
            return input().lower()

    def process_input(self, text):
        text = text.lower()
        # Priority commands
        if any(x in text for x in ['volume up', 'louder']):
            if self.volume:
                # pycaw code...
                pass
            else:
                pyautogui.press('volumeup')
            self.speak("Volume up")
            return True
        elif any(x in text for x in ['volume down', 'quieter']):
            pyautogui.press('volumedown')
            self.speak("Volume down")
            return True
        elif 'mute' in text:
            pyautogui.press('volumemute')
            self.speak("Muted")
            return True
        elif 'help' in text:
            self.speak("Commands or ask Gemini anything!")
            return True
        elif any(x in text for x in ['goodbye', 'exit', 'quit']):
            self.speak("Goodbye sir!")
            return False

        # GEMINI for everything else
        print("🤖 Gemini...")
        response = self.gemini_chat(text)
        print(f"Gemini: {response}")
        self.speak(response)
        return True

    def run(self):
        print("\n🚀 JARVIS + GEMINI LIVE - Ask ANYTHING or volume/help!")
        while True:
            text = self.listen()
            if text and self.process_input(text):
                continue
            break

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
