#!/usr/bin/env python3
"""
Thorough test script for volume functionality in JarvisAssistant.
Tests initialization, volume up/down, mute/unmute, set volume, and edge cases.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import JarvisAssistant

def test_volume_initialization():
    """Test if volume control initializes correctly."""
    print("Testing volume initialization...")
    jarvis = JarvisAssistant()
    if jarvis.volume is not None:
        print("✅ Volume control initialized successfully")
        return True
    else:
        print("❌ Volume control failed to initialize")
        return False

def test_volume_methods():
    """Test volume control methods."""
    print("\nTesting volume methods...")
    jarvis = JarvisAssistant()

    if jarvis.volume is None:
        print("Testing fallback volume control (pyautogui)...")
        # Test volume up fallback
        print("Testing volume_up fallback...")
        try:
            jarvis.volume_up()
            print("✅ Volume up fallback works")
        except Exception as e:
            print(f"❌ Volume up fallback failed: {e}")

        # Test volume down fallback (but it doesn't have fallback yet)
        print("Testing volume_down fallback...")
        try:
            jarvis.volume_down()
            print("❌ Volume down fallback not implemented")
        except Exception as e:
            print(f"❌ Volume down fallback failed: {e}")

        # Test mute fallback (not implemented)
        print("Testing mute fallback...")
        try:
            jarvis.mute()
            print("❌ Mute fallback not implemented")
        except Exception as e:
            print(f"❌ Mute fallback failed: {e}")

        # Test unmute fallback (not implemented)
        print("Testing unmute fallback...")
        try:
            jarvis.unmute()
            print("❌ Unmute fallback not implemented")
        except Exception as e:
            print(f"❌ Unmute fallback failed: {e}")

        # Test set volume fallback (not implemented)
        print("Testing set_volume fallback...")
        try:
            jarvis.set_volume(50)
            print("❌ Set volume fallback not implemented")
        except Exception as e:
            print(f"❌ Set volume fallback failed: {e}")

        return

    # Test volume up
    print("Testing volume_up...")
    initial_volume = jarvis.volume.GetMasterVolumeLevelScalar()
    jarvis.volume_up()
    new_volume = jarvis.volume.GetMasterVolumeLevelScalar()
    if new_volume > initial_volume:
        print("✅ Volume up works")
    else:
        print("❌ Volume up failed")

    # Test volume down
    print("Testing volume_down...")
    initial_volume = jarvis.volume.GetMasterVolumeLevelScalar()
    jarvis.volume_down()
    new_volume = jarvis.volume.GetMasterVolumeLevelScalar()
    if new_volume < initial_volume:
        print("✅ Volume down works")
    else:
        print("❌ Volume down failed")

    # Test mute
    print("Testing mute...")
    jarvis.mute()
    if jarvis.volume.GetMute():
        print("✅ Mute works")
    else:
        print("❌ Mute failed")

    # Test unmute
    print("Testing unmute...")
    jarvis.unmute()
    if not jarvis.volume.GetMute():
        print("✅ Unmute works")
    else:
        print("❌ Unmute failed")

    # Test set volume to 50
    print("Testing set_volume to 50...")
    jarvis.set_volume(50)
    current_volume = jarvis.volume.GetMasterVolumeLevelScalar()
    if abs(current_volume - 0.5) < 0.01:  # Allow small floating point difference
        print("✅ Set volume to 50 works")
    else:
        print(f"❌ Set volume to 50 failed - got {current_volume}")

    # Edge cases
    print("Testing edge cases...")

    # Set to 0
    jarvis.set_volume(0)
    if jarvis.volume.GetMasterVolumeLevelScalar() == 0.0:
        print("✅ Set volume to 0 works")
    else:
        print("❌ Set volume to 0 failed")

    # Set to 100
    jarvis.set_volume(100)
    if jarvis.volume.GetMasterVolumeLevelScalar() == 1.0:
        print("✅ Set volume to 100 works")
    else:
        print("❌ Set volume to 100 failed")

    # Set to negative (should clamp to 0)
    jarvis.set_volume(-10)
    if jarvis.volume.GetMasterVolumeLevelScalar() == 0.0:
        print("✅ Set volume to negative clamps to 0")
    else:
        print("❌ Set volume to negative failed")

    # Set to over 100 (should clamp to 100)
    jarvis.set_volume(150)
    if jarvis.volume.GetMasterVolumeLevelScalar() == 1.0:
        print("✅ Set volume to over 100 clamps to 100")
    else:
        print("❌ Set volume to over 100 failed")

if __name__ == "__main__":
    print("Starting thorough volume functionality tests...\n")

    success = test_volume_initialization()
    if success:
        test_volume_methods()

    print("\nVolume functionality testing complete.")
