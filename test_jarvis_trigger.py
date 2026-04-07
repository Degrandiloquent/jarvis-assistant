import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import JarvisAssistant

class TestJarvisAssistant(JarvisAssistant):
    def __init__(self):
        # Skip the full initialization for testing
        self.engine = None
        self.recognizer = None
        self.volume = None
        self.model = None
        self.tokenizer = None
        self.speak_log = []

    def speak(self, text):
        """Override speak to log what would be said instead of speaking"""
        self.speak_log.append(text)
        print(f"Would speak: {text}")

def test_jarvis_trigger():
    jarvis = TestJarvisAssistant()

    test_cases = [
        ("jarvis", ["sir"]),  # Should say "sir" and continue
        ("hey jarvis", ["sir"]),  # Should say "sir" and continue
        ("hey jarvis open chrome", ["sir"]),  # Should say "sir" then process "open chrome"
        ("jarvis volume up", ["sir"]),  # Should say "sir" then process "volume up"
        ("open chrome", []),  # No trigger, should not say "sir"
        ("Hey Jarvis", ["sir"]),  # Case insensitive
        ("JARVIS", ["sir"]),  # Case insensitive
        ("hey jarvis", ["sir"]),  # Exact match
    ]

    for command, expected_speaks in test_cases:
        jarvis.speak_log = []  # Reset log
        print(f"\nTesting command: '{command}'")
        try:
            result = jarvis.process_command(command)
            print(f"Speak log: {jarvis.speak_log}")
            print(f"Expected speaks: {expected_speaks}")
            if jarvis.speak_log == expected_speaks:
                print("✅ PASS")
            else:
                print("❌ FAIL")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_jarvis_trigger()
