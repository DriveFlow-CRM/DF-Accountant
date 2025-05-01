.PHONY: setup run test clean docker docker-run docker-compose

# Default target
all: setup

# Setup the project
setup:
	pip install -r requirements.txt

# Run the application
run:
	python app.py

# Test the API
test:
	python test_invoice.py

# Clean up temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f test_invoice.pdf

# Build Docker image
docker:
	docker build -t df-accountant .

# Run the Docker container
docker-run:
	docker run -p 5000:5000 --name df-accountant-container df-accountant

# Run with Docker Compose
docker-compose:
	docker-compose up -d

# Help
help:
	@echo "Available targets:"
	@echo "  setup          - Install dependencies and set up the project"
	@echo "  run            - Run the Flask application"
	@echo "  test           - Test the API with sample data"
	@echo "  clean          - Clean up temporary files"
	@echo "  docker         - Build Docker image"
	@echo "  docker-run     - Run the application in a Docker container"
	@echo "  docker-compose - Run with Docker Compose" 