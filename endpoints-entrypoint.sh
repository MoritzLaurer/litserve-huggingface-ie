#!/bin/bash

# Ensure script fails on any error
set -e

# Add more detailed logging
echo "Starting server initialization..."
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "Environment variables: $(env)"

# Print system information for debugging
echo "Architecture: $(uname -m)"
echo "CUDA Version: $(nvcc --version || echo 'NVCC not found')"
echo "Python Version: $(python --version)"
echo "PyTorch CUDA Status: $(python -c 'import torch; print("CUDA available:", torch.cuda.is_available())')"

# Start nginx in background
#nginx

# Start the LitServe server
exec python /app/server.py --port 8080 