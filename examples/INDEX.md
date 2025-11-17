# Quantum Circuit Examples - Complete Index

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Test Coverage**: 100%  
**Last Updated**: November 17, 2025

---

## 📚 Documentation Files

| File | Purpose | Size |
|------|---------|------|
| **[README.md](README.md)** | Complete documentation and guide | 8.4 KB |
| **[QUICK_START.md](QUICK_START.md)** | Quick reference guide | 6.5 KB |
| **[TEST_SUMMARY.md](TEST_SUMMARY.md)** | Detailed test results | 6.5 KB |
| **INDEX.md** | This file - navigation hub | - |

---

## 🔬 Quantum Circuit Examples

### Beginner Level (🟢)

| # | File | Algorithm | Qubits | Description |
|---|------|-----------|--------|-------------|
| 1 | [01_bell_state.py](circuits/01_bell_state.py) | Bell State | 2 | Quantum entanglement demonstration |
| 6 | [06_quantum_random_number_generator.py](circuits/06_quantum_random_number_generator.py) | QRNG | 8 | True random number generation |
| 10 | [10_ghz_state.py](circuits/10_ghz_state.py) | GHZ State | 5 | Multi-qubit entanglement |

### Intermediate Level (🟡)

| # | File | Algorithm | Qubits | Description |
|---|------|-----------|--------|-------------|
| 2 | [02_quantum_teleportation.py](circuits/02_quantum_teleportation.py) | Teleportation | 3 | Quantum state transfer protocol |
| 3 | [03_quantum_fourier_transform.py](circuits/03_quantum_fourier_transform.py) | QFT | 4 | Quantum Fourier transform |
| 4 | [04_grover_search.py](circuits/04_grover_search.py) | Grover's | 3 | Quantum search algorithm |
| 8 | [08_bernstein_vazirani.py](circuits/08_bernstein_vazirani.py) | Bernstein-Vazirani | 5 | Hidden bit string finder |
| 9 | [09_deutsch_jozsa.py](circuits/09_deutsch_jozsa.py) | Deutsch-Jozsa | 4 | Function type determination |

### Advanced Level (🔴)

| # | File | Algorithm | Qubits | Description |
|---|------|-----------|--------|-------------|
| 5 | [05_shor_algorithm.py](circuits/05_shor_algorithm.py) | Shor's | 8 | Integer factorization |
| 7 | [07_vqe_circuit.py](circuits/07_vqe_circuit.py) | VQE | 2 | Variational quantum eigensolver |

---

## 🔧 Testing & Tools

| File | Purpose |
|------|---------|
| **[run_all_examples.py](run_all_examples.py)** | Main E2E test runner with regression reporting |

### Test Reports

Located in `results/` directory:
- `regression_report_20251117_171212.json` - Latest test results (100% pass)
- Automatic timestamped reports generated on each test run

---

## 📊 Algorithm Categories

### Entanglement (2 examples)
- Bell State / Bell Test
- GHZ State Creation

### Quantum Communication (1 example)
- Quantum Teleportation

### Quantum Transform (1 example)
- Quantum Fourier Transform

### Search Algorithms (1 example)
- Grover's Search Algorithm

### Number Theory (1 example)
- Shor's Algorithm

### Random Generation (1 example)
- Quantum Random Number Generator

### Quantum Chemistry (1 example)
- Variational Quantum Eigensolver

### Query Algorithms (2 examples)
- Bernstein-Vazirani Algorithm
- Deutsch-Jozsa Algorithm

---

## 🎯 Quick Commands

```bash
# View documentation
cat README.md              # Full guide
cat QUICK_START.md         # Quick reference
cat TEST_SUMMARY.md        # Test results

# Run tests
python3 run_all_examples.py                    # Basic run
python3 run_all_examples.py --verbose          # Verbose output
python3 run_all_examples.py --save-report      # Save JSON report
python3 run_all_examples.py --verbose --save-report  # Full options

# View individual circuits
cat circuits/01_bell_state.py
cat circuits/04_grover_search.py
# ... etc
```

---

## 📈 Test Statistics

```
Total Examples:   10
Success Rate:     100%
Total Duration:   3.45 seconds
Average per Test: 0.34 seconds
```

### By Complexity
- Beginner: 3/3 (100%)
- Intermediate: 5/5 (100%)
- Advanced: 2/2 (100%)

### By Category
- All 8 categories: 100% success rate

---

## 🚀 Integration Points

### With Validation Service
All examples are validated through:
```
qiskit-operator/validation-service/
```

### CI/CD Integration
Examples include GitHub Actions workflow for:
- Automated testing
- Regression report generation
- Artifact upload

### Kubernetes Deployment
Can be integrated with QiskitOperator for:
- Job validation
- Circuit analysis
- Pre-deployment checks

---

## 📖 Learning Path

1. **Start Here**: [QUICK_START.md](QUICK_START.md)
2. **Deep Dive**: [README.md](README.md)
3. **Run Tests**: `python3 run_all_examples.py --verbose`
4. **Study Circuits**: Begin with `circuits/01_bell_state.py`
5. **Check Results**: [TEST_SUMMARY.md](TEST_SUMMARY.md)

---

## 🔗 Related Resources

- **QiskitOperator**: `../README.md`
- **Validation Service**: `../validation-service/`
- **Qiskit Documentation**: https://qiskit.org/documentation/
- **Quantum Computing**: https://en.wikipedia.org/wiki/Quantum_computing

---

## 📝 File Manifest

```
examples/
├── circuits/               # 10 quantum circuit implementations
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
│
├── results/                # Test results and reports
│   └── regression_report_*.json
│
├── run_all_examples.py     # Test runner script
├── README.md               # Full documentation
├── QUICK_START.md          # Quick reference
├── TEST_SUMMARY.md         # Test results
└── INDEX.md                # This file
```

---

## ✅ Validation Checklist

- [x] 10 quantum algorithms implemented
- [x] All circuits tested and validated
- [x] 100% test success rate
- [x] Documentation complete
- [x] E2E test framework working
- [x] Regression reports generated
- [x] CI/CD ready
- [x] Production ready

---

## 🎓 Support

For questions or issues:
1. Check [README.md](README.md) for detailed documentation
2. Review [TEST_SUMMARY.md](TEST_SUMMARY.md) for examples
3. Examine regression reports in `results/`
4. Study individual circuit implementations in `circuits/`

---

**Status**: ✅ Complete and Tested  
**Maintainer**: QiskitOperator Team  
**License**: Apache 2.0

