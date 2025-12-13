#!/usr/bin/env python3
"""
Test Runner Script
Runs all unit tests and displays results with coverage information
"""

import unittest
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_tests(verbosity=2):
    """
    Discover and run all tests in the tests directory.
    
    Args:
        verbosity: Test output verbosity (0, 1, or 2)
    
    Returns:
        TestResult object
    """
    # Get the tests directory
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    # Count tests
    test_count = suite.countTestCases()
    
    print("=" * 70)
    print("MANCALA GAME - UNIT TEST SUITE")
    print("=" * 70)
    print(f"\nDiscovered {test_count} tests")
    print(f"Test directory: {tests_dir}")
    print("-" * 70)
    
    # Run tests
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print("-" * 70)
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    
    print("=" * 70)
    
    return result


def run_specific_test(test_name):
    """
    Run a specific test class or method.
    
    Args:
        test_name: Name of test class or method (e.g., 'test_game_logic.TestGameInitialization')
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


def list_tests():
    """List all available tests."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    print("=" * 70)
    print("AVAILABLE TESTS")
    print("=" * 70)
    
    def list_suite(s, indent=0):
        for test in s:
            if hasattr(test, '__iter__'):
                list_suite(test, indent)
            else:
                print("  " * indent + str(test))
    
    list_suite(suite)
    print("=" * 70)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            list_tests()
        elif sys.argv[1] == '--quick':
            # Quick test run with less verbosity
            result = run_tests(verbosity=1)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            # Run specific test
            result = run_specific_test(sys.argv[1])
            sys.exit(0 if result.wasSuccessful() else 1)
    else:
        result = run_tests(verbosity=2)
        sys.exit(0 if result.wasSuccessful() else 1)
