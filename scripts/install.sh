#!/bin/bash

cd ..
# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
echo "Virtual environment created successfully."
sleep 3

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Virtual environment activated successfully."
sleep 3

# Install requirements
echo "Installing packages..."
pip install -r requirements.txt
pip list
echo "Packages installed successfully."
sleep 5