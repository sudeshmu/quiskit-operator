#!/usr/bin/env python3
"""
Quantum Algorithm Examples - End-to-End Test Suite

This script runs all quantum circuit examples through the validation service
and generates a comprehensive regression report.

Usage:
    python run_all_examples.py [--save-report] [--verbose]
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

BASE_URL = "http://localhost:8000"

# Example definitions
EXAMPLES = [
    {
        "id": "01",
        "name": "Bell State / Bell Test",
        "file": "01_bell_state.py",
        "category": "Entanglement",
        "complexity": "Beginner",
        "qubits_expected": 2,
        "description": "Creates maximally entangled Bell state"
    },
    {
        "id": "02",
        "name": "Quantum Teleportation",
        "file": "02_quantum_teleportation.py",
        "category": "Quantum Communication",
        "complexity": "Intermediate",
        "qubits_expected": 3,
        "description": "Teleports quantum state using entanglement"
    },
    {
        "id": "03",
        "name": "Quantum Fourier Transform",
        "file": "03_quantum_fourier_transform.py",
        "category": "Quantum Transform",
        "complexity": "Intermediate",
        "qubits_expected": 4,
        "description": "Quantum analogue of discrete Fourier transform"
    },
    {
        "id": "04",
        "name": "Grover's Search Algorithm",
        "file": "04_grover_search.py",
        "category": "Search Algorithm",
        "complexity": "Intermediate",
        "qubits_expected": 3,
        "description": "Quantum search with quadratic speedup"
    },
    {
        "id": "05",
        "name": "Shor's Algorithm",
        "file": "05_shor_algorithm.py",
        "category": "Number Theory",
        "complexity": "Advanced",
        "qubits_expected": 8,
        "description": "Integer factorization using quantum period finding"
    },
    {
        "id": "06",
        "name": "Quantum Random Number Generator",
        "file": "06_quantum_random_number_generator.py",
        "category": "Random Generation",
        "complexity": "Beginner",
        "qubits_expected": 8,
        "description": "True random number generation"
    },
    {
        "id": "07",
        "name": "Variational Quantum Eigensolver",
        "file": "07_vqe_circuit.py",
        "category": "Quantum Chemistry",
        "complexity": "Advanced",
        "qubits_expected": 2,
        "description": "Hybrid algorithm for ground state energy"
    },
    {
        "id": "08",
        "name": "Bernstein-Vazirani Algorithm",
        "file": "08_bernstein_vazirani.py",
        "category": "Query Algorithm",
        "complexity": "Intermediate",
        "qubits_expected": 5,
        "description": "Finds hidden bit string in single query"
    },
    {
        "id": "09",
        "name": "Deutsch-Jozsa Algorithm",
        "file": "09_deutsch_jozsa.py",
        "category": "Query Algorithm",
        "complexity": "Intermediate",
        "qubits_expected": 4,
        "description": "Determines if function is constant or balanced"
    },
    {
        "id": "10",
        "name": "GHZ State Creation",
        "file": "10_ghz_state.py",
        "category": "Entanglement",
        "complexity": "Beginner",
        "qubits_expected": 5,
        "description": "Maximally entangled multi-qubit state"
    }
]


class TestResult:
    """Stores test results for an example"""
    def __init__(self, example: Dict, success: bool, validation_data: Optional[Dict] = None, 
                 error: Optional[str] = None, duration: float = 0.0):
        self.example = example
        self.success = success
        self.validation_data = validation_data
        self.error = error
        self.duration = duration


class RegressionReport:
    """Generates comprehensive regression report"""
    def __init__(self, results: List[TestResult], total_duration: float):
        self.results = results
        self.total_duration = total_duration
        self.timestamp = datetime.now()
    
    def print_console_report(self, verbose: bool = False):
        """Print colorful console report"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}QUANTUM CIRCUIT EXAMPLES - E2E REGRESSION TEST REPORT{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}Test Run: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.CYAN}Total Duration: {self.total_duration:.2f}s{Colors.RESET}\n")
        
        # Summary statistics
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        
        print(f"{Colors.BOLD}SUMMARY:{Colors.RESET}")
        print(f"  Total Examples:  {total}")
        print(f"  {Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"  {Colors.RED}Failed: {failed}{Colors.RESET}")
        print(f"  Success Rate:    {(passed/total*100):.1f}%\n")
        
        # Detailed results
        print(f"{Colors.BOLD}DETAILED RESULTS:{Colors.RESET}\n")
        
        for i, result in enumerate(self.results, 1):
            example = result.example
            status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result.success else f"{Colors.RED}✗ FAIL{Colors.RESET}"
            
            print(f"{Colors.BOLD}{i}. {example['name']}{Colors.RESET} ({example['complexity']}) {status}")
            print(f"   Category: {example['category']}")
            print(f"   File: {example['file']}")
            print(f"   Duration: {result.duration:.3f}s")
            
            if result.success and result.validation_data:
                data = result.validation_data
                print(f"   {Colors.CYAN}Circuit Stats:{Colors.RESET}")
                print(f"     • Qubits: {data.get('qubits', 'N/A')}")
                print(f"     • Depth: {data.get('depth', 'N/A')}")
                print(f"     • Gates: {data.get('gates', 'N/A')}")
                print(f"     • Hash: {data.get('circuit_hash', 'N/A')[:16]}...")
                
                if verbose and data.get('gate_types'):
                    print(f"     • Gate Types: {', '.join(f'{k}({v})' for k, v in data['gate_types'].items())}")
                
                if data.get('warnings'):
                    print(f"   {Colors.YELLOW}⚠ Warnings: {', '.join(data['warnings'])}{Colors.RESET}")
            elif not result.success:
                print(f"   {Colors.RED}Error: {result.error}{Colors.RESET}")
            
            print()
        
        # Category breakdown
        print(f"{Colors.BOLD}RESULTS BY CATEGORY:{Colors.RESET}\n")
        categories = {}
        for result in self.results:
            cat = result.example['category']
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0}
            if result.success:
                categories[cat]['passed'] += 1
            else:
                categories[cat]['failed'] += 1
        
        for category, stats in sorted(categories.items()):
            total_cat = stats['passed'] + stats['failed']
            rate = stats['passed'] / total_cat * 100 if total_cat > 0 else 0
            status_color = Colors.GREEN if rate == 100 else (Colors.YELLOW if rate >= 50 else Colors.RED)
            print(f"  {category:.<30} {status_color}{stats['passed']}/{total_cat} ({rate:.0f}%){Colors.RESET}")
        
        # Complexity breakdown
        print(f"\n{Colors.BOLD}RESULTS BY COMPLEXITY:{Colors.RESET}\n")
        complexity = {}
        for result in self.results:
            comp = result.example['complexity']
            if comp not in complexity:
                complexity[comp] = {'passed': 0, 'failed': 0}
            if result.success:
                complexity[comp]['passed'] += 1
            else:
                complexity[comp]['failed'] += 1
        
        for level in ['Beginner', 'Intermediate', 'Advanced']:
            if level in complexity:
                stats = complexity[level]
                total_comp = stats['passed'] + stats['failed']
                rate = stats['passed'] / total_comp * 100 if total_comp > 0 else 0
                status_color = Colors.GREEN if rate == 100 else (Colors.YELLOW if rate >= 50 else Colors.RED)
                print(f"  {level:.<30} {status_color}{stats['passed']}/{total_comp} ({rate:.0f}%){Colors.RESET}")
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.RESET}")
        
        if passed == total:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.RESET}")
            print(f"{Colors.GREEN}All quantum circuit examples validated successfully.{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ SOME TESTS FAILED{Colors.RESET}")
            print(f"{Colors.YELLOW}{failed} out of {total} examples failed validation.{Colors.RESET}")
        
        print(f"{Colors.BLUE}{Colors.BOLD}{'='*80}{Colors.RESET}\n")
    
    def save_json_report(self, output_dir: Path):
        """Save detailed JSON report"""
        report_data = {
            "timestamp": self.timestamp.isoformat(),
            "total_duration": self.total_duration,
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results if r.success),
                "failed": sum(1 for r in self.results if not r.success),
                "success_rate": sum(1 for r in self.results if r.success) / len(self.results) * 100
            },
            "results": [
                {
                    "id": r.example['id'],
                    "name": r.example['name'],
                    "file": r.example['file'],
                    "category": r.example['category'],
                    "complexity": r.example['complexity'],
                    "success": r.success,
                    "duration": r.duration,
                    "validation": r.validation_data if r.success else None,
                    "error": r.error if not r.success else None
                }
                for r in self.results
            ]
        }
        
        output_file = output_dir / f"regression_report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return output_file


def wait_for_service(max_wait: int = 30) -> bool:
    """Wait for validation service to be ready"""
    print(f"{Colors.CYAN}Waiting for validation service...{Colors.RESET}")
    for i in range(max_wait):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print(f"{Colors.GREEN}✓ Validation service is ready!{Colors.RESET}\n")
                return True
        except:
            pass
        if i < max_wait - 1:
            time.sleep(1)
    return False


def validate_circuit(circuit_file: Path) -> Tuple[bool, Optional[Dict], Optional[str], float]:
    """Validate a circuit file"""
    start_time = time.time()
    
    try:
        # Read circuit code
        with open(circuit_file, 'r') as f:
            circuit_code = f.read()
        
        # Send validation request
        payload = {
            "code": circuit_code,
            "optimization_level": 2
        }
        
        response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=30)
        duration = time.time() - start_time
        
        if response.status_code != 200:
            return False, None, f"HTTP {response.status_code}", duration
        
        data = response.json()
        
        if data.get('valid'):
            return True, data, None, duration
        else:
            errors = '; '.join(data.get('errors', ['Unknown error']))
            return False, None, errors, duration
    
    except Exception as e:
        duration = time.time() - start_time
        return False, None, str(e), duration


def run_all_tests(circuits_dir: Path, verbose: bool = False) -> List[TestResult]:
    """Run all example tests"""
    results = []
    
    print(f"{Colors.BOLD}Running {len(EXAMPLES)} quantum circuit examples...{Colors.RESET}\n")
    
    for i, example in enumerate(EXAMPLES, 1):
        circuit_file = circuits_dir / example['file']
        
        print(f"{Colors.CYAN}[{i}/{len(EXAMPLES)}] Testing: {example['name']}...{Colors.RESET}", end=' ')
        
        if not circuit_file.exists():
            print(f"{Colors.RED}✗ File not found{Colors.RESET}")
            results.append(TestResult(example, False, error="File not found"))
            continue
        
        success, validation_data, error, duration = validate_circuit(circuit_file)
        
        if success:
            print(f"{Colors.GREEN}✓ PASS{Colors.RESET} ({duration:.2f}s)")
            if verbose and validation_data:
                print(f"  └─ {validation_data['qubits']}q, {validation_data['depth']}d, {validation_data['gates']}g")
        else:
            print(f"{Colors.RED}✗ FAIL{Colors.RESET} ({duration:.2f}s)")
            if verbose:
                print(f"  └─ Error: {error}")
        
        results.append(TestResult(example, success, validation_data, error, duration))
        time.sleep(0.3)  # Brief pause between tests
    
    print()
    return results


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='Run quantum circuit examples E2E tests')
    parser.add_argument('--save-report', action='store_true', help='Save JSON regression report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    circuits_dir = script_dir / 'circuits'
    results_dir = script_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # Check if validation service is running
    if not wait_for_service():
        print(f"{Colors.RED}✗ Validation service is not available.{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Please start the validation service first:{Colors.RESET}")
        print(f"  cd validation-service")
        print(f"  python3 main.py")
        print(f"\nOr use Docker:")
        print(f"  docker run -p 8000:8000 qiskit-validation-service")
        sys.exit(1)
    
    # Run all tests
    start_time = time.time()
    results = run_all_tests(circuits_dir, verbose=args.verbose)
    total_duration = time.time() - start_time
    
    # Generate report
    report = RegressionReport(results, total_duration)
    report.print_console_report(verbose=args.verbose)
    
    # Save JSON report if requested
    if args.save_report:
        report_file = report.save_json_report(results_dir)
        print(f"{Colors.GREEN}✓ Regression report saved: {report_file}{Colors.RESET}\n")
    
    # Exit with appropriate code
    all_passed = all(r.success for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

