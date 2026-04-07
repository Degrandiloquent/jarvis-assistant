#!/usr/bin/env python3
"""
Test script to specifically test searching for Ishowspeed on YouTube
"""

from jarvis import JarvisAssistant

def test_ishowspeed_search():
    """Test searching for Ishowspeed on YouTube"""
    print("Testing: Search for Ishowspeed on YouTube")

    # Create Jarvis instance (without running the full loop)
    jarvis = JarvisAssistant()

    # Test the command directly
    command = "search Ishowspeed on youtube"
    print(f"Testing command: '{command}'")

    try:
        # Process the command
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with YouTube search for 'Ishowspeed'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

if __name__ == "__main__":
    print("Testing YouTube search for Ishowspeed...\n")

    success = test_ishowspeed_search()

    if success:
        print("\n🎉 Test completed successfully!")
        print("Chrome should have opened with YouTube search results for 'Ishowspeed'")
    else:
        print("\n❌ Test failed.")

    print("\nTest complete.")
