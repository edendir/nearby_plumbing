#!/bin/bash

set -e

echo "Loading environment variables..."
export $(grep -v '^#' .env | xargs)

echo "Building container..."

gcloud builds submit \
  --tag gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME

echo "Deploying to Cloud Run..."

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated \
  --set-env-vars ENV=$ENV \
  --set-env-vars SECRET_KEY=$SECRET_KEY \
  --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY \
  --set-env-vars MAIL_FROM=$MAIL_FROM \
  --set-env-vars MAIL_TO=$MAIL_TO

echo "Deployment complete."