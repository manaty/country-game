import os
from PIL import Image

maxSize = 1000000
imagesPath = "../files/images/"

def resize_image(image_path,ratio):
    image = Image.open(image_path)
    imageSize = image.size
    print(f"image size: {imageSize}")

    image.thumbnail((ratio * image.size[0], ratio * image.size[1]))
    print(f"new image size: {image.size}")
    
    image.save(image_path)

def process_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") and not filename.startswith("cr_"):
            image_path = os.path.join(directory, filename)
            # if image size greater than maxSize, resize it
            if os.path.getsize(image_path) > maxSize:
                print(f"file {image_path} is too large, resize it")
                resize_image(image_path,maxSize/os.path.getsize(image_path))

# Usage
process_images(imagesPath)