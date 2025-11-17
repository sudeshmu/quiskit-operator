"""
GHZ State Creation

Creates a Greenberger-Horne-Zeilinger (GHZ) state, which is a maximally
entangled state of n qubits. For 4 qubits:

|GHZ⟩ = (|0000⟩ + |1111⟩)/√2

GHZ states are used to test quantum mechanics vs local hidden variable
theories and are useful for quantum error correction and quantum communication.

This example creates a 5-qubit GHZ state.
Expected outcome: 50% |00000⟩ and 50% |11111⟩
"""

from qiskit import QuantumCircuit

# Number of qubits for GHZ state
n_qubits = 5

# Create circuit
qc = QuantumCircuit(n_qubits, n_qubits)

# Create GHZ state
# 1. Apply Hadamard to first qubit (creates superposition)
qc.h(0)

qc.barrier()

# 2. Apply CNOT gates to entangle all qubits
for qubit in range(n_qubits - 1):
    qc.cx(qubit, qubit + 1)

qc.barrier()

# Measure all qubits
qc.measure(range(n_qubits), range(n_qubits))

