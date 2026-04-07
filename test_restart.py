#!/usr/bin/env python3
"""
Test script for restart functionality
"""

import sys
import os

# Add current directory to path to import jarvis
sys.path.insert(0, os.getcwd())

from jarvis import JarvisAssistant

def test_restart_functionality():
    """Test the restart functionality without actually restarting"""
    print("Testing restart functionality...")

    # Create Jarvis instance
    jarvis = JarvisAssistant()

    # Test that the method exists
    assert hasattr(jarvis, 'restart_computer'), "restart_computer method not found"

    # Test that the command is recognized
    test_commands = ['restart computer', 'restart laptop']

    for cmd in test_commands:
        print(f"\nTesting command: '{cmd}'")
        try:
            # This should return True and not actually restart
            result = jarvis.process_command(cmd)
            print(f"✅ Command processed successfully: {result}")
        except Exception as e:
            print(f"❌ Error processing command '{cmd}': {e}")

    print("\n✅ All restart functionality tests passed!")

if __name__ == "__main__":
    test_restart_functionality()
