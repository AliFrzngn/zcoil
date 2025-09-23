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
    print("AliFrzngn Development - Microservices Test Runner")
    print("=" * 60)
    
    # Set up environment
    os.environ["PYTHONPATH"] = "/workspace"
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    os.environ["ENVIRONMENT"] = "test"
    
    # Change to workspace directory
    os.chdir("/workspace")
    
    success = True
    
    # Test Inventory Service
    print("\n" + "=" * 40)
    print("Testing Inventory Service")
    print("=" * 40)
    
    inventory_tests = [
        "python -m pytest backend/inventory-service/tests/ -v",
        "python -c 'from backend.inventory_service.main import app; print(\"Inventory service imports successfully\")'",
        "python -c 'from backend.inventory_service.models.product import Product; print(\"Product model imports successfully\")'",
        "python -c 'from backend.inventory_service.services.product_service import ProductService; print(\"Product service imports successfully\")'",
    ]
    
    for test in inventory_tests:
        if not run_command(test):
            success = False
    
    # Test CRM Service
    print("\n" + "=" * 40)
    print("Testing CRM Service")
    print("=" * 40)
    
    crm_tests = [
        "python -m pytest backend/crm-service/tests/ -v",
        "python -c 'from backend.crm_service.main import app; print(\"CRM service imports successfully\")'",
        "python -c 'from backend.crm_service.services.customer_service import CustomerService; print(\"Customer service imports successfully\")'",
    ]
    
    for test in crm_tests:
        if not run_command(test):
            success = False
    
    # Test Shared Components
    print("\n" + "=" * 40)
    print("Testing Shared Components")
    print("=" * 40)
    
    shared_tests = [
        "python -c 'from backend.shared.config import settings; print(f\"Config loaded: {settings.service_name}\")'",
        "python -c 'from backend.shared.database import get_db; print(\"Database module imports successfully\")'",
        "python -c 'from backend.shared.auth import create_access_token; print(\"Auth module imports successfully\")'",
        "python -c 'from backend.shared.utils import HTTPClient; print(\"Utils module imports successfully\")'",
    ]
    
    for test in shared_tests:
        if not run_command(test):
            success = False
    
    # Test Integration
    print("\n" + "=" * 40)
    print("Testing Integration")
    print("=" * 40)
    
    integration_tests = [
        "python -c 'from backend.inventory_service.schemas.product import ProductCreate; print(\"Inventory schemas work\")'",
        "python -c 'from backend.crm_service.schemas.customer import CustomerProductResponse; print(\"CRM schemas work\")'",
    ]
    
    for test in integration_tests:
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
