#!/bin/bash

# Define the project name
PROJECT_NAME="country-game"

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$PROJECT_NAME-venv/bin/activate"

# set private keys as environment variables
echo "Setting private keys as environment variables..."
python ../private/setEnv.py

# Execute the createCountryList.py script
echo "Executing createCountryList.py..."
python createCountryList.py

echo "Download images of the landmarks..."
python downloadImages.py

echo "Crop images of the landmarks..."
python cropImages.py 

echo "assemble images into card's back..."
python createCardBack.py

echo "Download globe images for card's front..."
python downloadGlobeImages.py

echo "Copy map images for card's front..."
python copyMapImages.py

echo "Assemble card's front..."
python createCardFront.py
