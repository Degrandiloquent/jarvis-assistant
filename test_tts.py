import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
print(f"Available voices: {len(voices)}")
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name} - {voice.id}")

if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)
    print(f"Set voice to: {voices[0].name}")

engine.say("Hello, this is a test of text to speech.")
engine.runAndWait()
print("TTS test completed.")
