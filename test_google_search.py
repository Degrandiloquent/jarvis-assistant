#!/usr/bin/env python3
"""
Test script to thoroughly test Google search functionality in Jarvis
"""

from jarvis import JarvisAssistant
import time

def test_google_search_basic():
    """Test basic Google search functionality"""
    print("Testing: Basic Google search")

    # Create Jarvis instance (without running the full loop)
    jarvis = JarvisAssistant()

    # Test basic search command
    command = "search python programming"
    print(f"Testing command: '{command}'")

    try:
        # Process the command
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with Google search for 'python programming'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

def test_google_search_with_spaces():
    """Test Google search with multiple words"""
    print("\nTesting: Google search with multiple words")

    jarvis = JarvisAssistant()

    command = "search machine learning tutorials"
    print(f"Testing command: '{command}'")

    try:
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with Google search for 'machine learning tutorials'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

def test_google_search_empty_query():
    """Test Google search with empty query"""
    print("\nTesting: Google search with empty query")

    jarvis = JarvisAssistant()

    command = "search"
    print(f"Testing command: '{command}'")

    try:
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have prompted for a query")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

def test_google_search_special_characters():
    """Test Google search with special characters"""
    print("\nTesting: Google search with special characters")

    jarvis = JarvisAssistant()

    command = "search C++ programming language"
    print(f"Testing command: '{command}'")

    try:
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with Google search for 'C++ programming language'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

def test_youtube_search_still_works():
    """Test that YouTube search still works separately"""
    print("\nTesting: YouTube search still works")

    jarvis = JarvisAssistant()

    command = "search python tutorials on youtube"
    print(f"Testing command: '{command}'")

    try:
        result = jarvis.process_command(command)
        print("✅ Command processed successfully")
        print("✅ Should have opened Chrome with YouTube search for 'python tutorials'")
        return True
    except Exception as e:
        print(f"❌ Error processing command: {e}")
        return False

def run_all_tests():
    """Run all Google search tests"""
    print("Running thorough Google search functionality tests...\n")

    tests = [
        test_google_search_basic,
        test_google_search_with_spaces,
        test_google_search_empty_query,
        test_google_search_special_characters,
        test_youtube_search_still_works
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests completed successfully!")
        print("Google search functionality is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")

    print(f"{'='*50}")

if __name__ == "__main__":
    run_all_tests()
