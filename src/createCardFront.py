import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

font_size = 30
small_font_size = 20
line_height = 40
font_folder = "../files/font"
font_name = "Lato-Regular.ttf"
font_path = os.path.join(font_folder,font_name)
font = ImageFont.truetype(font_path, font_size)
small_font = ImageFont.truetype(font_path, small_font_size)

# Directory where the images are stored
image_folder = '../files/globe'
# Directory where you want to save the output images
output_dir = '../files/cards'
# Ensure directory exists
os.makedirs(os.path.dirname(output_dir), exist_ok=True)

# Get a list of all files in the directory
files = os.listdir(image_folder)

# Read CSV file
csv_file = '../files/country_names.csv'  
data = pd.read_csv(csv_file, header=None)
countries = data.values

landmarks_csv = '../files/country_landmarks.csv' 
landmark_data = pd.read_csv(landmarks_csv, header=None, quotechar='"', doublequote=True)
landmarks_dict = dict(zip(landmark_data[0], landmark_data.iloc[:, 1:].values.tolist()))


# Function to paste an image with transparency onto a background
def paste_with_transparency(background, image, position):
    alpha = image.split()[3]
    alpha = alpha.point(lambda p: p * 0.5)
    image.putalpha(alpha)
    # Paste the image onto this temporary image
    background.paste(image, position, image)
    return background

# Function to resize image while preserving aspect ratio
def resize_image(image, target_height):
    w, h = image.size
    aspect_ratio = w / h
    new_height = target_height
    new_width = int(new_height * aspect_ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)

# Function to wrap text to fit within a specified width
def draw_text(draw, text, position, font, max_width):
    text_x, text_y = position
    lines = []
    words = text.split()
    while words:
        line = ''
        # Check the width of the line with one more word
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line += words.pop(0) + ' '
        lines.append(line)

    for line in lines:
        draw.text((text_x, text_y), line.strip(), fill='black', font=font)
        text_y += line_height

    return text_y


# Function to create a card for each country
def create_front_card(index,country_info):
    country_name = country_info[0]

    globe_image_path = f'{image_folder}/{index}_{country_name}_globe.png'
    map_image_path = f'{image_folder}/{index}_{country_name}_map.png'

    # Create a new image (card) with white background
    card_width = 576
    card_height = 1024  # portrait mode (9:16 aspect ratio)
    card = Image.new('RGB', (card_width, card_height), 'white')

    # Load images
    # this should not fail if an image is missing
    try:
        globe_image = Image.open(globe_image_path)
        globe_image = resize_image(globe_image, int(card_height * 0.3))
        globe_x = (card_width - globe_image.width) // 2
        card = paste_with_transparency(card,globe_image, (globe_x, 0))
    except FileNotFoundError:
        print(f"Could not find {globe_image_path}")
        pass
    try:
        map_image = Image.open(map_image_path)
        map_image = resize_image(map_image, int(card_height * 0.7))
        map_x = (card_width - map_image.width) // 2
        card = paste_with_transparency(card, map_image, (map_x, int(card_height * 0.3)))
    except FileNotFoundError:
        print(f"Could not find {map_image_path}")
        pass


    # Add text over the images
    draw = ImageDraw.Draw(card)
    text_x, text_y = 20, 20  # Starting position for the text
    
    # Country information with labels
    info_labels = ["Name: ","Population: ", "Capital: ", "Languages: ", "Currency: ", 
                   "Landmark: ", "Dish/Drink 1: ", "Dish/Drink 2: ", "Dish/Drink 3: "]
    text_y = draw_text(draw, f'Name: {country_info[0]}', (text_x, text_y), font, card_width)
    text_y = draw_text(draw, f'Population: {country_info[1]}', (text_x, text_y), font, card_width)
    text_y = draw_text(draw, f'Capital: {country_info[2]}', (text_x, text_y), font, card_width)
    text_y = draw_text(draw, f'Currency: {country_info[3]}', (text_x, text_y), font, card_width)
    text_y = draw_text(draw, f'Languages: {country_info[4]}', (text_x, text_y), font, card_width)
    text_y += 40
    # Landmark information
    landmarks = landmarks_dict.get(country_name)
    h1 = draw_text(draw, f'{landmarks[0]}', (10, text_y), font, card_width/2-10)
    h2 = draw_text(draw, f'{landmarks[2]}', (20+card_width/2, text_y), font, card_width/2-10)
    text_y = max(h1,h2)
    h1 = draw_text(draw, f'{landmarks[1]}', (10, text_y), font, card_width/2)
    h2 = draw_text(draw, f'{landmarks[3]}', (20+card_width/2, text_y), font, card_width/2-10)
    text_y = max(h1,h2)+40
    
    text_y = draw_text(draw, f'{country_info[6]}', (text_x, text_y), small_font, card_width-20)
    text_y += 20
    text_y = draw_text(draw, f'{country_info[7]}', (text_x, text_y), small_font, card_width-20)
    text_y += 20
    text_y = draw_text(draw, f'{country_info[8]}', (text_x, text_y), small_font, card_width-20)
    
    # Save the card
    card.save(f'{output_dir}/{index}_{country_name}_front.png')

# Create a card for each country
for index, country in enumerate(countries):
    create_front_card(index+1, country)

print("Cards created successfully.")