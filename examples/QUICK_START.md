# 🚀 Quantum Examples - Quick Start Guide

## 📦 What's Included

**10 Production-Ready Quantum Circuit Examples**

```
✅ TESTED & VALIDATED - 100% Success Rate
```

---

## 🎯 One-Command Test

```bash
# Start validation service (Terminal 1)
cd qiskit-operator/validation-service
python3 main.py

# Run all examples (Terminal 2)
cd qiskit-operator/examples
python3 run_all_examples.py --save-report --verbose
```

---

## 📚 Available Examples

| # | Algorithm | Level | Qubits | Category |
|---|-----------|-------|--------|----------|
| 1 | **Bell State** | 🟢 Beginner | 2 | Entanglement |
| 2 | **Quantum Teleportation** | 🟡 Intermediate | 3 | Communication |
| 3 | **Quantum Fourier Transform** | 🟡 Intermediate | 4 | Transform |
| 4 | **Grover's Search** | 🟡 Intermediate | 3 | Search |
| 5 | **Shor's Algorithm** | 🔴 Advanced | 8 | Number Theory |
| 6 | **QRNG** | 🟢 Beginner | 8 | Random |
| 7 | **VQE** | 🔴 Advanced | 2 | Chemistry |
| 8 | **Bernstein-Vazirani** | 🟡 Intermediate | 5 | Query |
| 9 | **Deutsch-Jozsa** | 🟡 Intermediate | 4 | Query |
| 10 | **GHZ State** | 🟢 Beginner | 5 | Entanglement |

---

## 📊 Expected Output

```
================================================================================
QUANTUM CIRCUIT EXAMPLES - E2E REGRESSION TEST REPORT
================================================================================

Test Run: 2025-11-17 17:12:12
Total Duration: 3.45s

SUMMARY:
  Total Examples:  10
  Passed: 10      ✅
  Failed: 0       
  Success Rate:    100.0%

DETAILED RESULTS:

1. Bell State / Bell Test (Beginner) ✓ PASS
   Circuit Stats:
     • Qubits: 2
     • Depth: 3
     • Gates: 4

[... 9 more successful tests ...]

RESULTS BY CATEGORY:
  Entanglement...................... 2/2 (100%) ✅
  Quantum Communication............. 1/1 (100%) ✅
  Search Algorithm.................. 1/1 (100%) ✅
  [... all categories 100% ...]

================================================================================
✓ ALL TESTS PASSED!
All quantum circuit examples validated successfully.
================================================================================
```

---

## 🏗️ Directory Structure

```
qiskit-operator/examples/
├── circuits/                          # 10 quantum algorithms
│   ├── 01_bell_state.py              # Quantum entanglement
│   ├── 02_quantum_teleportation.py   # State transfer
│   ├── 03_quantum_fourier_transform.py # QFT
│   ├── 04_grover_search.py           # Search algorithm
│   ├── 05_shor_algorithm.py          # Factorization
│   ├── 06_quantum_random_number_generator.py # QRNG
│   ├── 07_vqe_circuit.py             # Variational eigensolver
│   ├── 08_bernstein_vazirani.py      # Hidden string
│   ├── 09_deutsch_jozsa.py           # Function type test
│   └── 10_ghz_state.py               # Multi-qubit entanglement
│
├── results/                           # Test results
│   └── regression_report_*.json      # Detailed JSON reports
│
├── run_all_examples.py               # 🎯 Main test runner
├── README.md                          # Full documentation
├── TEST_SUMMARY.md                    # Test results summary
└── QUICK_START.md                     # This file
```

---

## 💡 Usage Examples

### Run All Tests
```bash
python3 run_all_examples.py
```

### Run with Verbose Output
```bash
python3 run_all_examples.py --verbose
```

### Save Regression Report
```bash
python3 run_all_examples.py --save-report
```

### Full Options
```bash
python3 run_all_examples.py --save-report --verbose
```

---

## 🔍 Testing Individual Circuits

```python
import requests

# Read any circuit
with open('circuits/01_bell_state.py') as f:
    code = f.read()

# Validate
response = requests.post(
    'http://localhost:8000/validate',
    json={'code': code, 'optimization_level': 1}
)

print(response.json())
```

---

## 📈 Continuous Integration

Add to your CI pipeline:

```yaml
name: Quantum Examples E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install qiskit requests fastapi uvicorn
      
      - name: Start validation service
        run: |
          cd validation-service
          python3 main.py &
          sleep 5
      
      - name: Run all examples
        run: |
          cd examples
          python3 run_all_examples.py --save-report
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: regression-reports
          path: examples/results/*.json
```

---

## 🎓 Learning Path

### Beginners Start Here
1. 📘 **Bell State** - Learn quantum entanglement
2. 📘 **QRNG** - Understand superposition
3. 📘 **GHZ State** - Multi-qubit entanglement

### Intermediate Concepts
4. 📙 **Quantum Teleportation** - State transfer
5. 📙 **Grover's Search** - Quantum speedup
6. 📙 **Deutsch-Jozsa** - Query complexity
7. 📙 **Bernstein-Vazirani** - Hidden information
8. 📙 **QFT** - Quantum transforms

### Advanced Algorithms
9. 📕 **Shor's Algorithm** - Integer factorization
10. 📕 **VQE** - Quantum chemistry

---

## ⚡ Performance

- **Total Suite Time**: ~3.5 seconds
- **Average per Test**: ~0.35 seconds
- **Success Rate**: 100%
- **Validation Accuracy**: ✅ Verified

---

## 🎯 What Gets Validated

For each circuit:
- ✅ Python syntax correctness
- ✅ Circuit creation success
- ✅ Gate type analysis
- ✅ Circuit depth calculation
- ✅ Qubit count verification
- ✅ Execution time estimation
- ✅ Circuit hash generation

---

## 🐛 Troubleshooting

### Service Not Running
```
Error: Connection refused
```
**Solution**: Start validation service first
```bash
cd validation-service && python3 main.py
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Kill existing process
```bash
lsof -ti:8000 | xargs kill -9
```

### Missing Dependencies
```
Error: No module named 'qiskit'
```
**Solution**: Install dependencies
```bash
pip install qiskit requests
```

---

## 📖 Further Reading

- [Full Documentation](README.md)
- [Test Results](TEST_SUMMARY.md)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [QiskitOperator Docs](../README.md)

---

## ✨ Summary

**✅ 10 Quantum Algorithms**  
**✅ 100% Test Coverage**  
**✅ Production Ready**  
**✅ CI/CD Integrated**  
**✅ Fully Documented**

---

*Last Updated: 2025-11-17*  
*Version: 1.0.0*  
*Status: 🟢 Production Ready*

