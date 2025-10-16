# ArgoCD Deployment

GitOps-based continuous deployment using ArgoCD.

## Prerequisites

1. Kubernetes cluster (v1.24+)
2. kubectl configured
3. ArgoCD installed in cluster

## Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Access ArgoCD UI: https://localhost:8080
- Username: `admin`
- Password: (from command above)

## Deploy Application

### Option 1: Using kubectl

```bash
# Update application.yaml with your GitHub username
sed -i 's/YOUR_GITHUB_USERNAME/your-username/g' application.yaml

# Apply ArgoCD application
kubectl apply -f application.yaml

# Check application status
kubectl get application -n argocd
```

### Option 2: Using ArgoCD CLI

```bash
# Install ArgoCD CLI
brew install argocd  # macOS
# or download from https://argo-cd.readthedocs.io/en/stable/cli_installation/

# Login
argocd login localhost:8080

# Create application
argocd app create exoplanet-detection \
  --repo https://github.com/YOUR_GITHUB_USERNAME/exovisions2.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace exoplanet \
  --sync-policy automated \
  --auto-prune \
  --self-heal

# Sync application
argocd app sync exoplanet-detection

# Watch application status
argocd app get exoplanet-detection --watch
```

## Verify Deployment

```bash
# Check all resources
kubectl get all -n exoplanet

# Check application health
kubectl get application -n argocd exoplanet-detection

# Check ingress
kubectl get ingress -n exoplanet
```

## Update Deployment

ArgoCD automatically syncs when you push changes to Git:

```bash
# 1. Make changes to k8s/ manifests
# 2. Commit and push to GitHub
git add k8s/
git commit -m "Update deployment"
git push origin main

# 3. ArgoCD will automatically detect and apply changes
# Watch in ArgoCD UI or:
argocd app get exoplanet-detection --watch
```

## Rollback

```bash
# List application history
argocd app history exoplanet-detection

# Rollback to previous version
argocd app rollback exoplanet-detection <REVISION_ID>
```

## Delete Application

```bash
# Delete via ArgoCD (cascade deletes all resources)
argocd app delete exoplanet-detection

# Or via kubectl
kubectl delete -f application.yaml
```
