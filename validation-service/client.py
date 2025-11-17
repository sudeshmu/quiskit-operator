"""
Simple Python client for the QiskitOperator Validation Service

This module provides a simple interface to interact with the validation service.
Can be used for integration testing or as a library in other Python applications.

Example usage:
    from client import ValidationClient
    
    client = ValidationClient("http://localhost:8000")
    
    circuit_code = '''
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    '''
    
    result = client.validate_circuit(circuit_code)
    if result.valid:
        print(f"Circuit is valid! Qubits: {result.qubits}, Depth: {result.depth}")
    else:
        print(f"Circuit is invalid: {result.errors}")
"""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of circuit validation"""
    valid: bool
    circuit_hash: str
    depth: int = 0
    qubits: int = 0
    gates: int = 0
    gate_types: Dict[str, int] = None
    estimated_execution_time: float = 0.0
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.gate_types is None:
            self.gate_types = {}
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
    
    def __str__(self) -> str:
        if self.valid:
            return (f"✓ Valid Circuit\n"
                   f"  Hash: {self.circuit_hash[:16]}...\n"
                   f"  Qubits: {self.qubits}, Depth: {self.depth}, Gates: {self.gates}\n"
                   f"  Gate Types: {self.gate_types}\n"
                   f"  Est. Time: {self.estimated_execution_time:.3f}s")
        else:
            return (f"✗ Invalid Circuit\n"
                   f"  Errors: {', '.join(self.errors)}\n"
                   f"  Hash: {self.circuit_hash[:16]}...")


@dataclass
class HealthStatus:
    """Health status of the validation service"""
    status: str
    timestamp: datetime
    version: str
    
    def __str__(self) -> str:
        return f"Status: {self.status}, Version: {self.version}, Time: {self.timestamp}"


class ValidationClient:
    """Client for the QiskitOperator Validation Service"""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """
        Initialize the validation client
        
        Args:
            base_url: Base URL of the validation service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def health(self) -> HealthStatus:
        """
        Check the health of the validation service
        
        Returns:
            HealthStatus object
            
        Raises:
            requests.RequestException: If the request fails
        """
        response = self.session.get(
            f"{self.base_url}/health",
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        
        return HealthStatus(
            status=data['status'],
            timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            version=data['version']
        )
    
    def is_healthy(self) -> bool:
        """
        Check if the service is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            health = self.health()
            return health.status == "healthy"
        except Exception:
            return False
    
    def validate_circuit(
        self,
        code: str,
        backend_name: Optional[str] = None,
        optimization_level: int = 1
    ) -> ValidationResult:
        """
        Validate a Qiskit quantum circuit
        
        Args:
            code: Qiskit Python circuit code
            backend_name: Optional target backend name
            optimization_level: Optimization level (0-3)
            
        Returns:
            ValidationResult object
            
        Raises:
            requests.RequestException: If the request fails
        """
        payload = {
            "code": code,
            "optimization_level": optimization_level
        }
        
        if backend_name:
            payload["backend_name"] = backend_name
        
        response = self.session.post(
            f"{self.base_url}/validate",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        
        return ValidationResult(
            valid=data['valid'],
            circuit_hash=data['circuit_hash'],
            depth=data.get('depth', 0),
            qubits=data.get('qubits', 0),
            gates=data.get('gates', 0),
            gate_types=data.get('gate_types', {}),
            estimated_execution_time=data.get('estimated_execution_time', 0.0),
            errors=data.get('errors', []),
            warnings=data.get('warnings', [])
        )
    
    def validate_circuit_file(
        self,
        file_path: str,
        backend_name: Optional[str] = None,
        optimization_level: int = 1
    ) -> ValidationResult:
        """
        Validate a Qiskit quantum circuit from a file
        
        Args:
            file_path: Path to file containing Qiskit circuit code
            backend_name: Optional target backend name
            optimization_level: Optimization level (0-3)
            
        Returns:
            ValidationResult object
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            requests.RequestException: If the request fails
        """
        with open(file_path, 'r') as f:
            code = f.read()
        
        return self.validate_circuit(
            code=code,
            backend_name=backend_name,
            optimization_level=optimization_level
        )
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage
if __name__ == "__main__":
    # Create client
    client = ValidationClient("http://localhost:8000")
    
    # Check health
    try:
        health = client.health()
        print(f"Service Health: {health}")
        print()
    except Exception as e:
        print(f"Service is not available: {e}")
        exit(1)
    
    # Example 1: Valid circuit
    print("=" * 60)
    print("Example 1: Valid Bell State Circuit")
    print("=" * 60)
    
    bell_circuit = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])"""
    
    result = client.validate_circuit(bell_circuit)
    print(result)
    print()
    
    # Example 2: Circuit with error
    print("=" * 60)
    print("Example 2: Circuit with Runtime Error")
    print("=" * 60)
    
    error_circuit = """from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(5)"""  # Qubit 5 doesn't exist
    
    result = client.validate_circuit(error_circuit)
    print(result)
    print()
    
    # Example 3: Complex circuit with backend
    print("=" * 60)
    print("Example 3: GHZ State with Backend Check")
    print("=" * 60)
    
    ghz_circuit = """from qiskit import QuantumCircuit
qc = QuantumCircuit(4, 4)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.measure([0, 1, 2, 3], [0, 1, 2, 3])"""
    
    result = client.validate_circuit(
        ghz_circuit,
        backend_name="ibmq_qasm_simulator",
        optimization_level=2
    )
    print(result)
    
    # Close the client
    client.close()

