# Qiskit Kubernetes Operator

A production-ready Kubernetes Operator for managing quantum computing workloads using Qiskit. Deploy and manage quantum circuits across multiple quantum backends (IBM Quantum, AWS Braket, local simulators) directly from Kubernetes.

## 🚀 Quick Start

```bash
# Pull the controller image
docker pull sudeshmu/qiskit-operator:controller-latest

# Pull the validation service image
docker pull sudeshmu/qiskit-operator:validation-latest
```

## 📦 Available Images

### 1. Controller Image
**`sudeshmu/qiskit-operator:controller-latest`**

The main Kubernetes operator controller that manages quantum computing resources.

- **Size**: ~15-20 MB
- **Base**: Distroless (secure, minimal)
- **Platforms**: linux/amd64, linux/arm64
- **Use Case**: Kubernetes controller deployment

```bash
docker run sudeshmu/qiskit-operator:controller-latest
```

### 2. Validation Service Image
**`sudeshmu/qiskit-operator:validation-latest`**

FastAPI-based service for validating and analyzing Qiskit quantum circuits.

- **Size**: ~1.3 GB (includes Qiskit, NumPy, SciPy)
- **Base**: Python 3.11 Slim
- **Platforms**: linux/amd64, linux/arm64
- **Ports**: 8000
- **Use Case**: Circuit validation and analysis

```bash
docker run -p 8000:8000 sudeshmu/qiskit-operator:validation-latest
```

## 🏗️ Architecture Support

Both images are **multi-platform** and automatically work on:

| Platform | Architecture | Examples |
|----------|-------------|----------|
| `linux/amd64` | x86_64 Intel/AMD | Most cloud instances, servers |
| `linux/arm64` | ARM64 | Apple Silicon M1/M2/M3, AWS Graviton, Raspberry Pi 4 |

Docker and Kubernetes automatically detect your architecture and pull the correct variant.

## 🎯 Features

- **Multi-Backend Support**: IBM Quantum, AWS Braket, Local Simulators
- **Resource Management**: Quota tracking, cost estimation, session management
- **Circuit Validation**: Pre-flight checks before quantum execution
- **Kubernetes Native**: CRDs for Jobs, Backends, Sessions, Budgets
- **Production Ready**: Security, monitoring, RBAC built-in
- **Cost Optimization**: Budget controls and cost tracking

## 📋 Kubernetes Custom Resources

```yaml
# QiskitJob - Execute quantum circuits
apiVersion: quantum.quantum.io/v1
kind: QiskitJob
metadata:
  name: my-quantum-job
spec:
  backend:
    name: ibm_brisbane
    provider: ibm
  circuit:
    inline: |
      from qiskit import QuantumCircuit
      qc = QuantumCircuit(2)
      qc.h(0)
      qc.cx(0, 1)
      qc.measure_all()
  shots: 1024
```

## 🚢 Kubernetes Deployment

### Deploy the Operator

```bash
# Install CRDs
kubectl apply -f https://raw.githubusercontent.com/your-repo/qiskit-operator/main/config/crd/bases/

# Deploy operator
kubectl create namespace qiskit-system
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qiskit-operator
  namespace: qiskit-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: qiskit-operator
  template:
    metadata:
      labels:
        app: qiskit-operator
    spec:
      containers:
      - name: manager
        image: sudeshmu/qiskit-operator:controller-latest
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
EOF
```

### Deploy Validation Service

```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qiskit-validation
  namespace: qiskit-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: qiskit-validation
  template:
    metadata:
      labels:
        app: qiskit-validation
    spec:
      containers:
      - name: validation
        image: sudeshmu/qiskit-operator:validation-latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: qiskit-validation
  namespace: qiskit-system
spec:
  selector:
    app: qiskit-validation
  ports:
  - port: 8000
    targetPort: 8000
EOF
```

## 🧪 Testing the Validation Service

```bash
# Test circuit validation
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "circuit_code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0,1)"
  }'
```

## 🔧 Configuration

### Environment Variables (Controller)

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_WEBHOOKS` | Enable admission webhooks | `false` |
| `METRICS_ADDR` | Metrics endpoint | `:8080` |
| `HEALTH_PROBE_ADDR` | Health probe endpoint | `:8081` |

### Environment Variables (Validation Service)

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Service port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔐 Security

- **Non-root**: Both images run as non-root users
- **Distroless**: Controller uses minimal distroless base
- **No secrets in images**: Configure secrets via Kubernetes
- **RBAC**: Fine-grained permissions

## 📊 Resource Requirements

### Controller
- **CPU**: 100m-500m
- **Memory**: 128Mi-256Mi
- **Storage**: None required

### Validation Service
- **CPU**: 500m-2000m (circuit validation is CPU-intensive)
- **Memory**: 512Mi-2Gi (depends on circuit complexity)
- **Storage**: None required

## 🏷️ Tags

### Controller Tags
- `controller-latest` - Latest stable release
- `controller-v0.1.0` - Specific version
- `latest` - Alias for controller-latest

### Validation Service Tags
- `validation-latest` - Latest stable release
- `validation-v0.1.0` - Specific version

## 🌟 Use Cases

1. **Quantum Research**: Run quantum experiments at scale
2. **Algorithm Development**: Test quantum algorithms across multiple backends
3. **Education**: Teach quantum computing with Kubernetes
4. **Hybrid Applications**: Integrate quantum processing into classical workflows
5. **Cost Management**: Track and control quantum computing costs

## 🔗 Links

- **GitHub**: [github.com/sudeshmu/qiskit-operator](https://github.com/sudeshmu/qiskit-operator) *(update with your repo)*
- **Documentation**: Full operator documentation
- **Issues**: Report bugs or request features
- **Qiskit**: [qiskit.org](https://qiskit.org)

## 📝 Examples

### Bell State Circuit

```yaml
apiVersion: quantum.quantum.io/v1
kind: QiskitJob
metadata:
  name: bell-state
spec:
  backend:
    name: ibm_simulator
    provider: ibm
  circuit:
    inline: |
      from qiskit import QuantumCircuit
      qc = QuantumCircuit(2, 2)
      qc.h(0)
      qc.cx(0, 1)
      qc.measure([0, 1], [0, 1])
  shots: 1024
```

### Grover's Algorithm

```yaml
apiVersion: quantum.quantum.io/v1
kind: QiskitJob
metadata:
  name: grover-search
spec:
  backend:
    name: ibm_kyoto
    provider: ibm
  circuit:
    configMapRef:
      name: grover-circuit
      key: circuit.py
  shots: 8192
  optimization_level: 3
```

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

Apache License 2.0

## 🙏 Acknowledgments

- Built with [Kubebuilder](https://kubebuilder.io/)
- Powered by [Qiskit](https://qiskit.org)
- Inspired by the quantum computing community

---

**Need help?** Open an issue on GitHub or check our documentation.

**⭐ Star us on GitHub** if you find this useful!

