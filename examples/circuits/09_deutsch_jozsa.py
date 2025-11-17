"""
Deutsch-Jozsa Algorithm

Determines if a function f:{0,1}^n → {0,1} is constant or balanced
in a single query, compared to 2^(n-1)+1 queries classically.

- Constant: f(x) = 0 for all x, or f(x) = 1 for all x
- Balanced: f(x) = 0 for half the inputs, f(x) = 1 for the other half

This example uses a 3-qubit balanced oracle.
Result: If all qubits measure |0⟩ → constant, otherwise → balanced
"""

from qiskit import QuantumCircuit

# Number of input qubits
n = 3

# Create circuit: n input qubits + 1 output qubit
qc = QuantumCircuit(n + 1, n)

# Initialize output qubit in |−⟩ state
qc.x(n)
qc.h(n)

# Initialize input qubits in superposition
for qubit in range(n):
    qc.h(qubit)

qc.barrier()

# Oracle for balanced function (example: f(x) = x0 ⊕ x1 ⊕ x2)
# This oracle is balanced (outputs 0 for half inputs, 1 for other half)
qc.cx(0, n)
qc.cx(1, n)
qc.cx(2, n)

qc.barrier()

# Apply Hadamard to input qubits
for qubit in range(n):
    qc.h(qubit)

qc.barrier()

# Measure input qubits
# Result: |000⟩ = constant, anything else = balanced
qc.measure(range(n), range(n))

