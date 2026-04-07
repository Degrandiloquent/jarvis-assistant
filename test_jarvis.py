import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class JarvisAssistant:
    def __init__(self):
        print("=" * 50)
        print("JARVIS - Just A Rather Very Intelligent System")
        print("=" * 50)
        print("\nStarting initialization...")
        
        # Initialize text-to-speech engine
        print("• Initializing text-to-speech engine...")
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 170)  # Speed of speech
            self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
            
            # Try to set a different voice (more JARVIS-like)
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            print("  ✅ Text-to-speech ready")
        except Exception as e:
            print(f"  ❌ Error initializing text-to-speech: {e}")
            self.engine = None
        
        # Initialize speech recognizer
        print("• Initializing speech recognizer...")
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000  # Adjust sensitivity
            print("  ✅ Speech recognizer ready")
        except Exception as e:
            print(f"  ❌ Error initializing speech recognizer: {e}")
            self.recognizer = None
        
        # Initialize volume control
        print("• Initializing volume control...")
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("  ✅ Volume control ready")
        except Exception as e:
            print(f"  ⚠️ Volume control unavailable: {e}")
            self.volume = None
        
        print("\n" + "=" * 50)
        print("JARVIS initialized and ready, sir.")
        print("=" * 50)

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    print("Test initialization complete!")