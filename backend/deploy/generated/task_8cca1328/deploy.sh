#!/usr/bin/env bash
# Deploy autoguard-fortified-agent-task_8 to Google Cloud Run
set -e
echo "Building and deploying autoguard-fortified-agent-task_8 to Google Cloud Run in project autoguard-hackathon-demo..."
gcloud run deploy autoguard-fortified-agent-task_8 \
  --source . \
  --platform managed \
  --region us-central1 \
  --project autoguard-hackathon-demo \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_MODEL=gemini-2.5-flash"
