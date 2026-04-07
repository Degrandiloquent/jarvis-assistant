#!/usr/bin/env python3
"""
Manual test for volume functionality - tests volume methods directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import JarvisAssistant

def test_volume_methods():
    """Test volume methods directly"""
    print("Creating Jarvis instance...")
    jarvis = JarvisAssistant()

    print(f"Volume control available: {jarvis.volume is not None}")

    print("\nTesting volume_up...")
    jarvis.volume_up()

    print("Testing volume_down...")
    jarvis.volume_down()

    print("Testing mute...")
    jarvis.mute()

    print("Testing unmute...")
    jarvis.unmute()

    print("Testing set_volume to 50...")
    jarvis.set_volume(50)

    print("\nVolume testing complete!")

if __name__ == "__main__":
    test_volume_methods()
