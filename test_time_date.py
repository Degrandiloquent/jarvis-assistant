import datetime
from jarvis import JarvisAssistant

# Create a test instance
jarvis = JarvisAssistant()

# Override speak to print instead of TTS for testing
def test_speak(text):
    print(f"JARVIS: {text}")

jarvis.speak = test_speak

# Test the time and date functionality
print("Testing time and date query...")
jarvis.process_command("what time is it")

print("\nTesting with different phrases...")
jarvis.process_command("current time")
jarvis.process_command("what is the time")
jarvis.process_command("tell me the time")

print("\nTesting date queries...")
jarvis.process_command("what is the date")
jarvis.process_command("current date")
jarvis.process_command("what date is it")
jarvis.process_command("tell me the date")

print("\nTest complete!")
