import os
import re
import base64
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))
imagesPath = "../files/images/"
targetImageWidth=1000
targetImageHeight=600
widthToHeightRatio = targetImageWidth / targetImageHeight

def extract_coordinates(text):
    # Regular expression pattern to match the coordinates format (x1,y1,x2,y2)
    pattern = r'\((\d+),(\d+),(\d+),(\d+)\)'

    print(f"estract  coordiates from {text}")
    # Search for the pattern in the text
    match = re.search(pattern, text)

    # If a match is found, return the coordinates as integers
    if match:
        return tuple(map(int, match.groups()))

    # If no match is found, return None
    return None

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to get the cropping coordinates from chatGPT API
def get_cropping_coordinates(image_path,widthToHeightRatio):
    prompt_user = f""""Evaluate in coordinate format (x1,y1,x2,y2) the largest part of the picture that both preserve 
    the important part of the picture and has an aspect ratio of {widthToHeightRatio} (width-to-height)."
    """

    print(prompt_user)
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_user},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=300
    )
    text_response = response.choices[0].message.content;
    return extract_coordinates(text_response)

def crop_to_aspect_ratio(img, widthToHeightRatio):
    # Open the image
    original_width, original_height = img.size

    # Calculate the target dimensions based on the aspect ratio
    target_width = original_width
    target_height = int(target_width / widthToHeightRatio)

    # Adjust if the calculated height is greater than the original height
    if target_height > original_height:
        target_height = original_height
        target_width = int(target_height * widthToHeightRatio)

    # Calculate the cropping coordinates
    left = (original_width - target_width) // 2
    top = (original_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return img.crop((left, top, right, bottom))

def process_image(image_path, widthToHeightRatio):
    # Get the cropping coordinates from the API
    # Note that this API call is commented out because at the time it was written it would always fail
    # crop_coordinates = get_cropping_coordinates(image_path, widthToHeightRatio)

    # Crop the image based on the coordinates
    with Image.open(image_path) as img:
        #if crop_coordinates is None:
        #    print(f"ChatGPT could not find cropping coordinates for {image_path}")
        cropped_img = crop_to_aspect_ratio(img, widthToHeightRatio)
        #else:    
        #    cropped_img = img.crop(crop_coordinates)
        # Resize to maintain aspect ratio
        width, height = cropped_img.size
        if width  != targetImageWidth or height != targetImageHeight:
            cropped_img = cropped_img.resize((targetImageWidth, targetImageHeight), Image.LANCZOS)
            directory, filename = os.path.split(image_path)
            cropped_filename = "cr_" + filename
            cropped_imagepath = os.path.join(directory, cropped_filename)
            cropped_img.save(cropped_imagepath)


def process_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") and not filename.startswith("cr_"):
            image_path = os.path.join(directory, filename)
            process_image(image_path, widthToHeightRatio)

# Usage
process_images(imagesPath)
