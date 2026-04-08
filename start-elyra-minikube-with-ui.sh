#!/bin/bash
# Port forwarding script for Elyra + Minikube (with UI access)
# Keep this running while using Elyra with Minikube

echo "=========================================="
echo "Elyra + Minikube Port Forwarding Setup"
echo "=========================================="
echo ""

# Trap Ctrl+C to kill all background jobs
trap "echo ''; echo 'Stopping all port forwards...'; kill 0; exit 0" SIGINT SIGTERM EXIT

# Start port forwards in background
echo "Starting port forwards..."
kubectl port-forward -n kubeflow svc/ml-pipeline 8080:8888 > /dev/null 2>&1 &
PID1=$!
kubectl port-forward -n kubeflow svc/minio-service 9000:9000 > /dev/null 2>&1 &
PID2=$!
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8081:80 > /dev/null 2>&1 &
PID3=$!

# Wait a moment for port forwards to start
sleep 2

# Check if port forwards are working
if kill -0 $PID1 2>/dev/null && kill -0 $PID2 2>/dev/null && kill -0 $PID3 2>/dev/null; then
    echo "✓ Port forwarding active!"
    echo ""
    echo "Services available at:"
    echo "  • KFP API:  http://localhost:8080"
    echo "  • KFP UI:   http://localhost:8081  ← Open this in your browser!"
    echo "  • MinIO:    http://localhost:9000"
    echo ""
    echo "Elyra Runtime Configuration:"
    echo "  • API Endpoint: http://localhost:8080"
    echo "  • MinIO Endpoint: http://localhost:9000"
    echo "  • MinIO Username: minio"
    echo "  • MinIO Password: minio123"
    echo "  • Bucket: mlpipeline"
    echo ""
    echo "To view your pipeline runs:"
    echo "  1. Open http://localhost:8081 in your browser"
    echo "  2. Click on 'Experiments' to see your pipelines"
    echo ""
    echo "Press Ctrl+C to stop port forwarding"
    echo "=========================================="
    echo ""

    # Wait for all background jobs
    wait
else
    echo "✗ Failed to start port forwarding!"
    echo "Check that minikube is running: minikube status"
    exit 1
fi
