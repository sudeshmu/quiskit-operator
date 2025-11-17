"""
Quantum Fourier Transform (QFT)

The quantum analogue of the discrete Fourier transform.
QFT is a key subroutine in many quantum algorithms including 
Shor's algorithm and quantum phase estimation.

For n qubits: |j⟩ → (1/√2^n) Σ exp(2πijk/2^n)|k⟩

This example implements 4-qubit QFT.
"""

from qiskit import QuantumCircuit
import math

# Create a 4-qubit circuit for QFT
qc = QuantumCircuit(4)

# Prepare initial state (example: |0101⟩)
qc.x(1)
qc.x(3)

qc.barrier()

# QFT implementation for 4 qubits (manual expansion)
# Qubit 3
qc.h(3)
qc.cp(math.pi/2, 2, 3)
qc.cp(math.pi/4, 1, 3)
qc.cp(math.pi/8, 0, 3)

# Qubit 2
qc.h(2)
qc.cp(math.pi/2, 1, 2)
qc.cp(math.pi/4, 0, 2)

# Qubit 1
qc.h(1)
qc.cp(math.pi/2, 0, 1)

# Qubit 0
qc.h(0)

# Swap qubits to reverse order (part of QFT)
qc.swap(0, 3)
qc.swap(1, 2)

qc.barrier()

# Measure all qubits
qc.measure_all()

