#!/usr/bin/env python3
"""Test runner for the microservices."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {command}")
    if cwd:
        print(f"Working directory: {cwd}")
    
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    
    print("Command succeeded")
    if result.stdout:
        print(f"STDOUT: {result.stdout}")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("ZCoil Microservices - Comprehensive Test Runner")
    print("=" * 60)
    
    # Set up environment
    os.environ["PYTHONPATH"] = os.getcwd()
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["ENVIRONMENT"] = "test"
    
    success = True
    
    # Test Inventory Service
    print("\n" + "=" * 40)
    print("Testing Inventory Service")
    print("=" * 40)
    
    inventory_tests = [
        "python -m pytest backend/inventory-service/tests/ -v --tb=short",
    ]
    
    for test in inventory_tests:
        if not run_command(test):
            success = False
    
    # Test CRM Service
    print("\n" + "=" * 40)
    print("Testing CRM Service")
    print("=" * 40)
    
    crm_tests = [
        "python -m pytest backend/crm-service/tests/ -v --tb=short",
    ]
    
    for test in crm_tests:
        if not run_command(test):
            success = False
    
    # Test User Service
    print("\n" + "=" * 40)
    print("Testing User Service")
    print("=" * 40)
    
    user_tests = [
        "python -m pytest backend/user-service/tests/ -v --tb=short",
    ]
    
    for test in user_tests:
        if not run_command(test):
            success = False
    
    # Test Notification Service
    print("\n" + "=" * 40)
    print("Testing Notification Service")
    print("=" * 40)
    
    notification_tests = [
        "python -m pytest backend/notification-service/tests/ -v --tb=short",
    ]
    
    for test in notification_tests:
        if not run_command(test):
            success = False
    
    # Test All Services Together
    print("\n" + "=" * 40)
    print("Running All Tests Together")
    print("=" * 40)
    
    all_tests = [
        "python -m pytest backend/ -v --tb=short --cov=backend --cov-report=term-missing",
    ]
    
    for test in all_tests:
        if not run_command(test):
            success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("The microservices implementation is complete and functional.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the output above for details.")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())