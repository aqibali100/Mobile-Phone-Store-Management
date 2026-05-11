#!/usr/bin/env python3
"""Test script to verify all modules can be imported."""

import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported."""
    print("🧪 Testing Mobile Phone Store System...")
    print("=" * 50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test modules
    modules_to_test = [
        "utils.constants",
        "utils.validators",
        "backend.auth",
        "backend.phone_manager",
        "backend.file_handler",
        "frontend.components.buttons",
        "frontend.components.tables",
        "frontend.components.message_boxes",
        "frontend.login_window",
        "frontend.dashboard",
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
            tests_passed += 1
        except ImportError as e:
            print(f"❌ {module}: {e}")
            tests_failed += 1
    
    print("=" * 50)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 All tests passed! System is ready to run.")
        print("Run: python main.py")
        return True
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
