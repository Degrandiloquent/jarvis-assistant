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
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 220)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Try to set a different voice (more JARVIS-like)
        voices = self.engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        # Try to set to male voice (David) if available, else first
        if len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
            print(f"Set voice to: {voices[0].name}")
        else:
            print("No voices available")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Balanced sensitivity
        self.recognizer.dynamic_energy_threshold = True  # Adapt to ambient noise
        self.recognizer.pause_threshold = 0.8  # Balanced pause for fast response while allowing command completion
        
        # Initialize volume control using pycaw
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_INPROC_SERVER, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("  ✅ Volume control ready (pycaw)")
        except Exception as e:
            print(f"Warning: pycaw volume control failed: {e}, volume control disabled")
            self.volume = None

# Initialize Gemini AI model
        try:
            print("• Initializing Gemini conversational AI...")
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("  ✅ Gemini AI ready (no hallucinations!)")
        except Exception as e:
            print(f"  ❌ Error initializing Gemini AI: {e}")
            self.model = None

        # Determine time-based greeting
        now = datetime.datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Good morning, sir!"
        elif 12 <= hour < 17:
            greeting = "Good afternoon, sir!"
        else:
            greeting = "Good evening, sir!"

        # Initialize visual indicator
        self.visual_indicator = None

        print(f"\nJARVIS initialized and ready, sir. {greeting}")
        self.speak(f"JARVIS initialized and ready, sir. {greeting}")
        self.speak("Say a command to get started.")

    def show_visual_indicator(self):
        """Show an animated visual indicator like Iron Man JARVIS sound waves"""
        if self.visual_indicator is None:
            self.visual_indicator = tk.Tk()
            self.visual_indicator.attributes("-alpha", 0.8)  # Semi-transparent
            self.visual_indicator.attributes("-topmost", True)  # Always on top
            self.visual_indicator.overrideredirect(True)  # Remove window borders
            self.visual_indicator.geometry("500x120+{}+{}".format(
                int(self.visual_indicator.winfo_screenwidth() / 2 - 250),
                int(self.visual_indicator.winfo_screenheight() - 170)
            ))
            self.visual_indicator.configure(bg='black')

            # Create canvas for animation
            self.canvas = tk.Canvas(self.visual_indicator, width=500, height=120, bg='black', highlightthickness=0)
            self.canvas.pack()

            # Initialize bars for sound wave visualization
            self.bars = []
            self.bar_heights = []
            num_bars = 20
            bar_width = 20
            spacing = 5

            for i in range(num_bars):
                x1 = i * (bar_width + spacing) + 20
                x2 = x1 + bar_width
                y1 = 60  # Center line
                y2 = 60
                bar = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#00BFFF', outline='#00BFFF')
                self.bars.append(bar)
                self.bar_heights.append(0)

            # Start animation thread
            self.animation_running = True
            self.animation_thread = threading.Thread(target=self.animate_sound_waves, daemon=True)
            self.animation_thread.start()

            self.visual_indicator.update()

    def animate_sound_waves(self):
        """Animate the sound wave bars that respond to speech volume"""
        while self.animation_running:
            try:
                # Create dynamic wave patterns that simulate responding to sound volume
                for i in range(len(self.bars)):
                    # Start with a low baseline (quiet state)
                    base_height = 3  # Very low when no sound

                    # Add dynamic variations that simulate sound volume changes
                    # More dramatic up/down movement to show sound activity
                    volume_variation = random.randint(5, 35)  # Higher range for louder sounds

                    # Add wave motion that creates flowing effect
                    wave_motion = int(15 * math.sin(time.time() * 4 + i * 0.3))  # Faster, more dynamic

                    # Add some position-based variation (center bars tend to be higher)
                    position_boost = max(0, 10 - abs(i - 10))  # Center bars get boost

                    new_height = max(2, min(45, base_height + volume_variation + wave_motion + position_boost))
                    self.bar_heights[i] = new_height

                    # Update bar position
                    x1 = i * 25 + 20
                    x2 = x1 + 20
                    y1 = 60 - new_height  # Top of bar
                    y2 = 60 + new_height  # Bottom of bar

                    self.canvas.coords(self.bars[i], x1, y1, x2, y2)

                self.canvas.update()
                time.sleep(0.06)  # Even faster for more responsive feel
            except Exception as e:
                break  # Exit if window is destroyed

    def hide_visual_indicator(self):
        """Hide the visual indicator"""
        if self.visual_indicator is not None:
            self.animation_running = False  # Stop animation
            self.visual_indicator.destroy()
            self.visual_indicator = None
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"\nJARVIS: {text}")
        self.show_visual_indicator()  # Show visual indicator when speaking
        try:
            if WIN32COM_AVAILABLE:
                # Use win32com for TTS with male voice
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                voices = speaker.GetVoices()
                if voices.Count > 0:
                    speaker.Voice = voices.Item(0)  # Set to first voice (David, male)
                speaker.Speak(text)
            else:
                # Fallback to PowerShell with male voice
                import subprocess
                escaped_text = text.replace("'", "''")
                subprocess.run(['powershell', '-c', f"Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.SelectVoice('Microsoft David Desktop'); $speak.Speak('{escaped_text}')"], check=True)
        except  Exception as e:
            print(f"TTS error: {e}")
            # Final fallback to pyttsx3
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
            self.hide_visual_indicator()  # Hide visual indicator after speaking
    
    def listen(self):
        """Listen for voice commands"""
        # Try voice recognition first
        try:
            with sr.Microphone() as source:
                print("🎤 Listening for your command...")
                try:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)

                    print("🔄 Processing...")
                    # Recognize speech using Google Speech Recognition
                    command = self.recognizer.recognize_google(audio)
                    print(f"✅ You said: {command}")
                    return command.lower()

                except sr.WaitTimeoutError:
                    print("⏱️ No speech detected, trying again...")
                except sr.UnknownValueError:
                    print("❌ Could not understand audio, trying again...")
                except sr.RequestError as e:
                    print(f"❌ Could not request results; {e}, trying again...")
                except Exception as e:
                    print(f"❌ Error: {e}, trying again...")
        except Exception as e:
            # Fallback to text input if microphone is not available
            print(f"\n💬 Microphone not available ({type(e).__name__}), using text input instead...")
            print("✏️  Type your command: ", end="")
            try:
                command = input().strip()
                if command:
                    print(f"✅ You said: {command}")
                    return command.lower()
            except EOFError:
                return None
        
        return None
    
    def set_volume(self, level):
        """Set system volume (0-100)"""
        if self.volume is None:
            self.speak("Volume control is not available")
            return
        
        volume_level = max(0, min(100, level)) / 100.0
        self.volume.SetMasterVolumeLevelScalar(volume_level, None)
        self.speak(f"Volume set to {level} percent")
    
    def volume_up(self):
        """Increase volume by 10%"""
        if self.volume is None:
            try:
                pyautogui.press('volumeup')
                self.speak("Volume increased")
            except Exception as e:
                print(f"Error increasing volume: {e}")
                self.speak("Volume control is not available")
        else:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = min(current + 0.1, 1.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            percentage = int(new_volume * 100)
            self.speak(f"Volume increased to {percentage} percent")
    
    def volume_down(self):
        """Decrease volume by 10%"""
        if self.volume is None:
            try:
                pyautogui.press('volumedown')
                self.speak("Volume decreased")
            except Exception as e:
                print(f"Error decreasing volume: {e}")
                self.speak("Volume control is not available")
        else:
            current = self.volume.GetMasterVolumeLevelScalar()
            new_volume = max(current - 0.1, 0.0)
            self.volume.SetMasterVolumeLevelScalar(new_volume, None)
            percentage = int(new_volume * 100)
            self.speak(f"Volume decreased to {percentage} percent")
    
    def mute(self):
        """Mute system audio"""
        if self.volume is None:
            self.speak("Volume control is not available")
            return
        
        self.volume.SetMute(1, None)
        self.speak("Audio muted, sir")
    
    def unmute(self):
        """Unmute system audio"""
        if self.volume is None:
            self.speak("Volume control is not available")
            return

        self.volume.SetMute(0, None)
        self.speak("Audio unmuted, sir")

    def get_youtube_video_url(self, song_name):
        """Get the first YouTube video URL for a song"""
        try:
            search_query = song_name.replace(' ', '+')
            search_url = f"https://www.youtube.com/results?search_query={search_query}"

            # Set user agent to avoid blocking
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(search_url, headers=headers)
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')

            # Find video ID using regex
            video_id_match = re.search(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
            if video_id_match:
                video_id = video_id_match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"

        except Exception as e:
            print(f"Error getting YouTube video URL: {e}")

        return None

    def search_google(self, query):
        """Search for a query on Google using Chrome"""
        try:
            search_query = query.replace(' ', '+')
            search_url = f"https://www.google.com/search?q={search_query}"
            subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', search_url])
            self.speak(f"Searching for {query} on Google, sir")
        except Exception as e:
            print(f"Error searching on Google: {e}")
            self.speak("Sorry, I couldn't search on Google")

    def open_application(self, app_name):
        """Open applications"""
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'browser': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'file explorer': 'explorer.exe',
            'explorer': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'whatsapp': os.path.expanduser(r'~\AppData\Local\WhatsApp\WhatsApp.exe'),
            'outlook': r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
        }

        if app_name in apps:
            try:
                subprocess.Popen(apps[app_name])
                self.speak(f"Opening {app_name}, sir")
            except Exception as e:
                print(f"Error opening {app_name}: {e}")
                self.speak(f"Sorry, I couldn't open {app_name}")
        elif app_name == 'youtube':
            try:
                subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'https://www.youtube.com'])
                self.speak("Opening YouTube in Chrome, sir")
            except Exception as e:
                print(f"Error opening YouTube: {e}")
                self.speak("Sorry, I couldn't open YouTube")
        elif app_name == 'windows search bar' or app_name == 'search':
            try:
                pyautogui.hotkey('win', 's')
                self.speak("Opening Windows Search Bar, sir")
            except Exception as e:
                print(f"Error opening Windows Search Bar: {e}")
                self.speak("Sorry, I couldn't open Windows Search Bar")
        else:
            self.speak(f"I don't know how to open {app_name} yet, sir")

    def close_application(self, app_name):
        """Close applications"""
        apps = {
            'chrome': 'chrome.exe',
            'browser': 'chrome.exe',
            'edge': 'msedge.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'file explorer': 'explorer.exe',
            'explorer': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'powerpoint': 'POWERPNT.EXE',
            'outlook': 'OUTLOOK.EXE',
            'vscode': 'Code.exe',
            'spotify': 'Spotify.exe',
            'vlc': 'vlc.exe',
            'photoshop': 'Photoshop.exe',
            'firefox': 'firefox.exe',
            'opera': 'opera.exe',
            'whatsapp': 'WhatsApp.exe',
        }

        if app_name in apps:
            try:
                # Use taskkill to close the application
                subprocess.run(['taskkill', '/f', '/im', apps[app_name]], check=True)
                self.speak(f"Closing {app_name}, sir")
            except subprocess.CalledProcessError:
                self.speak(f"Sorry, I couldn't close {app_name}. It might not be running.")
            except Exception as e:
                print(f"Error closing {app_name}: {e}")
                self.speak(f"Sorry, I couldn't close {app_name}")
        elif app_name == 'windows search bar' or app_name == 'search':
            try:
                pyautogui.press('esc')
                self.speak("Closing Windows Search Bar, sir")
            except Exception as e:
                print(f"Error closing Windows Search Bar: {e}")
                self.speak("Sorry, I couldn't close Windows Search Bar")
        else:
            self.speak(f"I don't know how to close {app_name} yet, sir")
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'screenshot_{timestamp}.png'
            screenshot.save(filename)
            self.speak("Screenshot taken and saved, sir")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            self.speak("Sorry, I couldn't take a screenshot")
    
    def open_all_desktop_apps(self):
        """Open all applications on the desktop"""
        try:
            import os
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            opened_count = 0
            
            for file in os.listdir(desktop_path):
                if file.endswith(('.lnk', '.exe', '.bat', '.cmd')):
                    file_path = os.path.join(desktop_path, file)
                    try:
                        subprocess.Popen(file_path, shell=True)
                        opened_count += 1
                    except Exception as e:
                        print(f"Error opening {file}: {e}")
            
            if opened_count > 0:
                self.speak(f"Opened {opened_count} applications from your desktop, sir")
            else:
                self.speak("No applications found on your desktop to open, sir")
        except Exception as e:
            print(f"Error opening desktop apps: {e}")
            self.speak("Sorry, I couldn't open the desktop applications")
    
    def shutdown_computer(self):
        """Shutdown the computer"""
        self.speak("Shutting down the computer in 10 seconds, sir. Goodbye!")
        try:
            import os
            os.system("shutdown /s /t 10")
        except Exception as e:
            print(f"Error shutting down: {e}")
            self.speak("Sorry, I couldn't shutdown the computer")

    def restart_computer(self):
        """Restart the computer"""
        self.speak("Restarting the computer in 10 seconds, sir. I'll be back!")
        try:
            os.system("shutdown /r /t 10")
        except Exception as e:
            print(f"Error restarting: {e}")
            self.speak("Sorry, I couldn't restart the computer")

    def think(self, command):
        """Analyze user input to determine if it's a command or conversational query"""
        command_keywords = [
            'volume', 'mute', 'unmute', 'open', 'close', 'screenshot', 'shutdown', 'restart',
            'good morning', 'good afternoon', 'good evening', 'goodbye',
            'exit', 'quit', 'help', 'what can you do', 'time', 'play', 'youtube', 'search', 'find'
        ]

        # Check if the command contains any known command keywords
        for keyword in command_keywords:
            if keyword in command:
                return 'command'

        # If no command keywords found, treat as conversational
        return 'conversation'

    def generate_response(self, user_input):
        """Generate a conversational response using Gemini AI (no hallucinations!)"""
        if not self.model:
            return "Conversational AI not available. Say 'help' for commands."

        try:
            response = self.model.generate_content(user_input)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return "I'm having trouble connecting to Gemini right now. Try a command like 'help'."

    def process_command(self, command):
        """Process and execute commands"""

        # Check for Jarvis trigger and respond with "sir"
        if command.lower().startswith("jarvis") or "hey jarvis" in command.lower():
            self.speak("sir")
            # Remove the trigger phrase to process the rest of the command
            if command.lower().startswith("jarvis"):
                command = command[6:].strip()  # Remove "jarvis" and any leading space
            elif "hey jarvis" in command.lower():
                command = command.lower().replace("hey jarvis", "").strip()
            # If nothing left after removing trigger, just acknowledge and continue
            if not command:
                return True

        # Volume controls
        if 'volume up' in command or 'increase volume' in command or 'louder' in command or 'raise volume' in command:
            self.volume_up()
        
        elif 'volume down' in command or 'decrease volume' in command or 'lower volume' in command or 'quieter' in command or 'reduce volume' in command:
            self.volume_down()
        
        elif 'mute' in command:
            self.mute()
        
        elif 'unmute' in command:
            self.unmute()
        
        elif 'set volume' in command or 'volume to' in command:
            try:
                # Extract number from command
                words = command.split()
                for i, word in enumerate(words):
                    if word.isdigit():
                        level = int(word)
                        self.set_volume(level)
                        return True
                self.speak("I couldn't understand the volume level, sir")
            except Exception as e:
                print(f"Error setting volume: {e}")
                self.speak("Sorry, I couldn't set the volume")
        
        # Open applications
        elif 'open' in command:
            app = command.replace('open', '').strip()
            self.open_application(app)

        # Close applications
        elif 'close' in command:
            app = command.replace('close', '').strip()
            self.close_application(app)

        # Screenshot
        elif 'screenshot' in command or 'take a screenshot' in command:
            self.take_screenshot()
        
        # Open all desktop apps
        elif 'open all desktop apps' in command or 'open desktop apps' in command or 'open all apps' in command:
            self.open_all_desktop_apps()
        
        # Shutdown computer
        elif 'shutdown computer' in command or 'turn off laptop' in command or 'shutdown laptop' in command or 'switch off the laptop' in command or 'shut down computer' in command:
            self.shutdown_computer()

        # Restart computer
        elif 'restart computer' in command or 'restart laptop' in command:
            self.restart_computer()

        # Time query
        elif 'what time is it' in command or 'current time' in command or 'what is the time' in command or 'tell me the time' in command:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            self.speak(f"{current_time}")

        # Date query
        elif 'what is the date' in command or 'current date' in command or 'what date is it' in command or 'tell me the date' in command:
            now = datetime.datetime.now()
            current_date = now.strftime("%A, %B %d, %Y")
            self.speak(f"{current_date}")

        # Greetings
        elif 'good morning' in command:
            self.speak("Good morning, sir! I hope you have a productive day.")
        
        elif 'good afternoon' in command:
            self.speak("Good afternoon, sir! How can I assist you today?")
        
        elif 'good evening' in command:
            self.speak("Good evening, sir! Ready to help with anything you need.")
        
        # Exit commands
        elif 'goodbye' in command or 'exit' in command or 'quit' in command:
            self.speak("Goodbye, sir. It's been a pleasure serving you.")
            return False
        
        # Search on Google
        elif 'search' in command and 'youtube' not in command:
            try:
                # Extract search query
                query = command.replace('search', '').strip()
                if query:
                    self.search_google(query)
                else:
                    self.speak("Please specify what to search for, sir")
            except Exception as e:
                print(f"Error searching on Google: {e}")
                self.speak("Sorry, I couldn't search on Google")

        # Play song on YouTube
        elif 'play' in command:
            try:
                # Extract song name from command
                song_name = command.replace('play', '').strip()
                if song_name:
                    # Try to get direct video URL first (most reliable)
                    video_url = self.get_youtube_video_url(song_name)
                    if video_url:
                        # Open direct video URL
                        subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', video_url])
                        self.speak(f"Opening {song_name} on YouTube. Please click play if it doesn't start automatically, sir")
                    else:
                        # Fallback to search page
                        search_query = song_name.replace(' ', '+')
                        search_url = f"https://www.youtube.com/results?search_query={search_query}"
                        subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', search_url])
                        self.speak(f"Searching for {song_name} on YouTube. Please select and play the video, sir")
                else:
                    self.speak("Please specify a song name, sir")
            except Exception as e:
                print(f"Error opening YouTube: {e}")
                self.speak("Sorry, I couldn't open YouTube")

        # Search video on YouTube
        elif ('search' in command or 'find' in command) and 'youtube' in command:
            try:
                # Extract video name from command
                if 'search' in command:
                    video_name = command.replace('search', '').replace('on youtube', '').strip()
                elif 'find' in command:
                    video_name = command.replace('find', '').replace('on youtube', '').strip()
                else:
                    video_name = command.replace('youtube', '').strip()

                if video_name:
                    search_url = f"https://www.youtube.com/search?q={video_name.replace(' ', '+')}"
                    subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', search_url])
                    self.speak(f"Searching for {video_name} on YouTube, sir")
                else:
                    self.speak("Please specify what to search for on YouTube, sir")
            except Exception as e:
                print(f"Error searching on YouTube: {e}")
                self.speak("Sorry, I couldn't search on YouTube")

        # Help
        elif 'help' in command or 'what can you do' in command:
            self.speak("I can control volume, open/close apps (Chrome, WhatsApp, etc.), screenshots, desktop apps, shutdown/restart, time/date, Google/YouTube search/play, greetings. Now with Gemini AI for smart chat (no hallucinations)! Say 'help', 'volume up', 'open chrome', 'play song', or chat freely.")
        
        # Default response - check if it's conversational
        else:
            input_type = self.think(command)
            if input_type == 'conversation':
                response = self.generate_response(command)
                self.speak(response)
            else:
                self.speak("I'm not sure how to do that yet, sir. Say help to hear what I can do.")

        return True
    
    def run(self):
        """Main loop"""
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
