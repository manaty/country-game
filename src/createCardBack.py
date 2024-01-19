import io
import zipfile
from PIL import Image, ImageDraw, ImageFont
import os

import requests

def download_and_extract_font(url, destination_folder, font_name):
    # Check if the font already exists
    if os.path.exists(os.path.join(destination_folder, font_name)):
        #print(f"Font '{font_name}' already exists in '{destination_folder}'. No download needed.")
        return

    # Make the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    try:
        # Download the font
        response = requests.get(url)
        response.raise_for_status()
        # Unzip the font and save to the destination folder
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            thezip.extractall(destination_folder)
        print(f"Font '{font_name}' downloaded and extracted to '{destination_folder}'")
    except requests.RequestException as e:
        print(f"Error downloading the font: {e}")


def combine_images(image_dir, country_name, country_code,country_files, output_dir):
    # List of image paths for the current country
    image_paths = [os.path.join(image_dir, f"{country_file}") for country_file in country_files]
    
    # Load images
    images = [Image.open(path) for path in image_paths]
    print(f"Loaded {len(images)}")

    # Determine the max width and height of the images (assuming they are the same size)
    max_width = max(i.size[0] for i in images)
    max_height = max(i.size[1] for i in images)
    
    # Create a new image with a white background
    combined_image = Image.new('RGB', (max_width * 2, max_height * 2), 'white')
    
    # Paste images into a 2x2 grid
    combined_image.paste(images[0], (0, 0))
    combined_image.paste(images[1], (max_width, 0))
    combined_image.paste(images[2], (0, max_height))
    combined_image.paste(images[3], (max_width, max_height))
    
    # Add the country name with shadow effect
    draw = ImageDraw.Draw(combined_image)
    font_size = 100
    text_width = 0
    download_and_extract_font(font_url,font_folder,font_name)
    try:
        font_path = os.path.join(font_folder,font_name)
        font = ImageFont.truetype(font_path, font_size)
        targetwidth = combined_image.size[0] * 0.6
        while text_width < targetwidth  and font_size < 1000:
            # Increment font size
            font_size += 10    
            font = ImageFont.truetype(font_path, font_size)
            (left, top, right, bottom) = draw.textbbox((0, 0), country_name, font=font)
            text_width = right-left
            #print(f"Trying font size {font_size}, text width {text_width}")
        # Calculate text position (centered)
        (left, top, right, bottom) = draw.textbbox((0, 0), country_name, font=font)
        text_width = right - left
        text_height = bottom - top
        x_text = (combined_image.size[0] - text_width) // 2
        y_text = (combined_image.size[1] - text_height) // 2.5
        
        # neon effect
        delta=5
        draw.text((x_text-delta, y_text-delta), country_name, font=font, fill='white')
        draw.text((x_text-delta, y_text+delta), country_name, font=font, fill='white')
        draw.text((x_text+delta, y_text-delta), country_name, font=font, fill='white')
        draw.text((x_text+delta, y_text+delta), country_name, font=font, fill='white')
        # Actual text
        draw.text((x_text, y_text), country_name, font=font, fill='black')
    except OSError:
        print("Font not found. Skipping country name.")
        return

    
    # Save the result
    output_path = os.path.join(output_dir, f"{country_code}_{country_name}_back.png")
    combined_image.save(output_path, 'PNG')
    print(f"Image saved for {country_name}")



font_url = "https://fonts.google.com/download?family=Lato"
font_folder = "../files/font"
font_name = "Lato-Regular.ttf"
# Directory where the images are stored
image_dir = '../files/images'
# Directory where you want to save the output images
output_dir = '../files/cards'
# Ensure directory exists
os.makedirs(os.path.dirname(output_dir), exist_ok=True)

# Get a list of all files in the directory
files = os.listdir(image_dir)
#print(f"Found {len(files)} files")
# Group files by country code and country name
countries = {}
for file in files:
    parts = file.split('_')
    if parts[0] != 'cr':
        continue
    #print(parts)
    country_code = parts[1]
    country_name = parts[2]
    countries.setdefault(country_name, []).append(file)
    print(f"Added {file} to {country_name}")
    #print(countries)

# Process each country
for country_name, country_files in countries.items():
    print(f"Processing {country_name}")
    #print(country_files)
    country_code = country_files[0].split('_')[1]
    combine_images(image_dir, country_name, country_code,country_files, output_dir)
