#!/usr/bin/env python3
"""
Day 3 Test Runner

Simple script to run Day 3 tests.
"""

import subprocess
import sys

def main():
    """Run Day 3 tests"""
    print("="*60)
    print("Running Day 3 Tests")
    print("="*60)
    
    try:
        # Run the test script
        result = subprocess.run(
            [sys.executable, "test_day3_services.py"],
            check=False
        )
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
