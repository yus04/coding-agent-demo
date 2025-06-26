#!/bin/bash

# Streamlit TODO App - Azure Deployment Script
# This script automates the deployment process to Azure App Service

set -e

# Configuration
RESOURCE_GROUP="rg-streamlit-todo"
LOCATION="japaneast"
APP_SERVICE_PLAN="plan-streamlit-todo"
WEB_APP_NAME="streamlit-todo-app-$(date +%s)"  # Add timestamp for uniqueness
SKU="B1"

echo "🚀 Starting Azure deployment for Streamlit TODO app..."

# Check if Azure CLI is installed and user is logged in
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

echo "✅ Azure CLI check passed"

# Create resource group
echo "📦 Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
echo "🏗️  Creating App Service plan: $APP_SERVICE_PLAN"
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku $SKU \
    --is-linux

# Create Web App
echo "🌐 Creating Web App: $WEB_APP_NAME"
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --runtime "PYTHON|3.11" \
    --startup-file startup.sh

# Configure app settings
echo "⚙️  Configuring application settings..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        ENABLE_ORYX_BUILD=true \
        STREAMLIT_SERVER_HEADLESS=true \
        STREAMLIT_SERVER_ENABLE_CORS=false \
        STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Prepare deployment package
echo "📦 Preparing deployment package..."
zip -r deployment.zip app.py requirements.txt startup.sh

# Deploy the application
echo "🚀 Deploying application..."
az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --src deployment.zip

# Clean up
rm deployment.zip

# Get the URL
URL="https://${WEB_APP_NAME}.azurewebsites.net"

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your app is available at: $URL"
echo "📊 Monitor logs with: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo ""
echo "📝 Resource details:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   App Service Plan: $APP_SERVICE_PLAN"
echo "   Web App Name: $WEB_APP_NAME"
echo "   Location: $LOCATION"