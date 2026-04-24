"""
Day 4 Test Runner

Simple script to run Day 4 indicator tests.
"""

import subprocess
import sys

def main():
    """Run the Day 4 test script"""
    print("Running Day 4 Indicator Tests...")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, "test_day4_indicators.py"],
            check=False
        )
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
