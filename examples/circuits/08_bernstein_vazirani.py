"""
Bernstein-Vazirani Algorithm

Finds a hidden bit string s in a single query, compared to n queries
classically. Given a function f(x) = s·x (mod 2), the algorithm determines s.

This example finds a hidden 4-bit string s = 1011.

Classical: Would need 4 queries to determine each bit
Quantum: Finds all 4 bits in a single query
"""

from qiskit import QuantumCircuit

# Hidden bit string (example: s = '1011')
hidden_string = '1011'
n = len(hidden_string)

# Create circuit: n qubits + 1 ancilla for phase kickback
qc = QuantumCircuit(n + 1, n)

# Initialize ancilla in |−⟩ state for phase kickback
qc.x(n)
qc.h(n)

# Initialize input qubits in superposition
for qubit in range(n):
    qc.h(qubit)

qc.barrier()

# Oracle: Apply CNOT for each '1' in hidden string
# If s[i] = '1', apply CNOT from qubit i to ancilla
# For hidden_string = '1011': reversed = '1101'
reversed_string = hidden_string[::-1]
for i in range(len(reversed_string)):
    if reversed_string[i] == '1':
        qc.cx(i, n)

qc.barrier()

# Apply Hadamard to input qubits
for qubit in range(n):
    qc.h(qubit)

qc.barrier()

# Measure input qubits (result will be the hidden string)
qc.measure(range(n), range(n))

