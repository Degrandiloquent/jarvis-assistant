import subprocess

text = "Hello, this is a test of PowerShell TTS."
try:
    result = subprocess.run(['powershell', '-c', f"Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak('{text}')"], capture_output=False)
    print("PowerShell TTS executed.")
except Exception as e:
    print(f"Error: {e}")
