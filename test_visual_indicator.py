#!/usr/bin/env python3
"""
Test script for the visual indicator functionality in Jarvis.
This script tests if the visual indicator appears and disappears correctly when speaking.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis import JarvisAssistant
import time

def test_visual_indicator():
    """Test the visual indicator by speaking a short message"""
    print("Testing visual indicator...")

    # Create Jarvis instance (without full initialization to avoid TTS setup)
    jarvis = JarvisAssistant.__new__(JarvisAssistant)  # Create without __init__
    jarvis.visual_indicator = None  # Initialize manually

    # Test show and hide
    print("Showing visual indicator...")
    jarvis.show_visual_indicator()
    time.sleep(2)  # Wait 2 seconds

    print("Hiding visual indicator...")
    jarvis.hide_visual_indicator()

    print("Visual indicator test completed.")

if __name__ == "__main__":
    test_visual_indicator()
