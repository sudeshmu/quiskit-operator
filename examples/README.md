# Quantum Circuit Examples

A comprehensive collection of quantum algorithm implementations for testing the QiskitOperator validation service.

## 📚 Examples Overview

### 1. **Bell State / Bell Test** (Beginner)
- **File**: `circuits/01_bell_state.py`
- **Category**: Entanglement
- **Description**: Creates a maximally entangled Bell state demonstrating quantum entanglement
- **Qubits**: 2
- **Use Case**: Quantum communication, testing quantum mechanics foundations

### 2. **Quantum Teleportation** (Intermediate)
- **File**: `circuits/02_quantum_teleportation.py`
- **Category**: Quantum Communication
- **Description**: Teleports a quantum state using entanglement and classical communication
- **Qubits**: 3
- **Use Case**: Quantum networks, secure quantum communication

### 3. **Quantum Fourier Transform (QFT)** (Intermediate)
- **File**: `circuits/03_quantum_fourier_transform.py`
- **Category**: Quantum Transform
- **Description**: Quantum analogue of the discrete Fourier transform
- **Qubits**: 4
- **Use Case**: Key subroutine in Shor's algorithm and phase estimation

### 4. **Grover's Search Algorithm** (Intermediate)
- **File**: `circuits/04_grover_search.py`
- **Category**: Search Algorithm
- **Description**: Quantum search with O(√N) speedup over classical algorithms
- **Qubits**: 3
- **Use Case**: Database search, optimization problems

### 5. **Shor's Algorithm** (Advanced)
- **File**: `circuits/05_shor_algorithm.py`
- **Category**: Number Theory
- **Description**: Integer factorization using quantum period finding
- **Qubits**: 8
- **Use Case**: Cryptography, breaking RSA encryption

### 6. **Quantum Random Number Generator** (Beginner)
- **File**: `circuits/06_quantum_random_number_generator.py`
- **Category**: Random Generation
- **Description**: Generates truly random numbers using quantum mechanics
- **Qubits**: 8
- **Use Case**: Cryptographic keys, Monte Carlo simulations

### 7. **Variational Quantum Eigensolver (VQE)** (Advanced)
- **File**: `circuits/07_vqe_circuit.py`
- **Category**: Quantum Chemistry
- **Description**: Hybrid algorithm for finding ground state energy
- **Qubits**: 2
- **Use Case**: Molecular simulation, drug discovery

### 8. **Bernstein-Vazirani Algorithm** (Intermediate)
- **File**: `circuits/08_bernstein_vazirani.py`
- **Category**: Query Algorithm
- **Description**: Finds hidden bit string in a single query
- **Qubits**: 5
- **Use Case**: Query complexity, algorithm demonstration

### 9. **Deutsch-Jozsa Algorithm** (Intermediate)
- **File**: `circuits/09_deutsch_jozsa.py`
- **Category**: Query Algorithm
- **Description**: Determines if function is constant or balanced in one query
- **Qubits**: 4
- **Use Case**: First quantum algorithm showing speedup over classical

### 10. **GHZ State Creation** (Beginner)
- **File**: `circuits/10_ghz_state.py`
- **Category**: Entanglement
- **Description**: Creates maximally entangled multi-qubit state
- **Qubits**: 5
- **Use Case**: Quantum error correction, testing Bell inequalities

---

## 🚀 Quick Start

### Prerequisites

1. **Validation Service Running**:
   ```bash
   cd validation-service
   python3 main.py
   ```

2. **Python Dependencies**:
   ```bash
   pip install requests qiskit
   ```

### Run All Examples

```bash
cd examples
python3 run_all_examples.py
```

### Run with Options

```bash
# Verbose output with detailed circuit information
python3 run_all_examples.py --verbose

# Save regression report to JSON
python3 run_all_examples.py --save-report

# Both options
python3 run_all_examples.py --verbose --save-report
```

---

## 📊 Example Output

```
================================================================================
QUANTUM CIRCUIT EXAMPLES - E2E REGRESSION TEST REPORT
================================================================================

Test Run: 2025-11-17 10:30:45
Total Duration: 12.34s

SUMMARY:
  Total Examples:  10
  Passed: 10
  Failed: 0
  Success Rate:    100.0%

DETAILED RESULTS:

1. Bell State / Bell Test (Beginner) ✓ PASS
   Category: Entanglement
   File: 01_bell_state.py
   Duration: 0.845s
   Circuit Stats:
     • Qubits: 2
     • Depth: 3
     • Gates: 4
     • Hash: 9e974f568998358a...

[... more results ...]

RESULTS BY CATEGORY:

  Entanglement...................... 2/2 (100%)
  Quantum Communication............. 1/1 (100%)
  Search Algorithm.................. 1/1 (100%)
  Query Algorithm................... 2/2 (100%)
  [... more categories ...]

RESULTS BY COMPLEXITY:

  Beginner.......................... 3/3 (100%)
  Intermediate...................... 5/5 (100%)
  Advanced.......................... 2/2 (100%)

================================================================================
✓ ALL TESTS PASSED!
All quantum circuit examples validated successfully.
================================================================================
```

---

## 📁 Directory Structure

```
examples/
├── circuits/                           # Individual circuit examples
│   ├── 01_bell_state.py
│   ├── 02_quantum_teleportation.py
│   ├── 03_quantum_fourier_transform.py
│   ├── 04_grover_search.py
│   ├── 05_shor_algorithm.py
│   ├── 06_quantum_random_number_generator.py
│   ├── 07_vqe_circuit.py
│   ├── 08_bernstein_vazirani.py
│   ├── 09_deutsch_jozsa.py
│   └── 10_ghz_state.py
├── results/                            # Test results and reports
│   └── regression_report_*.json        # Generated regression reports
├── run_all_examples.py                 # Main test runner
└── README.md                           # This file
```

---

## 🔬 Individual Circuit Testing

You can also test individual circuits:

```python
from pathlib import Path
import requests

# Read circuit
with open('circuits/01_bell_state.py', 'r') as f:
    circuit_code = f.read()

# Validate
response = requests.post(
    'http://localhost:8000/validate',
    json={'code': circuit_code, 'optimization_level': 1}
)

print(response.json())
```

---

## 📈 Regression Reports

When using `--save-report`, a detailed JSON report is generated in `results/`:

```json
{
  "timestamp": "2025-11-17T10:30:45.123456",
  "total_duration": 12.34,
  "summary": {
    "total": 10,
    "passed": 10,
    "failed": 0,
    "success_rate": 100.0
  },
  "results": [
    {
      "id": "01",
      "name": "Bell State / Bell Test",
      "success": true,
      "duration": 0.845,
      "validation": {
        "qubits": 2,
        "depth": 3,
        "gates": 4,
        ...
      }
    },
    ...
  ]
}
```

---

## 🎯 Use Cases

### 1. **Continuous Integration**
Add to your CI/CD pipeline to ensure validation service works correctly:
```yaml
- name: Test Quantum Examples
  run: |
    python3 validation-service/main.py &
    sleep 5
    python3 examples/run_all_examples.py --save-report
```

### 2. **Regression Testing**
Run before and after changes to ensure no regressions:
```bash
# Baseline
python3 run_all_examples.py --save-report

# After changes
python3 run_all_examples.py --save-report

# Compare results/regression_report_*.json
```

### 3. **Educational Purposes**
Study quantum algorithms by examining the circuit implementations.

### 4. **Validation Service Testing**
Comprehensive test suite for the validation service with diverse quantum circuits.

---

## 🛠️ Troubleshooting

### Validation Service Not Running
```
✗ Validation service is not available.

Please start the validation service first:
  cd validation-service
  python3 main.py
```

**Solution**: Start the validation service on port 8000.

### Import Errors
```
ModuleNotFoundError: No module named 'qiskit'
```

**Solution**: Install dependencies:
```bash
pip install qiskit requests
```

### Port Already in Use
```
Address already in use
```

**Solution**: Stop existing service or use different port:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

---

## 📖 Further Reading

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Quantum Computing Algorithms](https://en.wikipedia.org/wiki/Quantum_algorithm)
- [QiskitOperator Documentation](../README.md)

---

## 🤝 Contributing

To add new examples:

1. Create new circuit file in `circuits/` following naming convention
2. Add comprehensive docstring explaining the algorithm
3. Add entry to `EXAMPLES` list in `run_all_examples.py`
4. Update this README

---

## 📝 License

Apache License 2.0 - See LICENSE file for details

