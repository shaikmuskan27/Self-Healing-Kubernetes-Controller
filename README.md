# Self-Healing Kubernetes Controller

This project demonstrates a Python-based Kubernetes controller that automatically detects, diagnoses, and remediates application failures, while logging automated fixes via GitOps principles.

## Features
- Watches for failing `Pods` (e.g., OOMKilled, CrashLoopBackOff).
- Extracts diagnostic logs from Kubernetes.
- Integrates with GitHub to open Pull Requests for automated fixes.
- Sends Interactive webhooks to Slack/Teams with diagnostics and PR links.

## Prerequisites
- A Kubernetes Cluster (Minikube, Kind, etc.)
- Python 3.11+
- `kubectl` configured

## Setup for Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

3. **Run the Controller Locally (Standalone mode):**
   ```bash
   kopf run src/controller.py --standalone
   ```

4. **Deploy the Test Application:**
   ```bash
   kubectl apply -f manifests/test-app.yaml
   ```

## Deploying to Kubernetes
1. Build the Docker image.
2. Apply the RBAC and Deployment manifests.
   ```bash
   kubectl apply -f manifests/rbac.yaml
   kubectl apply -f manifests/deployment.yaml
   ```
