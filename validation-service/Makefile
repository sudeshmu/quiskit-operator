# Makefile for QiskitOperator Validation Service
# Provides convenient commands for development and testing

.PHONY: help install run test test-bash docker-build docker-run docker-test clean

# Default target
help:
	@echo "QiskitOperator Validation Service - Make Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install      - Install Python dependencies in venv"
	@echo "  make run          - Run service locally (development mode)"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run Python test suite"
	@echo "  make test-bash    - Run bash/curl test examples"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-test  - Build and test Docker container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove temporary files and venv"

# Python virtual environment setup
venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip

# Install dependencies
install: venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "✓ Dependencies installed!"
	@echo "To activate: source venv/bin/activate"

# Run the service locally
run:
	@echo "Starting validation service on http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@if [ -d "venv" ]; then \
		. venv/bin/activate && python main.py; \
	else \
		python3 main.py; \
	fi

# Run Python test suite
test:
	@echo "Running Python test suite..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate && pip install -q requests && python test_validation_service.py; \
	else \
		pip3 install -q requests && python3 test_validation_service.py; \
	fi

# Run bash/curl tests
test-bash:
	@echo "Running bash test examples..."
	./test_examples.sh

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	docker build -t qiskit-validation-service:test .
	@echo ""
	@echo "✓ Docker image built: qiskit-validation-service:test"
	@echo ""
	@docker images qiskit-validation-service:test

# Run Docker container
docker-run:
	@echo "Starting Docker container on http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	docker run --rm -p 8000:8000 --name qiskit-validation-test qiskit-validation-service:test

# Build and test Docker container
docker-test: docker-build
	@echo ""
	@echo "Starting Docker container in background..."
	@docker run -d --rm -p 8000:8000 --name qiskit-validation-test qiskit-validation-service:test
	@echo "Waiting for service to be ready..."
	@sleep 5
	@echo ""
	@echo "Running tests..."
	@$(MAKE) test-bash || (docker stop qiskit-validation-test && exit 1)
	@echo ""
	@echo "Stopping Docker container..."
	@docker stop qiskit-validation-test
	@echo "✓ Docker tests passed!"

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf venv __pycache__ *.pyc .pytest_cache
	@docker stop qiskit-validation-test 2>/dev/null || true
	@echo "✓ Cleanup complete"

# Install test dependencies
install-test-deps:
	@if [ -d "venv" ]; then \
		. venv/bin/activate && pip install requests pytest pytest-cov httpx; \
	else \
		pip3 install requests pytest pytest-cov httpx; \
	fi

