#!/usr/bin/env python3
"""
Simple example to test the validation service
Demonstrates that the syntax error is fixed and the service works correctly.
"""

import requests
import json
import time

# ANSI colors
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

def wait_for_service():
    """Wait for service to be ready"""
    print(f"{CYAN}Checking if service is ready...{RESET}")
    for i in range(5):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print(f"{GREEN}✓ Service is ready!{RESET}\n")
                return True
        except:
            time.sleep(1)
    return False

def test_example(name, circuit_code):
    """Test a circuit example"""
    print_header(f"Example: {name}")
    
    print(f"{CYAN}Circuit Code:{RESET}")
    print(circuit_code)
    print()
    
    payload = {
        "code": circuit_code,
        "optimization_level": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=10)
        data = response.json()
        
        if data.get('valid'):
            print(f"{GREEN}✅ VALIDATION SUCCESSFUL{RESET}\n")
            print(f"{CYAN}Circuit Details:{RESET}")
            print(f"  • Circuit Hash:     {data['circuit_hash'][:32]}...")
            print(f"  • Qubits:           {data['qubits']}")
            print(f"  • Circuit Depth:    {data['depth']}")
            print(f"  • Total Gates:      {data['gates']}")
            print(f"  • Execution Time:   ~{data['estimated_execution_time']:.3f}s")
            
            if data.get('gate_types'):
                print(f"\n{CYAN}Gate Breakdown:{RESET}")
                for gate, count in data['gate_types'].items():
                    print(f"    {gate:10s} → {count}")
            
            if data.get('warnings'):
                print(f"\n{YELLOW}⚠ Warnings:{RESET}")
                for warning in data['warnings']:
                    print(f"    {warning}")
            
            return True
        else:
            print(f"{RED}❌ VALIDATION FAILED{RESET}\n")
            print(f"{RED}Errors:{RESET}")
            for error in data.get('errors', []):
                print(f"  • {error}")
            return False
            
    except Exception as e:
        print(f"{RED}❌ Request failed: {e}{RESET}")
        return False

def main():
    print_header("Validation Service - Simple Example Test")
    
    if not wait_for_service():
        print(f"{RED}Service not available. Please start it first.{RESET}")
        return
    
    # Example 1: Bell State (Quantum Entanglement)
    bell_state = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])"""
    
    # Example 2: Quantum Teleportation Protocol (3 qubits)
    teleportation = """from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 3)
# Create entangled pair
qc.h(1)
qc.cx(1, 2)
# Alice's operations
qc.cx(0, 1)
qc.h(0)
# Measurements
qc.measure([0, 1], [0, 1])
# Bob's corrections
qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)"""
    
    # Example 3: Quantum Fourier Transform (3 qubits)
    qft = """from qiskit import QuantumCircuit
import math
qc = QuantumCircuit(3)
# QFT on 3 qubits
qc.h(2)
qc.cp(math.pi/2, 1, 2)
qc.cp(math.pi/4, 0, 2)
qc.h(1)
qc.cp(math.pi/2, 0, 1)
qc.h(0)
# Swap qubits
qc.swap(0, 2)"""
    
    # Example 4: Deutsch-Jozsa Algorithm (2 qubits)
    deutsch = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 1)
# Initialize
qc.x(1)
qc.h([0, 1])
# Oracle (balanced function)
qc.cx(0, 1)
# Apply Hadamard
qc.h(0)
# Measure
qc.measure(0, 0)"""
    
    examples = [
        ("Bell State - Quantum Entanglement", bell_state),
        ("Quantum Teleportation Protocol", teleportation),
        ("Quantum Fourier Transform", qft),
        ("Deutsch-Jozsa Algorithm", deutsch),
    ]
    
    results = []
    for name, code in examples:
        result = test_example(name, code)
        results.append((name, result))
        time.sleep(0.5)
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"  {name:.<50} {status}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    if passed == total:
        print(f"{GREEN}✅ All {total} examples validated successfully!{RESET}")
        print(f"\n{CYAN}The syntax error is fixed and the service is working perfectly!{RESET}")
    else:
        print(f"{YELLOW}⚠ {passed}/{total} examples passed{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

if __name__ == "__main__":
    main()

