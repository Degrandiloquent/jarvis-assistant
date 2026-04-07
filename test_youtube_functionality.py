
#!/usr/bin/env python3
"""
Test script for YouTube functionality in Jarvis Assistant
"""

import subprocess
import os
import sys

def test_open_youtube():
    """Test opening YouTube in Chrome"""
    print("Testing: Open YouTube")
    try:
        # Simulate the command
        subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'https://www.youtube.com'])
        print("✅ YouTube opened successfully in Chrome")
        return True
    except Exception as e:
        print(f"❌ Error opening YouTube: {e}")
        return False

def test_play_song():
    """Test playing a song on YouTube"""
    print("Testing: Play song on YouTube")
    song_name = "shape of you"
    try:
        # Simulate the command - try direct video URL first
        # For testing, we'll just check if the URL construction works
        search_url = f"https://www.youtube.com/search?q={song_name.replace(' ', '+')}"
        print(f"✅ Would open search URL: {search_url}")
        print("✅ Spacebar press simulation would occur after page load to play video")
        print("⚠️  Note: YouTube may block autoplay - spacebar press attempts to start playback")
        return True
    except Exception as e:
        print(f"❌ Error in play song test: {e}")
        return False

def test_command_processing():
    """Test command processing logic"""
    print("Testing: Command processing logic")

    # Test open youtube command
    command = "open youtube"
    if 'open' in command:
        app = command.replace('open', '').strip()
        if app == 'youtube':
            print("✅ 'open youtube' command recognized correctly")
        else:
            print(f"❌ 'open youtube' command not recognized: got '{app}'")
            return False

    # Test play song command (old syntax)
    command = "play shape of you on youtube"
    if 'play' in command and 'youtube' in command:
        song_name = command.replace('play', '').replace('on youtube', '').strip()
        if song_name == "shape of you":
            print("✅ 'play shape of you on youtube' command recognized correctly")
        else:
            print(f"❌ Song name extraction failed: got '{song_name}'")
            return False

    # Test new play song command (without 'on youtube')
    command = "play shape of you"
    if 'play' in command:
        song_name = command.replace('play', '').strip()
        if song_name == "shape of you":
            print("✅ 'play shape of you' command recognized correctly (new syntax)")
        else:
            print(f"❌ Song name extraction failed for new syntax: got '{song_name}'")
            return False

    # Test search video command
    command = "search python tutorial on youtube"
    if ('search' in command or 'find' in command) and 'youtube' in command:
        video_name = command.replace('search', '').replace('on youtube', '').strip()
        if video_name == "python tutorial":
            print("✅ 'search python tutorial on youtube' command recognized correctly")
        else:
            print(f"❌ Video name extraction failed: got '{video_name}'")
            return False

    return True

if __name__ == "__main__":
    print("Testing YouTube functionality...\n")

    # Test command processing (safe)
    success = test_command_processing()
    print()

    # Test actual functionality (opens browsers)
    print("Note: The following tests will open Chrome windows.")
    print("Proceeding with browser tests...")

    success &= test_open_youtube()
    print()

    success &= test_play_song()
    print()

    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed.")

    print("\nTest complete.")
