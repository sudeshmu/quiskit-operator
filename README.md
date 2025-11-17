# QiskitOperator

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Go Report Card](https://goreportcard.com/badge/github.com/quantum-operator/qiskit-operator)](https://goreportcard.com/report/github.com/quantum-operator/qiskit-operator)

**QiskitOperator** is a production-ready Kubernetes operator for IBM Qiskit quantum computing workloads. It brings quantum computing into the cloud-native world with enterprise-grade reliability, security, and cost management.

## 🌟 Key Features

- **🔧 Kubernetes-Native**: Custom Resource Definitions (CRDs) for quantum jobs, backends, budgets, and sessions
- **🔐 Multi-Backend Support**: IBM Quantum Platform, AWS Braket, and local simulators
- **💰 Cost Management**: Intelligent backend selection with budget enforcement and cost optimization
- **🛡️ Enterprise Security**: RBAC, Pod Security Standards, secret management, and audit logging
- **📊 Observability**: Prometheus metrics and Grafana dashboards out of the box
- **🚀 Production Ready**: Designed for 99.9% uptime with comprehensive error handling and retry logic

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Custom Resources](#custom-resources)
- [Examples](#examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

QiskitOperator consists of several key components:

- **Operator Controller (Go)**: Manages quantum job lifecycle and reconciliation
- **Validation Service (Python)**: Validates circuit syntax and analyzes circuit properties
- **Backend Managers**: Abstractions for IBM Quantum, AWS Braket, and local simulators
- **Cost Manager**: Tracks spending and enforces budget constraints
- **Storage Manager**: Handles result persistence across PVC, S3, GCS

```
┌─────────────────────────────────────────────────────────┐
│ QiskitOperator Controller (Go)                          │
│ ┌─────────────────────────────────────────────────┐    │
│ │ Reconciliation Loop                              │    │
│ │ - Job validation                                 │    │
│ │ - Backend selection                              │    │
│ │ - Pod creation                                   │    │
│ └──────────────┬──────────────────────────────────┘    │
└────────────────┼──────────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Python Validation Service                                │
│ - Circuit syntax validation                              │
│ - Circuit metrics extraction                             │
│ - Backend compatibility checking                         │
└─────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Quantum Backends                                         │
│ - IBM Quantum Platform                                   │
│ - AWS Braket                                            │
│ - Local Simulators (Qiskit Aer)                         │
└─────────────────────────────────────────────────────────┘
```

## 📦 Prerequisites

- Kubernetes 1.24+
- Go 1.21+ (for development)
- Docker or Podman (for building images)
- kubectl configured for your cluster
- (Optional) IBM Quantum account with API key

## ⚙️ Installation

### Using Helm (Recommended)

```bash
# Add the QiskitOperator Helm repository
helm repo add qiskit-operator https://quantum-operator.github.io/qiskit-operator
helm repo update

# Install the operator
helm install qiskit-operator qiskit-operator/qiskit-operator \
  --namespace qiskit-operator-system \
  --create-namespace
```

### Using kubectl

```bash
# Install CRDs
kubectl apply -f config/crd/bases/

# Install the operator
kubectl apply -f config/manager/manager.yaml
```

### From Source

```bash
# Clone the repository
git clone https://github.com/quantum-operator/qiskit-operator
cd qiskit-operator

# Build and install
make manifests
make install

# Run locally (for development)
make run
```

## 🚀 Quick Start

### 1. Create IBM Quantum Credentials Secret

```bash
kubectl create secret generic ibm-quantum-credentials \
  --from-literal=api-key=YOUR_IBM_QUANTUM_API_KEY \
  --namespace default
```

### 2. Submit Your First Quantum Job

Create a file named `hello-quantum.yaml`:

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: hello-quantum
spec:
  backend:
    type: local_simulator
  
  circuit:
    source: inline
    code: |
      from qiskit import QuantumCircuit
      
      # Create a simple Bell state
      qc = QuantumCircuit(2, 2)
      qc.h(0)
      qc.cx(0, 1)
      qc.measure([0, 1], [0, 1])
  
  execution:
    shots: 1024
    optimizationLevel: 1
  
  output:
    type: configmap
    location: hello-quantum-results
```

Apply it:

```bash
kubectl apply -f hello-quantum.yaml
```

### 3. Check Job Status

```bash
# List quantum jobs
kubectl get qiskitjobs

# Get detailed status
kubectl describe qiskitjob hello-quantum

# View results
kubectl get configmap hello-quantum-results -o yaml
```

## 📚 Custom Resources

### QiskitJob

Represents a quantum circuit execution job.

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: my-quantum-job
spec:
  backend:
    type: ibm_quantum           # ibm_quantum | local_simulator | aws_braket
    name: ibm_brisbane          # Specific backend name
    instance: crn:v1:bluemix... # IBM Cloud CRN (enterprise)
  
  circuit:
    source: inline              # inline | configmap | url | git
    code: |
      from qiskit import QuantumCircuit
      qc = QuantumCircuit(2)
      qc.h(0)
      qc.cx(0, 1)
      qc.measure_all()
  
  execution:
    shots: 1024
    optimizationLevel: 3
    priority: normal            # low | normal | high | urgent
  
  budget:
    maxCost: "$10.00"
    costCenter: quantum-research
  
  output:
    type: pvc                   # pvc | s3 | gcs | configmap
    location: quantum-results
    format: json                # json | pickle | qpy | csv
  
  credentials:
    secretRef:
      name: ibm-quantum-credentials
```

### QiskitBackend

Represents a quantum backend configuration.

### QiskitBudget

Manages cost constraints and quotas per namespace.

### QiskitSession

Manages IBM Quantum Runtime sessions for iterative algorithms.

## 💡 Examples

### Cost-Optimized Job

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: cost-sensitive-job
spec:
  backend:
    type: ibm_quantum
  
  backendSelection:
    weights:
      cost: 0.70          # Prioritize cost
      queueTime: 0.20
      capability: 0.05
      availability: 0.05
    fallbackToSimulator: true
  
  budget:
    maxCost: "$5.00"
  # ... rest of spec
```

### VQE Algorithm with Session

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: vqe-optimization
spec:
  backend:
    type: ibm_quantum
    name: ibm_brisbane
  
  session:
    name: vqe-session
    maxTime: 3600       # 1 hour
    mode: dedicated     # Lock QPU for exclusive access
  
  circuit:
    source: git
    gitRef:
      repository: https://github.com/your-org/quantum-algorithms
      branch: main
      path: vqe/h2_molecule.py
  # ... rest of spec
```

## 🛠️ Development

### Project Structure

```
qiskit-operator/
├── api/v1/                     # CRD type definitions
│   ├── qiskitjob_types.go
│   ├── qiskitbackend_types.go
│   ├── qiskitbudget_types.go
│   └── qiskitsession_types.go
├── internal/controller/        # Reconciliation logic
│   ├── qiskitjob_controller.go
│   └── ...
├── pkg/
│   ├── backend/               # Backend implementations
│   │   ├── ibm/              # IBM Quantum backend
│   │   ├── aws/              # AWS Braket backend
│   │   └── local/            # Local simulator
│   ├── cost/                  # Cost management
│   ├── storage/               # Storage abstraction
│   ├── metrics/               # Observability
│   └── validation/            # Circuit validation
├── validation-service/        # Python validation service
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── config/                    # Kubernetes manifests
│   ├── crd/bases/            # Generated CRDs
│   ├── manager/              # Operator deployment
│   └── rbac/                 # RBAC configuration
└── charts/                   # Helm chart
```

### Building from Source

```bash
# Generate manifests
make manifests

# Generate code
make generate

# Run tests
make test

# Build Docker image
make docker-build IMG=your-registry/qiskit-operator:tag

# Push Docker image
make docker-push IMG=your-registry/qiskit-operator:tag
```

### Running Tests

```bash
# Unit tests
make test

# Integration tests
make test-integration

# E2E tests (requires Kind cluster)
make test-e2e
```

### Validation Service Development

```bash
cd validation-service

# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test the service
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0,1)",
    "backend_name": "ibm_brisbane",
    "optimization_level": 1
  }'
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Copyright 2025 Quantum Operator Team.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## 🌐 Community & Support

- **Documentation**: [https://docs.quantum-operator.io](https://docs.quantum-operator.io)
- **GitHub Issues**: [https://github.com/quantum-operator/qiskit-operator/issues](https://github.com/quantum-operator/qiskit-operator/issues)
- **Slack Community**: [Join our Slack](https://quantum-operator.slack.com)
- **Discussions**: [GitHub Discussions](https://github.com/quantum-operator/qiskit-operator/discussions)

## 🎯 Roadmap

- [x] MVP with local simulator support
- [x] IBM Quantum Platform integration
- [x] Circuit validation service
- [ ] AWS Braket backend
- [ ] Cost optimization ML model
- [ ] Argo Workflows integration
- [ ] Tekton Pipeline integration
- [ ] OperatorHub certification
- [ ] Azure Quantum backend

## 💬 Acknowledgments

- IBM Qiskit team for their excellent quantum computing framework
- Kubernetes community for the operator framework
- All contributors who help make quantum computing more accessible

---

**Built with ❤️ by the Quantum Operator Team**

*Making quantum computing cloud-native, one operator at a time*
