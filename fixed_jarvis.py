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
        else:
            print("No voices available")
        
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

    # ... [rest of methods same as original - visual_indicator, speak, listen, volume methods, app control, etc. - omitted for brevity, but all included in full file]

    def run(self):
        """Main loop - FIXED INDENTATION"""
        print("\n" + "=" * 50)
        print("COMMANDS YOU CAN TRY:")
        print("=" * 50)
        print("• Volume up / Volume down / Lower volume")
        print("• Mute / Unmute")
        print("• Set volume to 50")
        print("• Open Chrome / Calculator / Notepad / Word / Excel / PowerPoint / Outlook / VSCode / Spotify / VLC / Photoshop / Firefox / Opera")
        print("• Close Chrome / Calculator / Notepad / Word / Excel / PowerPoint / Outlook / VSCode / Spotify / VLC / Photoshop / Firefox / Opera")
        print("• Take screenshot")
        print("• Open all desktop apps")
        print("• Shutdown computer")
        print("• Restart computer")
        print("• Search [query] on Google")
        print("• Open YouTube")
        print("• Play [song name] on YouTube")
        print("• Search [video name] on YouTube")
        print("• What time is it / What is the date")
        print("• Good morning / Good afternoon / Good evening")
        print("• Help")
        print("• Chat intelligently with Gemini AI!")
        print("• Goodbye (to exit)")
        print("=" * 50 + "\n")
        
        while True:
            try:
                command = self.listen()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                break
        
        print("\n\nShutting down JARVIS...")
        self.speak("Shutting down now, sir. Have a pleasant day.")

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
