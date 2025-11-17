# QiskitOperator Execution Pod Dockerfile
#
# This image contains Qiskit and executes quantum circuits
# Target size: < 500MB

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Qiskit
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Qiskit and required packages
RUN pip install --no-cache-dir \
    qiskit==1.0.0 \
    qiskit-aer==0.13.0 \
    numpy==1.24.3

# Copy executor script
COPY executor.py /app/executor.py
RUN chmod +x /app/executor.py

# Create results directory
RUN mkdir -p /results && chmod 777 /results

# Create non-root user for security
RUN useradd -m -u 1000 qiskit && chown -R qiskit:qiskit /app /results
USER qiskit

# Set Python to unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python3", "/app/executor.py"]

