#!/usr/bin/env python3
"""
Day 5 Test Runner

Runs all Day 5 component tests and displays results.
"""

import subprocess
import sys


def run_tests():
    """Run Day 5 component tests"""
    print("="*70)
    print("RUNNING DAY 5 COMPONENT TESTS")
    print("="*70)
    print("\nTesting:")
    print("  - Sector Analyzer")
    print("  - Stock Screener")
    print("  - Beta Calculator")
    print("\n" + "="*70 + "\n")
    
    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, "test_day5_components.py"],
            capture_output=False,
            text=True
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_tests()
    
    if success:
        print("\n" + "="*70)
        print("✅ ALL DAY 5 TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ SOME TESTS FAILED")
        print("="*70)
        sys.exit(1)
