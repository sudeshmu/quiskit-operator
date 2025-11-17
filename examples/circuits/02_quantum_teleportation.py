"""
Quantum Teleportation Circuit

Demonstrates quantum teleportation protocol where Alice sends 
a quantum state to Bob using entanglement and classical communication.

Protocol:
1. Create entangled pair between Alice and Bob
2. Alice performs Bell measurement on her qubit and the state to teleport
3. Alice sends classical bits to Bob
4. Bob applies corrections based on classical bits
5. Bob now has the original quantum state
"""

from qiskit import QuantumCircuit

# Create 3-qubit circuit (qubit 0: state to teleport, qubits 1&2: entangled pair)
qc = QuantumCircuit(3, 3)

# Prepare the state to teleport (example: |+⟩ state on qubit 0)
qc.h(0)

# Create entangled pair between Alice (qubit 1) and Bob (qubit 2)
qc.h(1)
qc.cx(1, 2)

# Add barrier for visualization
qc.barrier()

# Alice's Bell measurement
qc.cx(0, 1)  # CNOT between state and Alice's qubit
qc.h(0)      # Hadamard on state qubit

# Measure Alice's qubits
qc.measure([0, 1], [0, 1])

# Add barrier
qc.barrier()

# Bob's corrections based on measurement results
qc.cx(1, 2)  # X correction if qubit 1 is |1⟩
qc.cz(0, 2)  # Z correction if qubit 0 is |1⟩

# Measure Bob's qubit (now has the teleported state)
qc.measure(2, 2)

