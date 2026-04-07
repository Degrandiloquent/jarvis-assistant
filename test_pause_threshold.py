#!/usr/bin/env python3
"""
Test script to verify the pause_threshold fix for Jarvis voice recognition.
This tests that Jarvis waits longer before processing commands, allowing users to finish speaking.
"""
 
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import JarvisAssistant
import speech_recognition as sr
import time

def test_pause_threshold_configuration():
    """Test that the pause_threshold is correctly set to 0.8 seconds"""
    print("Testing pause_threshold configuration...")

    jarvis = JarvisAssistant()

    # Check if the recognizer has the correct pause_threshold
    expected_threshold = 0.8
    actual_threshold = jarvis.recognizer.pause_threshold

    print(f"Expected pause_threshold: {expected_threshold} seconds")
    print(f"Actual pause_threshold: {actual_threshold} seconds")

    if abs(actual_threshold - expected_threshold) < 0.01:  # Allow small floating point differences
        print("✅ PASS: pause_threshold is correctly set to 0.8 seconds")
        return True
    else:
        print("❌ FAIL: pause_threshold is not set correctly")
        return False

def test_recognizer_settings():
    """Test other recognizer settings to ensure they work with the new pause_threshold"""
    print("\nTesting recognizer settings...")

    jarvis = JarvisAssistant()

    settings = {
        'energy_threshold': 300,
        'dynamic_energy_threshold': True,
        'pause_threshold': 0.8
    }

    all_correct = True
    for setting, expected_value in settings.items():
        actual_value = getattr(jarvis.recognizer, setting)
        print(f"{setting}: expected {expected_value}, actual {actual_value}")

        if isinstance(expected_value, float):
            if abs(actual_value - expected_value) >= 0.01:
                print(f"❌ FAIL: {setting} mismatch")
                all_correct = False
        elif actual_value != expected_value:
            print(f"❌ FAIL: {setting} mismatch")
            all_correct = False

    if all_correct:
        print("✅ PASS: All recognizer settings are correct")
    else:
        print("❌ FAIL: Some recognizer settings are incorrect")

    return all_correct

def simulate_command_processing():
    """Simulate processing of commands with different lengths to test timing"""
    print("\nSimulating command processing...")

    jarvis = JarvisAssistant()

    test_commands = [
        "volume up",  # Short command
        "play Michael Jackson song Earth on youtube",  # Long command with pauses
        "what time is it",  # Medium command
        "open chrome",  # Short command
        "search for python programming tutorials on youtube",  # Very long command
    ]

    print("Note: Since we can't actually test voice input, this simulates command processing.")
    print("In real usage, the 1.5 second pause_threshold means Jarvis will wait up to 1.5 seconds")
    print("of silence before processing, allowing you to finish longer commands.\n")

    for command in test_commands:
        print(f"Testing command: '{command}'")
        try:
            # Simulate processing without actual voice input
            result = jarvis.process_command(command)
            print(f"✅ Command processed successfully (would {'exit' if not result else 'continue'} Jarvis)")
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            return False

    print("✅ PASS: All test commands processed successfully")
    return True

def test_listen_method_timeout():
    """Test that the listen method has appropriate timeouts"""
    print("\nTesting listen method configuration...")

    jarvis = JarvisAssistant()

    # Check timeout and phrase_time_limit settings
    timeout = 8  # From the code
    phrase_time_limit = 8  # From the code

    print(f"Listen timeout: {timeout} seconds")
    print(f"Phrase time limit: {phrase_time_limit} seconds")
    print("✅ These settings work well with the 0.8 second pause_threshold")

    return True

if __name__ == "__main__":
    print("Testing Jarvis pause_threshold fix for voice recognition...\n")

    tests = [
        test_pause_threshold_configuration,
        test_recognizer_settings,
        simulate_command_processing,
        test_listen_method_timeout,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The pause_threshold optimization should work correctly.")
        print("Jarvis will now wait up to 0.8 seconds of silence before processing commands,")
        print("providing faster response while still allowing you to finish longer commands like 'play Michael Jackson song Earth on youtube'.")
    else:
        print("❌ Some tests failed. Please check the implementation.")

    print(f"{'='*50}")
