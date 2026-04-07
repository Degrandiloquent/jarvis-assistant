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
        """Convert text to speech - MOVED BEFORE __init__"""
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
        """Show animated visual indicator"""
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
        print("JARVIS - Just A Rather Very Intelligent System")
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
            print("  ✅ Volume control ready (pycaw)")
        except Exception as e:
            print(f"Warning: pycaw volume control failed: {e}, volume control disabled")
            self.volume = None

        try:
            print("• Initializing Gemini conversational AI...")
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("  ✅ Gemini AI ready (no hallucinations!)")
        except Exception as e:
            print(f"  ❌ Error initializing Gemini AI: {e}")
            self.model = None

        now = datetime.datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Good morning, sir!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon, sir!"
        else:
            greeting = "Good evening, sir!"

        self.visual_indicator = None

        print(f"\nJARVIS initialized and ready, sir. {greeting}")
        self.speak(f"JARVIS initialized and ready, sir. {greeting}")
        self.speak("Say a command to get started.")

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                print("🔄 Processing...")
                command = self.recognizer.recognize_google(audio)
                print(f"✅ You said: {command}")
                return command.lower()
        except:
            print("💬 Using text input...")
            return input("Type command: ").strip().lower()

    def volume_up(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = min(current + 0.1, 1.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            percentage = int(new_volume * 100)
            self.speak(f"Volume increased to {percentage} percent")
        else:
            pyautogui.press('volumeup')
            self.speak("Volume increased")

    def volume_down(self):
        if self.volume:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = max(current - 0.1, 0.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            percentage = int(new_volume * 100)
            self.speak(f"Volume decreased to {percentage} percent")
        else:
            pyautogui.press('volumedown')
            self.speak("Volume decreased")

    def set_volume(self, level):
        if self.volume:
            volume_level = max(0, min(100, level)) / 100.0
            self.volume.SetMasterVolumeLevelScalar(volume_level, None)
            self.speak(f"Volume set to {level} percent")

    def mute(self):
        if self.volume:
            self.volume.SetMute(1, None)
            self.speak("Audio muted, sir")

    def unmute(self):
        if self.volume:
            self.volume.SetMute(0, None)
            self.speak("Audio unmuted, sir")

    def open_application(self, app_name):
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
        }
        if app_name in apps:
            subprocess.Popen(apps[app_name])
            self.speak(f"Opening {app_name}")

    def process_command(self, command):
        if 'volume up' in command:
            self.volume_up()
        elif 'volume down' in command:
            self.volume_down()
        elif 'mute' in command:
            self.mute()
        elif 'help' in command:
            self.speak("I can control volume and open apps. Say help anytime.")
        elif 'goodbye' in command:
            self.speak("Goodbye sir")
            return False
        else:
            self.speak("Command not recognized. Say help.")
        return True

    def run(self):
        print("\n" + "=" * 50)
        print("JARVIS RUNNING! Say 'jarvis' then command or type.")
        print("Commands: volume up/down, mute, open chrome, help, goodbye")
        print("=" * 50)
        
        while True:
            command = self.listen()
            if command and self.process_command(command):
                continue
            break

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
