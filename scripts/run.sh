#!/bin/bash

cd ..
# Activate virtual environment
source .venv/bin/activate

# Start the program
echo "Project starting..."
.venv/bin/python3 src/app.py
