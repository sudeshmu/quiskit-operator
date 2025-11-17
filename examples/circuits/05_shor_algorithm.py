"""
Shor's Algorithm (Factoring 15)

Quantum algorithm for integer factorization. This is a simplified version
that factors N=15 using period finding with a=7.

Shor's algorithm:
1. Choose random a < N
2. Use quantum period finding to find period r of f(x) = a^x mod N
3. If r is even and a^(r/2) ≠ -1 (mod N), factors are gcd(a^(r/2)±1, N)

This implementation focuses on the quantum period-finding subroutine.
For N=15, a=7: 7^1=7, 7^2=4, 7^3=13, 7^4=1 (period r=4)
"""

from qiskit import QuantumCircuit
import math

# Number to factor: N = 15, using a = 7
N = 15
a = 7

# Number of qubits needed for period finding
n_count = 4  # Counting qubits for phase estimation

# Create circuit: counting qubits + work qubits
qc = QuantumCircuit(n_count + 4, n_count)

# Initialize counting qubits in superposition
for qubit in range(n_count):
    qc.h(qubit)

qc.barrier()

# Prepare |1⟩ in work register (for modular exponentiation)
qc.x(n_count)

# Controlled modular exponentiation: a^(2^j) mod 15
# This is simplified - full implementation would use modular arithmetic circuits
# For a=7, N=15: implement controlled-U operations
repetitions = 1
for counting_qubit in range(n_count):
    # Simplified controlled operations (placeholder for actual modular exponentiation)
    for _ in range(repetitions):
        # Apply controlled operations based on a^(2^j) mod N
        qc.cx(counting_qubit, n_count + 1)
        qc.cx(counting_qubit, n_count + 2)
    repetitions *= 2

qc.barrier()

# Inverse QFT on counting qubits
def inverse_qft(circuit, n):
    """Apply inverse QFT"""
    # Swap qubits
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    
    # Apply inverse QFT rotations
    for j in range(n):
        for m in range(j):
            circuit.cp(-math.pi/2**(j-m), m, j)
        circuit.h(j)

inverse_qft(qc, n_count)

qc.barrier()

# Measure counting qubits
qc.measure(range(n_count), range(n_count))

