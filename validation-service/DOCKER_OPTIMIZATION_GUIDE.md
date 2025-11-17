# Docker Image Size Optimization Guide

## Current Image Sizes

| Version | Size | Reduction | Description |
|---------|------|-----------|-------------|
| **Original** | **1.34 GB** | - | Single-stage build with all dependencies |
| **Optimized** | **1.28 GB** | **60 MB (4%)** | Multi-stage build (removes build tools) |
| **Minimal** | **1.20 GB** | **140 MB (10%)** | Without IBM Runtime dependencies |

## Size Breakdown Analysis

The large size is primarily due to:
- **Qiskit Core**: ~120 MB
- **Numpy**: 14.2 MB (but large in memory)
- **Scipy**: 33.6 MB (compiled scientific libraries)
- **Symengine**: 60.9 MB (symbolic computation engine)
- **IBM Cloud SDK** (if using qiskit-ibm-runtime): ~50 MB
- **Python base image**: ~150 MB

## Optimization Strategies

### 1. **Multi-Stage Build (Implemented)** ✅
**Reduction**: 60 MB (4%)

Uses separate build and runtime stages to exclude compilation tools (gcc, g++).

```dockerfile
FROM python:3.11-slim AS builder
RUN apt-get install gcc g++
RUN pip wheel ...

FROM python:3.11-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels -r requirements.txt
```

**File**: `Dockerfile.optimized`

###2. **Remove IBM Runtime Dependencies (Implemented)** ✅
**Reduction**: 140 MB (10%)

For validation-only purposes, you may not need `qiskit-ibm-runtime`:

```txt
# requirements.minimal.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
qiskit==1.0.0  # No IBM runtime
python-multipart==0.0.6
```

**File**: `requirements.minimal.txt`

### 3. **Alpine Linux (Experimental)** ⚠️
**Potential Reduction**: 200-300 MB (15-20%)

Alpine uses musl instead of glibc, resulting in smaller images.

**⚠️ Warning**: Scientific packages (numpy, scipy) may have compatibility issues with Alpine.

**File**: `Dockerfile.alpine`

### 4. **Additional Optimization Strategies** (Not Implemented)

#### A. **Use Distroless Images**
```dockerfile
FROM gcr.io/distroless/python3-debian11
# No shell, package manager - ultra minimal
# Size: ~50MB base instead of ~150MB
```

**Pros**: Smaller, more secure  
**Cons**: No shell for debugging, harder to troubleshoot

#### B. **Use Slim Python Packages**
Replace full packages with lightweight alternatives:
- `numpy-quaternion` instead of full numpy (if you only need specific features)
- Consider `micropython` for extremely minimal Python

**Limitation**: Qiskit requires full numpy/scipy

#### C. **Layer Caching Optimization**
Order Dockerfile instructions from least to most frequently changed:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt  # Cached unless requirements change
COPY main.py .  # Only this layer rebuilds on code changes
```

**Already implemented** in all Dockerfiles.

#### D. **Remove Unused Dependencies**
Audit and remove unused packages:
```bash
# Inside container
pip list
# Remove packages not imported in your code
```

#### E. **Use Docker Build Kit**
Enable BuildKit for better caching and parallel builds:
```bash
DOCKER_BUILDKIT=1 docker build -t image:tag .
```

**Already enabled** by default in newer Docker versions.

## Recommended Approach

### For Production Deployment:
**Use `Dockerfile.optimized` (1.28 GB)**
- Multi-stage build reduces size by removing build tools
- Maintains full compatibility with IBM Quantum
- Best balance of size and functionality

### For Validation-Only Service:
**Use `requirements.minimal.txt` (1.20 GB)**
- Removes IBM Cloud dependencies
- 10% smaller than full version
- Sufficient if you only validate circuits without executing on IBM hardware

### For Maximum Size Reduction:
**Try `Dockerfile.alpine` (experimental)**
- Can reduce to 300-500 MB potentially
- **Test thoroughly** before production use
- Scientific packages may have issues

## Why Can't We Reduce Further?

The core limitation is **Qiskit's scientific dependencies**:

| Package | Size | Why Needed | Can Remove? |
|---------|------|------------|-------------|
| qiskit | 5.4 MB | Core quantum framework | ❌ No |
| numpy | 14.2 MB | Numerical arrays | ❌ No |
| scipy | 33.6 MB | Scientific computing | ❌ No |
| symengine | 60.9 MB | Symbolic math | ✅ Maybe* |
| sympy | 6.3 MB | Symbolic math | ✅ Maybe* |

*Symbolic math engines could potentially be replaced with lighter alternatives if you don't use certain Qiskit features.

## Build Commands

### Build Optimized Version:
```bash
docker build -t sudeshmu/qiskit-operator:validation-optimized \\
  -f validation-service/Dockerfile.optimized \\
  ./validation-service
```

### Build Minimal Version:
```bash
docker build -t sudeshmu/qiskit-operator:validation-minimal \\
  --build-arg REQUIREMENTS_FILE=requirements.minimal.txt \\
  -f validation-service/Dockerfile.optimized \\
  ./validation-service
```

### Build Alpine Version (Experimental):
```bash
docker build -t sudeshmu/qiskit-operator:validation-alpine \\
  -f validation-service/Dockerfile.alpine \\
  ./validation-service
```

## Push to DockerHub

```bash
# Push optimized version
docker push sudeshmu/qiskit-operator:validation-optimized

# Push minimal version
docker push sudeshmu/qiskit-operator:validation-minimal
```

## Further Reading

- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Distroless Container Images](https://github.com/GoogleContainerTools/distroless)
- [Python Docker Best Practices](https://docs.docker.com/language/python/build-images/)
- [Docker BuildKit](https://docs.docker.com/build/buildkit/)

## Conclusion

**Realistic size reduction**: 4-15% (depending on your use case)  
**Best practical approach**: Use `Dockerfile.optimized` (1.28 GB)  
**Maximum reduction possible**: ~60-70% if using distroless + removing scientific libs (but breaks Qiskit)

The 1.2-1.3 GB size is **reasonable for a quantum computing validation service** given the complex scientific dependencies required.

