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

import google.generativeai as genai
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
            print(f"TTS error: {e}")
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
            self.visual_indicator.geometry("500x120+{}+{}".format(
                int(self.visual_indicator.winfo_screenwidth() / 2 - 250),
                int(self.visual_indicator.winfo_screenheight() - 170)
            ))
            self.visual_indicator.configure(bg='black')
            self.canvas = tk.Canvas(self.visual_indicator, width=500, height=120, bg='black', highlightthickness=0)
            self.canvas.pack()
            self.bars = []
            self.bar_heights = []
            num_bars = 20
            bar_width = 20
            spacing = 5
            for i in range(num_bars):
                x1 = i * (bar_width + spacing) + 20
                x2 = x1 + bar_width
                y1 = 60
                y2 = 60
                bar = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#00BFFF', outline='#00BFFF')
                self.bars.append(bar)
                self.bar_heights.append(0)
            self.animation_running = True
            self.animation_thread = threading.Thread(target=self.animate_sound_waves, daemon=True)
            self.animation_thread.start()
            self.visual_indicator.update()

    def animate_sound_waves(self):
        while self.animation_running:
            try:
                for i in range(len(self.bars)):
                    base_height = 3
                    volume_variation = random.randint(5, 35)
                    wave_motion = int(15 * math.sin(time.time() * 4 + i * 0.3))
                    position_boost = max(0, 10 - abs(i - 10))
                    new_height = max(2, min(45, base_height + volume_variation + wave_motion + position_boost))
                    self.bar_heights[i] = new_height
                    x1 = i * 25 + 20
                    x2 = x1 + 20
                    y1 = 60 - new_height
                    y2 = 60 + new_height
                    self.canvas.coords(self.bars[i], x1, y1, x2, y2)
                self.canvas.update()
                time.sleep(0.06)
            except Exception:
                break

    def hide_visual_indicator(self):
        if self.visual_indicator is not None:
            self.animation_running = False
            self.visual_indicator.destroy()
            self.visual_indicator = None

    def __init__(self):
        print("=" * 50)
        print("JARVIS - FULL GEMINI AI Version")
        print("=" * 50)
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 220)
        self.engine.setProperty('volume', 1.0)
        
        voices = self.engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        if len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
            print(f"Set voice to: {voices[0].name}")
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_INPROC_SERVER, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("  ✅ Volume control ready")
        except Exception as e:
            print(f"pycaw failed: {e}")
            self.volume = None

        try:
            print("Initializing FULL Gemini AI...")
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ FULL Gemini AI ACTIVE - Chat about ANYTHING!")
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            self.model = None

        self.visual_indicator = None

        print("\nFULL JARVIS + GEMINI ready!")
        self.speak("Full JARVIS with Gemini AI ready. Ask ANY question!")

    def generate_gemini_response(self, user_input):
        """Gemini AI - answers ANY text input intelligently"""
        if not self.model:
            return "Gemini not available. Use voice commands like 'help'."
        try:
            response = self.model.generate_content(user_input)
            return response.text.strip()
        except Exception as e:
            return f"Gemini error: {e}. Try again."

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("🔄 Processing...")
                command = self.recognizer.recognize_google(audio)
                print(f"✅ You said: {command}")
                return command.lower()
        except:
            print("💬 Text mode - type ANY question/ command:")
            return input().strip().lower()

    def process_command(self, text):
        """Enhanced: Commands OR Gemini chat fallback"""
        # Commands first
        if any(word in text for word in ['volume up', 'volume down', 'louder', 'quieter', 'mute']):
            if 'up' in text or 'louder' in text:
                self.volume_up()
            elif 'down' in text or 'quieter' in text:
                self.volume_down()
            else:
                self.mute()
            return True
        elif 'help' in text:
            self.speak("Volume control, apps, OR ask Gemini ANY question! Gemini answers everything.")
            return True
        elif 'goodbye' in text or 'exit' in text:
            self.speak("Goodbye!")
            return False

        # GEMINI AI for ALL other input - type ANYTHING!
        print("🤖 Gemini thinking...")
        response = self.generate_gemini_response(text)
        print(f"Gemini: {response}")
        self.speak(response)
        return True

    def volume_up(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = min(current + 0.1, 1.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            self.speak("Volume up")
        else:
            pyautogui.press('volumeup')
            self.speak("Volume up")

    def volume_down(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = max(current - 0.1, 0.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            self.speak("Volume down")
        else:
            pyautogui.press('volumedown')
            self.speak("Volume down")

    def run(self):
        print("\n" + "="*60)
        print("🔥 JARVIS + FULL GEMINI AI LIVE!")
        print("• Type/Say ANY question → Gemini answers")
        print("• volume up/down/mute/help/goodbye")
        print("="*60)
        self.speak("Gemini ready - ask anything!")
        
        while True:
            text = self.listen()
            if text:
                self.process_command(text)

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
