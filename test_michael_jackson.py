#!/usr/bin/env python3
"""
Test script to test searching for Michael Jackson on Google
"""

from jarvis import JarvisAssistant

def test_michael_jackson_search():
    """Test searching for Michael Jackson on Google"""
    print("Testing: Search for Michael Jackson on Google")

    # Create Jarvis instance (without running the full loop)
    jarvis = JarvisAssistant()

    # Test the command directly
    command = "search michael Jackson on google"
    print(f"Testing command: '{command}'")

    try:
        # Process the command
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with Google search for 'michael Jackson'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

if __name__ == "__main__":
    print("Testing Google search for Michael Jackson...\n")

    success = test_michael_jackson_search()

    if success:
        print("\n🎉 Test completed successfully!")
        print("Chrome should have opened with Google search results for 'michael Jackson'")
    else:
        print("\n❌ Test failed.")

    print("\nTest complete.")
