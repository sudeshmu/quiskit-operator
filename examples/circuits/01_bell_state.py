"""
Bell State / Bell Test (Entanglement Test)

Creates a maximally entangled Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
This demonstrates quantum entanglement where measuring one qubit 
immediately determines the state of the other.

Expected Output: 50% |00⟩ and 50% |11⟩ (perfectly correlated)
"""

from qiskit import QuantumCircuit

# Create a 2-qubit circuit with 2 classical bits for measurement
qc = QuantumCircuit(2, 2)

# Apply Hadamard gate to qubit 0 (creates superposition)
qc.h(0)

# Apply CNOT gate with qubit 0 as control and qubit 1 as target
# This creates entanglement
qc.cx(0, 1)

# Measure both qubits
qc.measure([0, 1], [0, 1])

