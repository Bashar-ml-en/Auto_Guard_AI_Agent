#!/usr/bin/env bash
# ==============================================================================
# AutoGuard AI - Google Cloud Run One-Click Deployment Script
# ==============================================================================
set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null)}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="autoguard-ai"

if [ -z "$PROJECT_ID" ]; then
  echo "Error: GOOGLE_CLOUD_PROJECT is not set and no default gcloud project configured."
  echo "Usage: export GOOGLE_CLOUD_PROJECT=your-project-id && ./deploy/deploy.sh"
  exit 1
fi

echo "========================================================"
echo " Deploying AutoGuard AI to Google Cloud Platform"
echo " Project: $PROJECT_ID | Region: $REGION"
echo " Service: $SERVICE_NAME"
echo "========================================================"

# Enable required Google Cloud APIs
echo "--> Enabling Cloud Run, Artifact Registry, and Firestore APIs..."
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  firestore.googleapis.com \
  storage.googleapis.com \
  --project="$PROJECT_ID"

# Build and Deploy to Cloud Run
echo "--> Submitting build to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --platform managed \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production,GEMINI_MODEL=gemini-2.5-flash,GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

echo "========================================================"
echo " Deployment Complete!"
echo " Service URL: $(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')"
echo "========================================================"
