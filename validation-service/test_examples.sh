#!/bin/bash
# Test script for QiskitOperator Validation Service
# This script provides example curl commands to test the service

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}QiskitOperator Validation Service Tests${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "Testing service at: ${BLUE}${BASE_URL}${NC}"
echo ""

# Function to print test headers
print_test() {
    echo ""
    echo -e "${BLUE}Testing: $1${NC}"
    echo "---"
}

# Function to check if service is running
check_service() {
    echo -e "${YELLOW}Checking if service is running...${NC}"
    if curl -s "${BASE_URL}/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Service is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Service is not running${NC}"
        echo ""
        echo "Please start the service first:"
        echo "  python main.py"
        echo "  or"
        echo "  docker run -p 8000:8000 qiskit-validation-service:test"
        exit 1
    fi
}

# Check service availability
check_service

# Test 1: Health Check
print_test "Health Check Endpoint"
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo -e "${GREEN}✓ Health check passed${NC}"

# Test 2: Root Endpoint
print_test "Root Endpoint"
curl -s "${BASE_URL}/" | python3 -m json.tool
echo -e "${GREEN}✓ Root endpoint passed${NC}"

# Test 3: Valid Circuit
print_test "Valid Bell State Circuit"
curl -s -X POST "${BASE_URL}/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure([0, 1], [0, 1])",
    "optimization_level": 1
  }' | python3 -m json.tool

echo -e "${GREEN}✓ Valid circuit test passed${NC}"

# Test 4: Syntax Error
print_test "Circuit with Syntax Error"
curl -s -X POST "${BASE_URL}/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2\nqc.h(0",
    "optimization_level": 1
  }' | python3 -m json.tool

echo -e "${GREEN}✓ Syntax error detection passed${NC}"

# Test 5: Runtime Error
print_test "Circuit with Runtime Error"
curl -s -X POST "${BASE_URL}/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(5)",
    "optimization_level": 1
  }' | python3 -m json.tool

echo -e "${GREEN}✓ Runtime error detection passed${NC}"

# Test 6: Complex Circuit
print_test "Complex GHZ State Circuit"
curl -s -X POST "${BASE_URL}/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(4, 4)\nqc.h(0)\nqc.cx(0, 1)\nqc.cx(1, 2)\nqc.cx(2, 3)\nqc.measure([0, 1, 2, 3], [0, 1, 2, 3])",
    "backend_name": "ibmq_qasm_simulator",
    "optimization_level": 2
  }' | python3 -m json.tool

echo -e "${GREEN}✓ Complex circuit test passed${NC}"

# Test 7: Circuit with Backend Check
print_test "Circuit with Backend Compatibility Check"
curl -s -X POST "${BASE_URL}/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from qiskit import QuantumCircuit\nqc = QuantumCircuit(5, 5)\nfor i in range(5):\n    qc.h(i)\nqc.measure_all()",
    "backend_name": "ibm_kyoto",
    "optimization_level": 3
  }' | python3 -m json.tool

echo -e "${GREEN}✓ Backend compatibility test passed${NC}"

# Summary
echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}All tests completed successfully!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

