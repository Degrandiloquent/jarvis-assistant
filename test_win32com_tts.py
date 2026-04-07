try:
    import win32com.client
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak("Hello, this is a test of win32com TTS.")
    print("Win32com TTS executed.")
except Exception as e:
    print(f"Error: {e}")
