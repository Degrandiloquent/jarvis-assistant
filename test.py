print("=" * 60)
print("JARVIS DIAGNOSTIC TEST")
print("=" * 60)
print("\nThis will test each component to find the problem...\n")

# Test 1: Basic Python
print("[TEST 1/5] Testing basic Python...")
print("  ✅ Python is working!")

# Test 2: Import pyttsx3
print("\n[TEST 2/5] Importing pyttsx3...")
try:
    import pyttsx3
    print("  ✅ pyttsx3 imported successfully")
except Exception as e:
    print(f"  ❌ Error importing pyttsx3: {e}")
    input("\nPress Enter to exit...")
    exit()

# Test 3: Initialize pyttsx3
print("\n[TEST 3/5] Initializing text-to-speech engine...")
print("  (This might take a few seconds...)")
try:
    engine = pyttsx3.init()
    print("  ✅ Text-to-speech engine initialized!")
except Exception as e:
    print(f"  ❌ Error initializing text-to-speech: {e}")
    input("\nPress Enter to exit...")
    exit()

# Test 4: Configure pyttsx3
print("\n[TEST 4/5] Configuring text-to-speech...")
try:
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    print("  ✅ Text-to-speech configured!")
except Exception as e:
    print(f"  ❌ Error configuring text-to-speech: {e}")
    input("\nPress Enter to exit...")
    exit()

# Test 5: Make it speak
print("\n[TEST 5/5] Testing speech output...")
print("  You should hear sound now...")
try:
    engine.say("Testing. JARVIS is working.")
    engine.runAndWait()
    print("  ✅ Speech test complete!")
except Exception as e:
    print(f"  ❌ Error during speech: {e}")
    input("\nPress Enter to exit...")
    exit()

# All tests passed
print("\n" + "=" * 60)
print("ALL TESTS PASSED! ✅")
print("=" * 60)
print("\nYour system can run JARVIS!")
print("The problem might be in the main code.")

# Test microphone
print("\n" + "=" * 60)
print("BONUS TEST: Microphone")
print("=" * 60)
print("\nTesting microphone in 3 seconds...")
print("Get ready to say something...")

import time
time.sleep(3)

try:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 Say something NOW (you have 5 seconds)...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        print("🔄 Processing...")
        
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: '{text}'")
        
        engine.say(f"You said {text}")
        engine.runAndWait()
        
except Exception as e:
    print(f"⚠️ Microphone test failed: {e}")
    print("This is OK - the main JARVIS features still work!")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE!")
print("=" * 60)
input("\nPress Enter to exit...")