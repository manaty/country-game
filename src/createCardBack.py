from PIL import Image, ImageDraw, ImageFont
import os

def combine_images(image_dir, country_name, country_code,country_files, output_dir):
    # List of image paths for the current country
    image_paths = [os.path.join(image_dir, f"{country_file}") for country_file in country_files]
    
    # Load images
    images = [Image.open(path) for path in image_paths]
    
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
    font_size = 10
    text_width = 0
    try:
        font = ImageFont.truetype('font/arial.ttf', font_size)
        while text_width < combined_image.size[0] * 0.6:
            # Increment font size
            font_size += 1    
            ImageFont.truetype('font/arial.ttf', font_size)
            text_width = draw.textlength(country_name, font=font)
        # Calculate text position (centered)
        (left, top, right, bottom) = draw.textbbox((0, 0), country_name, font=font)
        text_width = right - left
        text_height = bottom - top
        x_text = (combined_image.size[0] - text_width) // 2
        y_text = (combined_image.size[1] - text_height) // 2
        
        # Shadow effect
        shadow_offset = 2
        shadow_color = 'grey'
        draw.text((x_text + shadow_offset, y_text + shadow_offset), country_name, font=font, fill=shadow_color)
        
        # Actual text
        draw.text((x_text, y_text), country_name, font=font, fill='black')
    except OSError:
        font = ImageFont.load_default()    
        # Calculate the desired width of the text as 60% of the image width
        target_text_width = combined_image.size[0] * 0.6
        
        # Load the default font
        font = ImageFont.load_default()
        
        (left, top, right, bottom) = draw.textbbox((0, 0), country_name, font=font)
        temp_width = right - left
        temp_height = bottom - top

        # Create a new temporary image for drawing the text
        temp_image = Image.new('RGB', (temp_width, temp_height), 'white')
        text_draw = ImageDraw.Draw(temp_image)

        # Draw the text
        text_draw.text((0, 0), country_name, font=font, fill='black')
        
        # Resize the temp image to 80% of the combined image width while maintaining aspect ratio
        scaling_factor = target_text_width / temp_width
        new_size = (int(temp_width * scaling_factor), int(temp_height * scaling_factor))
        resized_text_image = temp_image.resize(new_size, Image.LANCZOS)
        
        # Calculate position to paste the resized text image onto the combined image
        x_text = (combined_image.size[0] - new_size[0]) // 2
        y_text = (combined_image.size[1] - new_size[1]) // 2
        
        # Paste the resized text image onto the combined image
        combined_image.paste(resized_text_image, (x_text, y_text))

    
    # Save the result
    output_path = os.path.join(output_dir, f"{country_code}_back.png")
    combined_image.save(output_path, 'PNG')
    print(f"Image saved for {country_name}")

# Directory where the images are stored
image_dir = '../files/images'
# Directory where you want to save the output images
output_dir = '../files/cards'
# Ensure directory exists
os.makedirs(os.path.dirname(output_dir), exist_ok=True)

# Get a list of all files in the directory
files = os.listdir(image_dir)

# Group files by country code and country name
countries = {}
for file in files:
    parts = file.split('_')
    country_code = parts[1]
    country_name = parts[2]
    countries.setdefault(country_name, []).append(file)

# Process each country
for country_name, country_files in countries.items():
    country_code = country_files[0].split('_')[1]
    combine_images(image_dir, country_name, country_code,country_files, output_dir)
