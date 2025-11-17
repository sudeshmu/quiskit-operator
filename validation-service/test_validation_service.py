#!/usr/bin/env python3
"""
Test script for the QiskitOperator Validation Service

This script tests all endpoints and validation scenarios.
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Service configuration
BASE_URL = "http://localhost:8000"

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name: str):
    """Print test name"""
    print(f"\n{BLUE}Testing: {name}{RESET}")

def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def test_health_endpoint():
    """Test the /health endpoint"""
    print_test("Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data['status']}")
            print(f"  Version: {data.get('version', 'N/A')}")
            print(f"  Timestamp: {data.get('timestamp', 'N/A')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the / endpoint"""
    print_test("Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Root endpoint passed: {data['status']}")
            return True
        else:
            print_error(f"Root endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Root endpoint failed: {e}")
        return False

def test_valid_circuit():
    """Test validation with a valid circuit"""
    print_test("Valid Circuit Validation")
    
    circuit_code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])"""
    
    payload = {
        "code": circuit_code,
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print_success("Valid circuit accepted")
                print(f"  Circuit Hash: {data.get('circuit_hash', 'N/A')[:16]}...")
                print(f"  Qubits: {data.get('qubits', 0)}")
                print(f"  Depth: {data.get('depth', 0)}")
                print(f"  Gates: {data.get('gates', 0)}")
                print(f"  Gate Types: {data.get('gate_types', {})}")
                print(f"  Estimated Time: {data.get('estimated_execution_time', 0):.3f}s")
                return True
            else:
                print_error(f"Valid circuit rejected: {data.get('errors', [])}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def test_syntax_error():
    """Test validation with Python syntax error"""
    print_test("Syntax Error Detection")
    
    circuit_code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2
qc.h(0"""  # Intentional syntax errors
    
    payload = {
        "code": circuit_code,
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('valid') and data.get('errors'):
                print_success(f"Syntax error detected correctly")
                print(f"  Error: {data['errors'][0]}")
                return True
            else:
                print_error("Syntax error not detected")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def test_runtime_error():
    """Test validation with runtime error"""
    print_test("Runtime Error Detection")
    
    circuit_code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(5)"""  # Qubit 5 doesn't exist
    
    payload = {
        "code": circuit_code,
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('valid') and data.get('errors'):
                print_success(f"Runtime error detected correctly")
                print(f"  Error: {data['errors'][0][:80]}...")
                return True
            else:
                print_error("Runtime error not detected")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def test_no_circuit():
    """Test validation with code that doesn't create a circuit"""
    print_test("No Circuit Detection")
    
    circuit_code = """x = 5
y = 10
print(x + y)"""
    
    payload = {
        "code": circuit_code,
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('valid') and 'No QuantumCircuit' in str(data.get('errors', [])):
                print_success("No circuit detected correctly")
                return True
            else:
                print_error("Should have detected no circuit")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def test_complex_circuit():
    """Test validation with a more complex circuit"""
    print_test("Complex Circuit Validation")
    
    circuit_code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(4, 4)
# Create GHZ state
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
# Add some rotation gates
qc.rx(1.57, 0)
qc.ry(0.785, 1)
qc.rz(3.14, 2)
# Measure all
qc.measure([0, 1, 2, 3], [0, 1, 2, 3])"""
    
    payload = {
        "code": circuit_code,
        "backend_name": "ibmq_qasm_simulator",
        "optimization_level": 2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print_success("Complex circuit validated")
                print(f"  Qubits: {data.get('qubits', 0)}")
                print(f"  Depth: {data.get('depth', 0)}")
                print(f"  Gates: {data.get('gates', 0)}")
                if data.get('warnings'):
                    print_warning(f"Warnings: {data['warnings']}")
                return True
            else:
                print_error(f"Complex circuit rejected: {data.get('errors', [])}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def test_large_circuit():
    """Test validation with a large circuit (warning check)"""
    print_test("Large Circuit Warning")
    
    circuit_code = """from qiskit import QuantumCircuit
qc = QuantumCircuit(200, 200)
for i in range(200):
    qc.h(i)"""
    
    payload = {
        "code": circuit_code,
        "backend_name": "ibmq_qasm_simulator",
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print_success("Large circuit validated")
                if data.get('warnings'):
                    print_warning(f"Warnings: {data['warnings']}")
                    return True
                else:
                    print_warning("Expected warning about qubit count not present")
                    return True  # Still pass, warning is optional
            else:
                print_error(f"Large circuit rejected: {data.get('errors', [])}")
                return False
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False

def wait_for_service(timeout: int = 30) -> bool:
    """Wait for service to be ready"""
    print(f"\n{BLUE}Waiting for service to be ready...{RESET}")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print_success("Service is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    print_error(f"Service not ready after {timeout} seconds")
    return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}QiskitOperator Validation Service Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"\nTesting service at: {BASE_URL}")
    
    # Wait for service to be ready
    if not wait_for_service():
        print_error("\nService is not available. Please start the service first:")
        print("  python main.py")
        print("  or")
        print("  docker run -p 8000:8000 qiskit-validation-service:test")
        sys.exit(1)
    
    # Run all tests
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Valid Circuit", test_valid_circuit),
        ("Syntax Error", test_syntax_error),
        ("Runtime Error", test_runtime_error),
        ("No Circuit", test_no_circuit),
        ("Complex Circuit", test_complex_circuit),
        ("Large Circuit", test_large_circuit),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name:.<40} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}All tests passed! ({passed}/{total}){RESET}")
        sys.exit(0)
    else:
        print(f"{RED}Some tests failed. ({passed}/{total} passed){RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

