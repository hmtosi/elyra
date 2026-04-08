# 🚀 Elyra + Minikube Runtime Configuration Guide

## Current Status
✅ Minikube is running  
✅ Kubeflow Pipelines is deployed  
✅ Services detected:
- `ml-pipeline` (KFP API) on port 8888
- `minio-service` (Object Storage) on port 9000
- `seaweedfs` (Alternative storage) available

## Step 1: Set Up Port Forwarding

You need to forward the Kubernetes services to your local machine. Run these commands in **separate terminals** (keep them running):

### Terminal 1: Forward KFP API
```bash
kubectl port-forward -n kubeflow svc/ml-pipeline 8080:8888
```
**Keep this running!** You should see:
```
Forwarding from 127.0.0.1:8080 -> 8888
Forwarding from [::1]:8080 -> 8888
```

### Terminal 2: Forward MinIO (Object Storage)
```bash
kubectl port-forward -n kubeflow svc/minio-service 9000:9000
```
**Keep this running!** You should see:
```
Forwarding from 127.0.0.1:9000 -> 9000
Forwarding from [::1]:9000 -> 9000
```

## Step 2: Get MinIO Credentials

Check your MinIO credentials:
```bash
# Get MinIO access key (username)
kubectl get secret -n kubeflow minio-artifact-secret -o jsonpath='{.data.accesskey}' | base64 -d && echo

# Get MinIO secret key (password)
kubectl get secret -n kubeflow minio-artifact-secret -o jsonpath='{.data.secretkey}' | base64 -d && echo
```

Save these values - you'll need them!

## Step 3: Elyra Runtime Configuration

In JupyterLab, create a new Kubeflow Pipelines runtime with these values:

### Pipeline Settings
- **Display Name**: `Minikube KFP`
- **Description**: `Local Minikube Kubeflow Pipelines`
- **Pipelines API endpoint**: `http://localhost:8080`
- **Public API endpoint**: `http://localhost:8080` (same as above)
- **User namespace**: `kubeflow` (or leave empty)
- **Engine**: `Argo` (you have Argo Workflows)
- **Authentication Type**: `NO_AUTHENTICATION`

### Cloud Object Storage Settings
- **Endpoint**: `http://localhost:9000`
- **Public Endpoint**: `http://localhost:9000` (same as above)
- **Bucket Name**: `mlpipeline` (default KFP bucket)
- **Authentication Type**: `USER_CREDENTIALS`
- **Username**: (paste the accesskey from Step 2)
- **Password**: (paste the secretkey from Step 2)

## Step 4: Verify Port Forwarding is Working

Before running a pipeline, test the connections:

```bash
# Test KFP API
curl http://localhost:8080/apis/v1beta1/healthz
# Should return: {"commit_sha":"...","tag":"..."}

# Test MinIO
curl http://localhost:9000/minio/health/live
# Should return: 200 OK
```

## Step 5: Run Your Pipeline!

Now try running your pipeline with the directory dependency test.

## Troubleshooting

### Issue: "Connection Refused" error
**Cause**: Port forwarding not running  
**Fix**: Make sure both `kubectl port-forward` commands are running in separate terminals

### Issue: "Authentication failed" error
**Cause**: Wrong MinIO credentials  
**Fix**: Re-run Step 2 to get the correct credentials

### Issue: "Bucket not found" error
**Cause**: Wrong bucket name  
**Fix**: Check the bucket name:
```bash
# Access MinIO web UI (with port-forward running)
# Open http://localhost:9000 in browser
# Login with your credentials
# Check existing buckets
```

Common bucket names:
- `mlpipeline` (default)
- `minio` 
- Check what exists in your setup

### Issue: Port already in use
**Cause**: Another service using 8080 or 9000  
**Fix**: Use different local ports:
```bash
# KFP on 8081 instead of 8080
kubectl port-forward -n kubeflow svc/ml-pipeline 8081:8888

# MinIO on 9001 instead of 9000
kubectl port-forward -n kubeflow svc/minio-service 9001:9000
```
Then update your Elyra config to use `localhost:8081` and `localhost:9001`

## Quick Start Script

Save this as `start-elyra-minikube.sh`:
```bash
#!/bin/bash
echo "Starting port forwarding for Elyra + Minikube..."
echo "Press Ctrl+C to stop all port forwards"

# Trap Ctrl+C to kill all background jobs
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# Start port forwards in background
kubectl port-forward -n kubeflow svc/ml-pipeline 8080:8888 &
kubectl port-forward -n kubeflow svc/minio-service 9000:9000 &

echo ""
echo "✓ KFP API: http://localhost:8080"
echo "✓ MinIO: http://localhost:9000"
echo ""
echo "Port forwarding active. Press Ctrl+C to stop."

# Wait for all background jobs
wait
```

Make it executable and run:
```bash
chmod +x start-elyra-minikube.sh
./start-elyra-minikube.sh
```

## Summary

1. ✅ Run port-forward commands (keep them running)
2. ✅ Get MinIO credentials from Kubernetes secrets
3. ✅ Configure Elyra runtime with correct values
4. ✅ Test the pipeline with directory dependencies!
