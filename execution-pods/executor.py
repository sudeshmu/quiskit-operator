#!/usr/bin/env python3
"""
QiskitOperator Quantum Circuit Executor

This script executes quantum circuits using Qiskit Aer simulator.
It's designed to run in a Kubernetes pod as part of the QiskitOperator.

Copyright 2025 Quantum Operator Team.
Licensed under the Apache License, Version 2.0.
"""

import os
import sys
import json
import time
from datetime import datetime


def main():
    """Main execution function"""
    print("=" * 60)
    print("QiskitOperator Circuit Executor")
    print("=" * 60)
    
    # Get circuit code from environment
    circuit_code = os.getenv('CIRCUIT_CODE', '')
    shots = int(os.getenv('SHOTS', '1024'))
    optimization_level = int(os.getenv('OPTIMIZATION_LEVEL', '1'))
    
    if not circuit_code:
        print("ERROR: CIRCUIT_CODE environment variable is required")
        sys.exit(1)
    
    print(f"\nConfiguration:")
    print(f"  Shots: {shots}")
    print(f"  Optimization Level: {optimization_level}")
    print(f"  Circuit Code Length: {len(circuit_code)} chars")
    print()
    
    try:
        # Import Qiskit
        print("Importing Qiskit libraries...")
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        print("✓ Qiskit imported successfully")
        
        # Execute circuit code to create the circuit
        print("\nCreating quantum circuit...")
        local_vars = {}
        global_vars = {
            '__builtins__': __builtins__,
            'QuantumCircuit': QuantumCircuit,
        }
        
        exec(circuit_code, global_vars, local_vars)
        
        # Find the circuit object
        circuit = None
        for var in local_vars.values():
            if isinstance(var, QuantumCircuit):
                circuit = var
                break
        
        if circuit is None:
            print("ERROR: No QuantumCircuit object found in code")
            sys.exit(1)
        
        print(f"✓ Circuit created: {circuit.num_qubits} qubits, {circuit.depth()} depth")
        
        # Create simulator
        print("\nInitializing Aer simulator...")
        simulator = AerSimulator()
        print("✓ Simulator initialized")
        
        # Transpile circuit
        print(f"\nTranspiling circuit (optimization level {optimization_level})...")
        start_transpile = time.time()
        transpiled_circuit = transpile(circuit, simulator, optimization_level=optimization_level)
        transpile_time = time.time() - start_transpile
        print(f"✓ Circuit transpiled in {transpile_time:.3f}s")
        print(f"  Transpiled depth: {transpiled_circuit.depth()}")
        
        # Execute circuit
        print(f"\nExecuting circuit with {shots} shots...")
        start_exec = time.time()
        job = simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        exec_time = time.time() - start_exec
        print(f"✓ Execution completed in {exec_time:.3f}s")
        
        # Get counts
        counts = result.get_counts()
        print(f"\nResults:")
        print(f"  Total measurements: {shots}")
        print(f"  Unique outcomes: {len(counts)}")
        print(f"  Top 5 outcomes:")
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for state, count in sorted_counts[:5]:
            probability = count / shots * 100
            print(f"    {state}: {count} ({probability:.2f}%)")
        
        # Create results object
        results = {
            "job_id": os.getenv('JOB_ID', 'unknown'),
            "job_name": os.getenv('JOB_NAME', 'unknown'),
            "backend": "local_simulator",
            "backend_info": {
                "name": "aer_simulator",
                "type": "simulator",
                "version": "0.13.0"
            },
            "execution": {
                "start_time": datetime.utcnow().isoformat() + "Z",
                "transpile_time_seconds": transpile_time,
                "execution_time_seconds": exec_time,
                "total_time_seconds": transpile_time + exec_time
            },
            "circuit": {
                "qubits": circuit.num_qubits,
                "depth": circuit.depth(),
                "transpiled_depth": transpiled_circuit.depth(),
                "gates": len(circuit.data),
                "optimization_level": optimization_level
            },
            "results": {
                "shots": shots,
                "counts": counts,
                "success": True
            },
            "cost": {
                "estimated": "$0.00",
                "actual": "$0.00",
                "currency": "USD"
            }
        }
        
        # Write results to file
        results_file = "/results/results.json"
        os.makedirs("/results", exist_ok=True)
        
        print(f"\nWriting results to {results_file}...")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print("✓ Results written successfully")
        
        # Also print to stdout for logs
        print("\n" + "=" * 60)
        print("RESULTS (JSON):")
        print("=" * 60)
        print(json.dumps(results, indent=2))
        print("=" * 60)
        
        print("\n✓ Circuit execution completed successfully!")
        sys.exit(0)
        
    except ImportError as e:
        print(f"ERROR: Failed to import required libraries: {e}")
        print("Make sure Qiskit is installed: pip install qiskit qiskit-aer")
        sys.exit(1)
    except SyntaxError as e:
        print(f"ERROR: Circuit code has syntax errors: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Circuit execution failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

