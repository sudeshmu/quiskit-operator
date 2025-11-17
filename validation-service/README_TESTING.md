# Testing the QiskitOperator Validation Service

This guide explains how to test the Validation Service in various ways.

## Quick Start

The easiest way to test is using the provided Makefile:

```bash
# Show all available commands
make help

# Quick test with Python
make install    # Install dependencies
make run        # In terminal 1: Start the service
make test       # In terminal 2: Run tests

# Quick test with Docker
make docker-test  # Build, run, and test in one command
```

---

## Testing Methods

### 1. Local Python Testing

**Prerequisites:**
- Python 3.11+
- pip

**Steps:**

```bash
cd /Users/sudeshmu/work/temps/cirqKube/qiskit-operator/validation-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

The service will start on `http://localhost:8000`. You can now test it.

### 2. Docker Testing

**Prerequisites:**
- Docker installed and running

**Steps:**

```bash
cd /Users/sudeshmu/work/temps/cirqKube/qiskit-operator/validation-service

# Build the image
docker build -t qiskit-validation-service:test .

# Run the container
docker run -p 8000:8000 qiskit-validation-service:test

# Check the image size
docker images qiskit-validation-service:test
```

Expected image size: < 500MB

### 3. Automated Testing

#### Option A: Python Test Suite (Recommended)

Comprehensive test suite with colored output:

```bash
# Install test dependencies
pip install requests

# Run the test suite
python test_validation_service.py
```

This will test:
- ✓ Health and root endpoints
- ✓ Valid circuit validation
- ✓ Syntax error detection
- ✓ Runtime error detection
- ✓ Missing circuit detection
- ✓ Complex circuit analysis
- ✓ Large circuit warnings

#### Option B: Bash/curl Tests

Simple shell script using curl:

```bash
# Run the bash test script
./test_examples.sh
```

### 4. Manual Testing with curl

Test individual endpoints manually:

```bash
# Health check
curl http://localhost:8000/health

# Validate a simple Bell state circuit
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure([0, 1], [0, 1])",
    "optimization_level": 1
  }' | python3 -m json.tool

# Test with syntax error
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2\n",
    "optimization_level": 1
  }' | python3 -m json.tool

# Test with backend specification
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(5)\nfor i in range(5):\n    qc.h(i)",
    "backend_name": "ibmq_qasm_simulator",
    "optimization_level": 2
  }' | python3 -m json.tool
```

### 5. Interactive API Documentation

Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly in your browser.

---

## Testing in Kubernetes

If you want to test the validation service as part of the full QiskitOperator in Kubernetes:

```bash
# Build and load image to minikube (if using minikube)
eval $(minikube docker-env)
docker build -t qiskit-validation-service:latest .

# Deploy to Kubernetes
kubectl apply -f validation-service-deployment.yaml

# Port forward to access locally
kubectl port-forward svc/validation-service 8000:8000

# Run tests against the Kubernetes deployment
python test_validation_service.py
```

---

## Expected Test Results

### Successful Validation Response

```json
{
  "valid": true,
  "circuit_hash": "a1b2c3d4e5f6...",
  "depth": 2,
  "qubits": 2,
  "gates": 3,
  "gate_types": {
    "h": 1,
    "cx": 1,
    "measure": 2
  },
  "estimated_execution_time": 0.23,
  "errors": [],
  "warnings": []
}
```

### Error Response (Syntax Error)

```json
{
  "valid": false,
  "circuit_hash": "a1b2c3d4e5f6...",
  "depth": 0,
  "qubits": 0,
  "gates": 0,
  "gate_types": {},
  "estimated_execution_time": 0.0,
  "errors": [
    "Python syntax error at line 2: invalid syntax"
  ],
  "warnings": []
}
```

---

## Performance Testing

To test the service under load:

```bash
# Install Apache Bench or use it if already installed
# macOS: brew install apache-bench
# Linux: sudo apt-get install apache2-utils

# Run a simple load test (100 requests, 10 concurrent)
ab -n 100 -c 10 -p test_payload.json -T application/json http://localhost:8000/validate
```

Create `test_payload.json`:
```json
{
  "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0, 1)",
  "optimization_level": 1
}
```

---

## Troubleshooting

### Service won't start

1. Check if port 8000 is already in use:
   ```bash
   lsof -i :8000
   ```

2. Try a different port:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

### Tests fail with connection error

1. Ensure the service is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check Docker container logs:
   ```bash
   docker logs qiskit-validation-test
   ```

### Qiskit import errors

If running locally without Docker, ensure Qiskit is installed:
```bash
pip install qiskit==1.0.0 qiskit-ibm-runtime==0.18.0
```

### Docker image too large

Check the image size:
```bash
docker images qiskit-validation-service:test
```

If > 500MB, the image may need optimization. Check the layers:
```bash
docker history qiskit-validation-service:test
```

---

## CI/CD Integration

For automated testing in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Test Validation Service
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t qiskit-validation-service:test validation-service/
      
      - name: Start service
        run: docker run -d -p 8000:8000 qiskit-validation-service:test
      
      - name: Wait for service
        run: sleep 10
      
      - name: Run tests
        run: |
          pip install requests
          python validation-service/test_validation_service.py
```

---

## Next Steps

After testing the validation service:

1. **Integration Testing**: Test with the QiskitJob controller
2. **E2E Testing**: Full workflow from job submission to completion
3. **Performance Tuning**: Optimize for production workloads
4. **Monitoring**: Add Prometheus metrics and Grafana dashboards

See the main QiskitOperator documentation for more information.

