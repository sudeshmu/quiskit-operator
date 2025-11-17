"""
Grover's Search Algorithm

Quantum search algorithm that finds a marked item in an unsorted database
with O(√N) queries, compared to O(N) for classical algorithms.

This example searches for the state |101⟩ in a 3-qubit system.
With optimal iterations, Grover's algorithm amplifies the probability
of measuring the target state to near 100%.
"""

from qiskit import QuantumCircuit
import math

# Create 3-qubit circuit for searching
qc = QuantumCircuit(3, 3)

# Initialize: Create equal superposition
qc.h([0, 1, 2])
qc.barrier()

# Calculate optimal number of iterations: π/4 * sqrt(2^n)
n_qubits = 3
optimal_iterations = int(math.pi/4 * math.sqrt(2**n_qubits))

# Grover iterations
for iteration in range(optimal_iterations):
    # Oracle: Mark the state |101⟩
    # Flip phase of |101⟩
    qc.x(1)  # Flip middle qubit (so we're looking for |111⟩)
    qc.h(2)
    qc.ccx(0, 1, 2)  # Toffoli gate
    qc.h(2)
    qc.x(1)  # Flip back
    
    qc.barrier()
    
    # Diffusion operator (inversion about average)
    qc.h([0, 1, 2])
    qc.x([0, 1, 2])
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x([0, 1, 2])
    qc.h([0, 1, 2])
    
    qc.barrier()

# Measure all qubits
qc.measure([0, 1, 2], [0, 1, 2])

