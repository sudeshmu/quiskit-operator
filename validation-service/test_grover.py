#!/usr/bin/env python3
"""
Test Grover's Search Algorithm with the Validation Service

This script creates a Grover's algorithm circuit and validates it.
Grover's algorithm searches for a marked item in an unsorted database
with quadratic speedup compared to classical algorithms.
"""

import requests
import json
import time
import sys

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

BASE_URL = "http://localhost:8000"

# Grover's Algorithm for 2-qubit search
# This searches for the state |11> in a 2-qubit system
GROVER_2_QUBIT = """from qiskit import QuantumCircuit
import math

# Create a 2-qubit circuit for Grover's algorithm
qc = QuantumCircuit(2, 2)

# Initialize: Apply Hadamard to all qubits
qc.h([0, 1])

# Oracle: Mark the state |11>
qc.cz(0, 1)

# Diffusion operator (inversion about average)
qc.h([0, 1])
qc.z([0, 1])
qc.cz(0, 1)
qc.h([0, 1])

# Measure
qc.measure([0, 1], [0, 1])
"""

# Grover's Algorithm for 3-qubit search
# This searches for a specific state in a 3-qubit system
GROVER_3_QUBIT = """from qiskit import QuantumCircuit

# Create a 3-qubit circuit for Grover's algorithm
qc = QuantumCircuit(3, 3)

# Initialize: Apply Hadamard to all qubits
qc.h([0, 1, 2])

# Grover iteration (simplified oracle for |101>)
# Oracle: Mark the state |101>
qc.x(1)  # Flip qubit 1
qc.h(2)
qc.ccx(0, 1, 2)  # Toffoli gate
qc.h(2)
qc.x(1)  # Flip back

# Diffusion operator
qc.h([0, 1, 2])
qc.x([0, 1, 2])
qc.h(2)
qc.ccx(0, 1, 2)
qc.h(2)
qc.x([0, 1, 2])
qc.h([0, 1, 2])

# Measure all qubits
qc.measure([0, 1, 2], [0, 1, 2])
"""

# Complete Grover's Algorithm for 4-qubit search with multiple iterations
GROVER_4_QUBIT = """from qiskit import QuantumCircuit

# Create a 4-qubit circuit (3 search qubits + 1 ancilla)
qc = QuantumCircuit(4, 3)

# Initialize search qubits in superposition
qc.h([0, 1, 2])

# Prepare ancilla in |-> state for phase kickback
qc.x(3)
qc.h(3)

# Grover iterations (optimal number for 3 qubits searching 1 item is ~2 iterations)
num_iterations = 2

for _ in range(num_iterations):
    # Oracle: Mark the state |101> (search target)
    qc.x(1)  # Flip middle qubit
    qc.h(3)
    qc.ccx(0, 1, 3)  # Multi-controlled
    qc.ccx(2, 3, 1)  # operations
    qc.h(3)
    qc.x(1)  # Flip back
    
    # Diffusion operator (inversion about average)
    qc.h([0, 1, 2])
    qc.x([0, 1, 2])
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x([0, 1, 2])
    qc.h([0, 1, 2])

# Measure search qubits
qc.measure([0, 1, 2], [0, 1, 2])
"""

def wait_for_service(max_wait=10):
    """Wait for the service to be ready"""
    print(f"{CYAN}Waiting for validation service to start...{RESET}")
    for i in range(max_wait):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print(f"{GREEN}✓ Service is ready!{RESET}\n")
                return True
        except:
            pass
        time.sleep(1)
        print(f"  Attempt {i+1}/{max_wait}...")
    return False

def test_grover(name, circuit_code, backend=None, opt_level=1):
    """Test a Grover circuit"""
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Testing: {name}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    payload = {
        "code": circuit_code,
        "optimization_level": opt_level
    }
    
    if backend:
        payload["backend_name"] = backend
        print(f"{CYAN}Target Backend: {backend}{RESET}")
    
    print(f"{CYAN}Optimization Level: {opt_level}{RESET}\n")
    
    try:
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"{RED}✗ Request failed with status {response.status_code}{RESET}")
            return False
        
        data = response.json()
        
        if data.get('valid'):
            print(f"{GREEN}✓ Circuit is VALID{RESET}\n")
            
            print(f"{CYAN}Circuit Analysis:{RESET}")
            print(f"  Circuit Hash:       {data.get('circuit_hash', 'N/A')[:24]}...")
            print(f"  Qubits:             {data.get('qubits', 0)}")
            print(f"  Circuit Depth:      {data.get('depth', 0)}")
            print(f"  Total Gates:        {data.get('gates', 0)}")
            print(f"  Estimated Time:     {data.get('estimated_execution_time', 0):.3f} seconds")
            
            if data.get('gate_types'):
                print(f"\n{CYAN}Gate Breakdown:{RESET}")
                for gate, count in sorted(data['gate_types'].items()):
                    print(f"    {gate:12s}: {count:3d}")
            
            if data.get('warnings'):
                print(f"\n{YELLOW}Warnings:{RESET}")
                for warning in data['warnings']:
                    print(f"  ⚠ {warning}")
            
            print()
            return True
        else:
            print(f"{RED}✗ Circuit is INVALID{RESET}\n")
            print(f"{RED}Errors:{RESET}")
            for error in data.get('errors', []):
                print(f"  • {error}")
            print()
            return False
            
    except requests.exceptions.Timeout:
        print(f"{RED}✗ Request timed out{RESET}\n")
        return False
    except Exception as e:
        print(f"{RED}✗ Error: {e}{RESET}\n")
        return False

def main():
    """Run Grover's algorithm tests"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Grover's Search Algorithm - Validation Service Test{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    print(f"{CYAN}Grover's algorithm provides quadratic speedup for unstructured search.{RESET}")
    print(f"{CYAN}For N items, it finds the target in O(√N) steps vs O(N) classically.{RESET}\n")
    
    # Wait for service
    if not wait_for_service():
        print(f"{RED}✗ Service is not available{RESET}")
        print(f"\nPlease start the service first:")
        print(f"  python main.py")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Grover 2-Qubit Search (Simple)", GROVER_2_QUBIT, None, 1),
        ("Grover 3-Qubit Search (Intermediate)", GROVER_3_QUBIT, "ibmq_qasm_simulator", 2),
        ("Grover 4-Qubit Search (Advanced)", GROVER_4_QUBIT, "ibmq_qasm_simulator", 3),
    ]
    
    results = []
    for name, circuit, backend, opt_level in tests:
        result = test_grover(name, circuit, backend, opt_level)
        results.append((name, result))
        time.sleep(0.5)  # Brief pause between tests
    
    # Print summary
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {name:.<50} {status}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    if passed == total:
        print(f"{GREEN}✓ All Grover's algorithm tests passed! ({passed}/{total}){RESET}")
        print(f"\n{CYAN}Grover's algorithm circuits are ready for quantum execution!{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}✗ Some tests failed. ({passed}/{total} passed){RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

