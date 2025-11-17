# How to Update DockerHub README

You have two options to update the DockerHub README with the content from `DOCKERHUB_README.md`:

## Option 1: Automated Script (Recommended)

### Prerequisites
- Install `jq` if not already installed:
  ```bash
  # macOS
  brew install jq
  
  # Linux
  sudo apt-get install jq
  ```

### Steps

1. **Get your DockerHub Access Token**:
   - Go to https://hub.docker.com/settings/security
   - Click "New Access Token"
   - Name it "readme-update" (or any name)
   - Copy the generated token

2. **Run the script**:
   ```bash
   cd /Users/sudeshmu/work/temps/cirqKube/qiskit-operator
   ./push-dockerhub-readme.sh sudeshmu YOUR_DOCKERHUB_TOKEN
   ```

3. **Verify**:
   - Visit https://hub.docker.com/r/sudeshmu/qiskit-operator
   - Check that the README is updated

## Option 2: Manual Update (Simple)

If you prefer not to use the API or don't have `jq`:

1. **Open the README file**:
   ```bash
   cat /Users/sudeshmu/work/temps/cirqKube/qiskit-operator/DOCKERHUB_README.md
   ```

2. **Copy the entire content**

3. **Go to DockerHub**:
   - Visit https://hub.docker.com/r/sudeshmu/qiskit-operator
   - Sign in if needed

4. **Update the description**:
   - Click the **"Description"** tab (if not already there)
   - Click **"Edit"** button
   - Replace the existing content with the copied README
   - Click **"Update"** to save

## What's in the README?

The README includes:
- ✅ Quick start guide
- ✅ Image descriptions (controller + validation service)
- ✅ Multi-platform architecture support
- ✅ Kubernetes deployment examples
- ✅ Configuration options
- ✅ Use cases and examples
- ✅ Links and documentation

## Verify the Update

After updating, check:
- https://hub.docker.com/r/sudeshmu/qiskit-operator

The new README should be visible to anyone viewing your repository.

