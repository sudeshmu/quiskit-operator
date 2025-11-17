# Getting Started with QiskitOperator

This guide walks you through deploying and testing the QiskitOperator.

## 🎯 Prerequisites

- Kubernetes cluster (Kind, Minikube, or production cluster)
- kubectl configured
- Docker installed
- Go 1.21+ (for building from source)

## 🚀 Quick Start

### Option A: Local Development with Kind

#### 1. Create Kind Cluster

```bash
# Install Kind if you haven't
# brew install kind  # macOS
# or follow: https://kind.sigs.k8s.io/docs/user/quick-start/

# Create cluster
kind create cluster --name qiskit-operator-dev
```

#### 2. Build Executor Image

```bash
cd execution-pods

# Build Docker image
docker build -t qiskit-executor:v1 .

# Load into Kind cluster
kind load docker-image qiskit-executor:v1 --name qiskit-operator-dev
```

#### 3. Install CRDs and Run Operator

```bash
cd ..

# Install CRDs
make install

# Run operator locally (connects to Kind cluster)
make run
```

**Note**: Keep this terminal open - the operator is now running!

#### 4. Submit Your First Quantum Job

Open a new terminal:

```bash
# Apply the example job
kubectl apply -f config/samples/example-local-simulator.yaml

# Watch the job progress
kubectl get qiskitjob bell-state-example -w
```

You'll see:
```
NAME                  PHASE        BACKEND           COST     AGE
bell-state-example   Pending      local_simulator   $0.00    1s
bell-state-example   Validating   local_simulator   $0.00    2s
bell-state-example   Scheduling   local_simulator   $0.00    3s
bell-state-example   Running      local_simulator   $0.00    4s
bell-state-example   Completed    local_simulator   $0.00    25s
```

#### 5. View Results

```bash
# Get the results ConfigMap
kubectl get configmap bell-state-results -o yaml

# View execution pod logs
kubectl logs qiskit-job-bell-state-example

# Get detailed job status
kubectl describe qiskitjob bell-state-example
```

---

### Option B: Deploy to Existing Cluster

#### 1. Build and Push Images

```bash
# Build execution pod image
cd execution-pods
docker build -t YOUR_REGISTRY/qiskit-executor:v1 .
docker push YOUR_REGISTRY/qiskit-executor:v1

# Build operator image
cd ..
make docker-build IMG=YOUR_REGISTRY/qiskit-operator:v1
make docker-push IMG=YOUR_REGISTRY/qiskit-operator:v1
```

#### 2. Deploy Operator

```bash
# Install CRDs
make install

# Deploy operator
make deploy IMG=YOUR_REGISTRY/qiskit-operator:v1
```

#### 3. Submit Jobs

```bash
kubectl apply -f config/samples/example-local-simulator.yaml
kubectl get qiskitjobs -w
```

---

## 📝 Example Quantum Jobs

### Bell State (Simple)

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: bell-state
spec:
  backend:
    type: local_simulator
  
  circuit:
    source: inline
    code: |
      from qiskit import QuantumCircuit
      qc = QuantumCircuit(2, 2)
      qc.h(0)
      qc.cx(0, 1)
      qc.measure([0, 1], [0, 1])
  
  execution:
    shots: 1024
  
  output:
    type: configmap
    location: bell-state-results
```

### GHZ State (3 Qubits)

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: ghz-state
spec:
  backend:
    type: local_simulator
  
  circuit:
    source: inline
    code: |
      from qiskit import QuantumCircuit
      qc = QuantumCircuit(3, 3)
      qc.h(0)
      qc.cx(0, 1)
      qc.cx(0, 2)
      qc.measure([0, 1, 2], [0, 1, 2])
  
  execution:
    shots: 2048
    optimizationLevel: 2
  
  output:
    type: configmap
    location: ghz-results
```

### Quantum Fourier Transform

```yaml
apiVersion: quantum.io/v1
kind: QiskitJob
metadata:
  name: qft-example
spec:
  backend:
    type: local_simulator
  
  circuit:
    source: inline
    code: |
      from qiskit import QuantumCircuit
      import numpy as np
      
      def qft(n):
          qc = QuantumCircuit(n, n)
          for j in range(n):
              qc.h(j)
              for k in range(j+1, n):
                  qc.cp(np.pi/2**(k-j), k, j)
          for j in range(n//2):
              qc.swap(j, n-j-1)
          return qc
      
      qc = qft(4)
      qc.measure_all()
  
  execution:
    shots: 1024
    optimizationLevel: 3
  
  output:
    type: configmap
    location: qft-results
```

---

## 🔍 Monitoring and Debugging

### Check Operator Logs

```bash
# If running locally
# Logs are in your terminal where you ran `make run`

# If deployed
kubectl logs -n qiskit-operator-system deployment/qiskit-operator-controller -f
```

### Check Job Status

```bash
# List all jobs
kubectl get qiskitjobs

# Get detailed status
kubectl describe qiskitjob <job-name>

# Watch for changes
kubectl get qiskitjob <job-name> -w
```

### Check Execution Pod

```bash
# List pods
kubectl get pods -l app=qiskit-operator

# View pod logs
kubectl logs <pod-name>

# Describe pod
kubectl describe pod <pod-name>
```

### Check Results

```bash
# List result ConfigMaps
kubectl get configmaps -l app=qiskit-operator

# View results
kubectl get configmap <results-name> -o yaml
```

---

## 🐛 Troubleshooting

### Job Stuck in Pending

```bash
# Check operator logs
kubectl logs -n qiskit-operator-system deployment/qiskit-operator-controller

# Check CRD is installed
kubectl get crd qiskitjobs.quantum.quantum.io

# Check RBAC permissions
kubectl auth can-i create pods
```

### Pod Fails to Start

```bash
# Check pod events
kubectl describe pod qiskit-job-<name>

# Check if image is available
kubectl get pod qiskit-job-<name> -o jsonpath='{.spec.containers[0].image}'

# For Kind, ensure image is loaded
kind load docker-image qiskit-executor:v1 --name qiskit-operator-dev
```

### Circuit Execution Fails

```bash
# View executor logs
kubectl logs qiskit-job-<name>

# Check circuit code syntax
# Ensure you're using valid Qiskit syntax

# Verify Qiskit version compatibility
# Operator uses Qiskit 1.0.0
```

---

## 🧹 Cleanup

### Delete Jobs

```bash
# Delete a specific job
kubectl delete qiskitjob bell-state-example

# Delete all jobs
kubectl delete qiskitjobs --all
```

### Uninstall Operator

```bash
# If running locally: Ctrl+C to stop

# If deployed
make undeploy

# Remove CRDs
make uninstall
```

### Delete Kind Cluster

```bash
kind delete cluster --name qiskit-operator-dev
```

---

## 📚 Next Steps

1. **Try More Examples**: Create your own quantum circuits
2. **Explore Options**: Configure shots, optimization levels
3. **Read the Docs**: Check out `README.md` for full documentation
4. **Contribute**: Found a bug? Submit a PR!

---

## 🆘 Getting Help

- **Documentation**: [README.md](README.md)
- **GitHub Issues**: https://github.com/quantum-operator/qiskit-operator/issues
- **Slack**: https://quantum-operator.slack.com

---

## 🎉 Success!

If you've made it here and executed your first quantum circuit on Kubernetes, congratulations! You're now running one of the first production-ready quantum computing operators.

**Welcome to the cloud-native quantum revolution!** 🚀

