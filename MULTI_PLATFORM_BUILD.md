# Multi-Platform Docker Images

Both Docker images for the Qiskit Operator have been built and pushed as **multi-platform images** that work across different operating systems and architectures.

## Supported Platforms

Both images support the following platforms:
- **linux/amd64** - Intel/AMD x86_64 (most common for servers, cloud deployments)
- **linux/arm64** - ARM64 (Apple Silicon M1/M2/M3, AWS Graviton, Raspberry Pi 4)

## Published Images

### 1. Controller Image
```
sudeshmu/qiskit-operator:controller-latest
```
- **Digest**: `sha256:4b4e06297b841dfa2f123113b13710a27fb072abeeb013981e20359d43af41f2`
- **Platforms**: linux/amd64, linux/arm64
- **Base Image**: `gcr.io/distroless/static:nonroot`
- **Size**: ~15-20 MB per platform

### 2. Validation Service Image
```
sudeshmu/qiskit-operator:validation-latest
```
- **Digest**: `sha256:62292b0a6b3f437a1ad7703f9c743ad0728ada213b08e17520ecba6cca5535ee`
- **Platforms**: linux/amd64, linux/arm64
- **Base Image**: `python:3.11-slim`
- **Size**: ~1.3 GB per platform (includes Qiskit, NumPy, SciPy, SymEngine)

## How It Works

When you pull these images, Docker automatically detects your system architecture and pulls the correct image variant:

```bash
# On Intel/AMD machines (x86_64)
docker pull sudeshmu/qiskit-operator:controller-latest
# → Automatically pulls linux/amd64 variant

# On Apple Silicon (M1/M2/M3) or ARM servers
docker pull sudeshmu/qiskit-operator:controller-latest
# → Automatically pulls linux/arm64 variant
```

## Kubernetes Deployment

In Kubernetes, multi-platform images work seamlessly:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qiskit-operator
spec:
  template:
    spec:
      containers:
      - name: manager
        image: sudeshmu/qiskit-operator:controller-latest
        # Kubernetes automatically pulls the right architecture
```

Your cluster nodes can be:
- **Intel/AMD x86_64 nodes** → Gets linux/amd64 image
- **ARM64 nodes** (AWS Graviton, Raspberry Pi) → Gets linux/arm64 image
- **Mixed architecture clusters** → Each node gets its matching image

## Building Multi-Platform Images

The images were built using Docker Buildx:

```bash
# Create multi-platform builder
docker buildx create --name multiarch-builder --use --bootstrap

# Build and push controller
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t sudeshmu/qiskit-operator:controller-latest \
  -f Dockerfile .

# Build and push validation service
cd validation-service
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t sudeshmu/qiskit-operator:validation-latest \
  -f Dockerfile .
```

## Verification

Verify platform support:

```bash
# Check controller image platforms
docker buildx imagetools inspect sudeshmu/qiskit-operator:controller-latest

# Check validation service platforms
docker buildx imagetools inspect sudeshmu/qiskit-operator:validation-latest
```

## Benefits

1. **Universal Compatibility**: Works on Intel, AMD, and ARM processors
2. **Cloud-Native**: Compatible with all major cloud providers
   - AWS (x86 + Graviton ARM)
   - Google Cloud (x86 + Tau ARM)
   - Azure (x86 + Ampere ARM)
3. **Developer Friendly**: Works on Apple Silicon Macs natively
4. **Cost Optimization**: Can use cheaper ARM-based instances
5. **Edge Computing**: Deploy on Raspberry Pi and other ARM devices
6. **Future-Proof**: Ready for the industry shift to ARM architectures

## Size Optimization

The validation service image can be further optimized:
- See `DOCKER_OPTIMIZATION_GUIDE.md` for strategies
- Current optimized version: **~900 MB** (using multi-stage build)
- Minimal version (without IBM Runtime): **~700 MB**

## Notes

- Both images include attestation manifests for security verification
- Images are automatically scanned by DockerHub security scanning
- Use specific version tags in production (e.g., `v0.1.0`) instead of `latest`

