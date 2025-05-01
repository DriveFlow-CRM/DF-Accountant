#!/bin/bash

echo "Building and starting DF-Accountant in Docker..."
echo "---------------------------------------------------"

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose down

# Build and start the container
echo "Building and starting container..."
docker-compose up --build -d

echo "---------------------------------------------------"
echo "DF-Accountant is now running in Docker!"
echo "API available at: http://localhost:5000/api/v1/getInvoice"
echo "Use Postman or any API client to test with POST requests" 