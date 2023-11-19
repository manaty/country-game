#!/bin/bash

# Define the project name
PROJECT_NAME="country-game"

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$PROJECT_NAME-venv/bin/activate"

# Execute the createCountryList.py script
echo "Executing createCountryList.py..."
python createCountryList.py
