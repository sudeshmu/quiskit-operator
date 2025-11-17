"""
Quantum Random Number Generator (QRNG)

Uses quantum superposition to generate truly random numbers.
Unlike classical pseudo-random number generators, QRNG produces
truly random numbers based on quantum mechanics.

This implementation generates 8 random bits (0-255).
"""

from qiskit import QuantumCircuit

# Create an 8-qubit circuit for 8-bit random number (0-255)
n_bits = 8
qc = QuantumCircuit(n_bits, n_bits)

# Apply Hadamard gate to all qubits
# This puts each qubit in equal superposition |0⟩ + |1⟩
for qubit in range(n_bits):
    qc.h(qubit)

# Add barrier for visualization
qc.barrier()

# Measure all qubits
# Each measurement will randomly collapse to |0⟩ or |1⟩
# giving us a truly random bit string
qc.measure(range(n_bits), range(n_bits))

