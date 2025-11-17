"""
Variational Quantum Eigensolver (VQE)

VQE is a hybrid quantum-classical algorithm for finding the ground state
energy of a molecule or quantum system. This is the ansatz circuit used
in VQE for a simple 2-qubit system.

The circuit is parameterized and would be optimized classically to minimize
the expectation value of the Hamiltonian.

This example shows a Hardware Efficient Ansatz for H2 molecule.
"""

from qiskit import QuantumCircuit
import math

# Create a 2-qubit circuit for VQE ansatz
qc = QuantumCircuit(2, 2)

# Initial state preparation
qc.ry(math.pi/4, 0)  # Parameterized rotation (θ1)
qc.ry(math.pi/4, 1)  # Parameterized rotation (θ2)

qc.barrier()

# Entangling layer
qc.cx(0, 1)

qc.barrier()

# Additional rotation layer
qc.ry(math.pi/6, 0)  # Parameterized rotation (θ3)
qc.ry(math.pi/6, 1)  # Parameterized rotation (θ4)

qc.barrier()

# Second entangling layer
qc.cx(1, 0)

qc.barrier()

# Final rotation layer
qc.ry(math.pi/8, 0)  # Parameterized rotation (θ5)
qc.ry(math.pi/8, 1)  # Parameterized rotation (θ6)

# Measure in computational basis
qc.measure([0, 1], [0, 1])

