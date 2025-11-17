#!/bin/bash

# Script to push README to DockerHub repository
# Usage: ./push-dockerhub-readme.sh <dockerhub-username> <dockerhub-token>

set -e

DOCKERHUB_USERNAME="${1:-sudeshmu}"
DOCKERHUB_TOKEN="${2}"
REPOSITORY="qiskit-operator"
README_FILE="DOCKERHUB_README.md"

if [ -z "$DOCKERHUB_TOKEN" ]; then
    echo "❌ Error: DockerHub token is required"
    echo ""
    echo "Usage: ./push-dockerhub-readme.sh <username> <token>"
    echo ""
    echo "To get your DockerHub token:"
    echo "1. Go to https://hub.docker.com/settings/security"
    echo "2. Click 'New Access Token'"
    echo "3. Give it a name (e.g., 'readme-update')"
    echo "4. Copy the token"
    echo "5. Run: ./push-dockerhub-readme.sh sudeshmu YOUR_TOKEN"
    echo ""
    echo "Alternatively, update README manually:"
    echo "1. Go to https://hub.docker.com/r/${DOCKERHUB_USERNAME}/${REPOSITORY}"
    echo "2. Click 'Description' tab"
    echo "3. Copy contents from ${README_FILE}"
    echo "4. Paste and save"
    exit 1
fi

echo "📝 Updating DockerHub README for ${DOCKERHUB_USERNAME}/${REPOSITORY}..."

# Read the README file
README_CONTENT=$(cat "$README_FILE")

# Escape special characters for JSON
README_JSON=$(jq -Rs . <<< "$README_CONTENT")

# Get JWT token from DockerHub
echo "🔐 Authenticating with DockerHub..."
TOKEN_RESPONSE=$(curl -s -X POST \
    "https://hub.docker.com/v2/users/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${DOCKERHUB_USERNAME}\",\"password\":\"${DOCKERHUB_TOKEN}\"}")

JWT_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.token')

if [ "$JWT_TOKEN" = "null" ] || [ -z "$JWT_TOKEN" ]; then
    echo "❌ Authentication failed. Check your username and token."
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi

# Update the repository description
echo "📤 Uploading README to DockerHub..."
UPDATE_RESPONSE=$(curl -s -X PATCH \
    "https://hub.docker.com/v2/repositories/${DOCKERHUB_USERNAME}/${REPOSITORY}/" \
    -H "Authorization: JWT ${JWT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"full_description\": ${README_JSON}}")

# Check if update was successful
if echo "$UPDATE_RESPONSE" | jq -e '.full_description' > /dev/null 2>&1; then
    echo "✅ Successfully updated DockerHub README!"
    echo "🔗 View at: https://hub.docker.com/r/${DOCKERHUB_USERNAME}/${REPOSITORY}"
else
    echo "❌ Failed to update README"
    echo "Response: $UPDATE_RESPONSE"
    exit 1
fi

