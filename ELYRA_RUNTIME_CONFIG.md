# 🎯 Elyra Runtime Configuration for Your Minikube Setup

## Your Exact Configuration Values

Based on your Minikube setup, here are the **exact values** to use in Elyra:

### Pipeline Settings
```
Display Name: Minikube KFP
Description: Local Minikube Kubeflow Pipelines
Tags: (optional)

Pipelines API endpoint: http://localhost:8080
Public API endpoint: http://localhost:8080
User namespace: kubeflow
Engine: Argo

Authentication Type: NO_AUTHENTICATION
API endpoint username: (leave empty)
API endpoint password or token: (leave empty)
```

### Cloud Object Storage Settings
```
Cloud Object Storage Endpoint: http://localhost:9000
Public Cloud Object Storage Endpoint: http://localhost:9000
Cloud Object Storage Bucket Name: mlpipeline

Cloud Object Storage Authentication Type: USER_CREDENTIALS
Cloud Object Storage Credentials Secret: (leave empty)

Cloud Object Storage Username: minio
Cloud Object Storage Password: minio123
```

## Step-by-Step Setup

### 1. Start Port Forwarding
```bash
cd /home/htosi/elyra
./start-elyra-minikube.sh
```

**Keep this terminal open and running!**

You should see:
```
✓ Port forwarding active!

Services available at:
  • KFP API:  http://localhost:8080
  • MinIO:    http://localhost:9000
```

### 2. Test the Connections

Open a **new terminal** and test:

```bash
# Test KFP API
curl http://localhost:8080/apis/v1beta1/healthz

# Test MinIO
curl http://localhost:9000/minio/health/live
```

If both work, you're good to go! ✅

### 3. Create Elyra Runtime in JupyterLab

1. In JupyterLab, click the **Runtimes** icon (rocket icon) in the left sidebar
2. Click **"+"** to create a new runtime
3. Select **"Kubeflow Pipelines"**
4. Fill in the form with the **exact values above**
5. Click **"Save"**

### 4. Run Your Test Pipeline

1. Open the pipeline you created earlier
2. Make sure the dependency is set to `sample_data` (not `test_directory_deps/sample_data`)
3. Click the **"Run Pipeline"** button
4. Select your **"Minikube KFP"** runtime
5. Give it a name and click **"OK"**

## What's Different from Your Previous Config?

### ❌ Your Previous Config (Incorrect)
```
API endpoint: http://localhost:8080  ✓ Correct
MinIO Endpoint: http://localhost:50000  ✗ Wrong port!
MinIO Username: usrn  ✗ Wrong username!
MinIO Password: pwd  ✗ Wrong password!
Bucket: elyra  ✗ Wrong bucket!
```

### ✅ Correct Config
```
API endpoint: http://localhost:8080  ✓
MinIO Endpoint: http://localhost:9000  ✓ Correct port!
MinIO Username: minio  ✓ Actual username!
MinIO Password: minio123  ✓ Actual password!
Bucket: mlpipeline  ✓ Default KFP bucket!
```

## Common Issues

### "Connection Refused" on localhost:8080
**Problem**: Port forwarding not running  
**Solution**: 
```bash
./start-elyra-minikube.sh
```

### "Authentication failed" for MinIO
**Problem**: Wrong credentials  
**Solution**: Use exactly:
- Username: `minio`
- Password: `minio123`

### "Bucket not found: mlpipeline"
**Problem**: Bucket doesn't exist  
**Solution**: Create it:
```bash
# Port forward MinIO (if not already)
kubectl port-forward -n kubeflow svc/minio-service 9000:9000

# In browser, go to: http://localhost:9000
# Login with: minio / minio123
# Create bucket named: mlpipeline
```

Or use the MinIO client:
```bash
# Install mc (MinIO client)
# Then:
mc alias set myminio http://localhost:9000 minio minio123
mc mb myminio/mlpipeline
```

## Quick Checklist

Before running a pipeline, verify:

- [ ] Port forwarding is running (`./start-elyra-minikube.sh`)
- [ ] Can access http://localhost:8080/apis/v1beta1/healthz
- [ ] Can access http://localhost:9000/minio/health/live
- [ ] Elyra runtime is configured with correct values
- [ ] Bucket `mlpipeline` exists in MinIO
- [ ] Dependencies are specified relative to notebook (e.g., `sample_data`)

## All Set! 🚀

You're ready to test the directory dependency fix on your local Minikube cluster!
