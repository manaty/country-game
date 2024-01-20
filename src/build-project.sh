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
echo "Getting landmarks of countries"
python 1_createCountryLandmarks.py

echo "Download images of the landmarks..."
python 2_downloadImages.py

echo "Generate images of missing landmarks..."
python 3_generateLandmarkImages.py

echo "Resize landmarks images that are too large..."
python 4_resizeImages.py

echo "Crop images of the landmarks..."
python 5_cropImages.py 

echo "assemble images into card's back..."
python createCardBack.py

echo "Download globe images for card's front..."
python downloadGlobeImages.py

echo "Copy map images for card's front..."
python copyMapImages.py

echo "Assemble card's front..."
python createCardFront.py
