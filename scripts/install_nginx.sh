#!/bin/bash

LOG_FILE="../logs/provisioning.log"

# Ensure logs directory exists
mkdir -p ../logs

echo "🔄 Starting Nginx installation..." | tee -a $LOG_FILE

# Check if Nginx is already installed
if command -v nginx &> /dev/null; then
    echo "✅ Nginx is already installed." | tee -a $LOG_FILE
else
    echo "⚡ Installing Nginx..." | tee -a $LOG_FILE
    sudo apt update && sudo apt install -y nginx

    # Verify if installation was successful
    if command -v nginx &> /dev/null; then
        echo "✅ Nginx installed successfully!" | tee -a $LOG_FILE
    else
        echo "❌ Error: Nginx installation failed!" | tee -a $LOG_FILE
        exit 1
    fi
fi

