import os
import csv
import requests


csv_file = '../files/country_names.csv'
globePath = "../files/globe/"

def download_country_image(country_code, country_name,filename_suffix,orthographic_image_url,image_folder):

    image_path = os.path.join(image_folder,f"{country_code}_{country_name.replace(' ', '_')}_{filename_suffix}.png")
    # Ensure directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Download the image
    headers = {
        'User-Agent': 'game-country/1.0 (https://github.com/manaty/country-game)'
    }
    response = requests.get(orthographic_image_url,headers=headers)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully as {image_path}")
    else:
        print("Error downloading the image")


def get_map_image(country,imageType):
    # Wikimedia API endpoint
    endpoint = "https://en.wikipedia.org/w/api.php"

    # Define the parameters for the query
    params = {
        "action": "query",
        "format": "json",
        "titles": country,
        "prop": "images",
        "imlimit": "500"
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    # Extract the page ID to access the images
    page_id = next(iter(data['query']['pages']))
    images = data['query']['pages'][page_id]['images']

    # Find the orthographic projection image
    image = None
    countrylessImages = []
    for img in images:
        print(f"looking for {imageType} in {img['title']}")
        if imageType in (img['title']).lower():
            countrylessImages.append(img)
            print(f"Adding {imageType} image: {img['title']}")

    print(f"Found {len(countrylessImages)} {imageType} images")        
    
    if len(countrylessImages) > 1:
        for img in countrylessImages:
            if country.lower() in (img['title']).lower():
                print(f"Found {imageType} image for {country}: {img['title']}")
                image = img
                break
        if image is None:
            for img in countrylessImages:
                if country.lower()[:3]+" " in (img['title']).lower():
                    print(f"Found {imageType} image for {country}: {img['title']}")
                    image = img
                    break
    elif len(countrylessImages) == 1:
        image = countrylessImages[0]
    else:
        return f"{country} {imageType} image not found."

    # Get the image URL
    image_info_params = {
        "action": "query",
        "format": "json",
        "titles": image['title'],
        "prop": "imageinfo",
        "iiprop": "url"
    }

    image_info_response = requests.get(endpoint, params=image_info_params)
    image_info_data = image_info_response.json()
    image_page = next(iter(image_info_data['query']['pages'].values()))

    if 'imageinfo' in image_page:
        image_url = image_page['imageinfo'][0]['url']
        return image_url
    else:
        return "Image URL not found."

def svg_to_png_url(svg_url, width=550):
    """
    Convert a Wikimedia SVG URL to a PNG URL with the specified width.

    :param svg_url: The URL of the SVG image.
    :param width: The width in pixels for the PNG image.
    :return: The URL of the PNG image.
    """
    # Split the URL into parts
    parts = svg_url.split('/')

    # Add 'thumb' and the width specification in the correct position
    thumb_index = parts.index('commons') + 1
    parts.insert(thumb_index, 'thumb')
    
    # Add the width specification and change the extension to .png
    parts[-1] = f"{parts[-1]}/{width}px-{parts[-1]}.png"

    # Reconstruct the URL
    png_url = '/'.join(parts)

    return png_url

def download_country_images(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        countryIndex = 0
        for row in reader:
            countryIndex+=1
            country = row[0]
            # Look up the orthographic projection of Angola
            orthographic_image_url = get_map_image(country,"orthographic")
            print(orthographic_image_url)
            png_url = svg_to_png_url(orthographic_image_url)
            print(png_url)
            download_country_image(str(countryIndex),country,"globe",png_url,globePath)
            
            # Look up the orthographic projection of Angola
            map_image_url = get_map_image(country,"location")
            print(map_image_url)
            png_url = svg_to_png_url(map_image_url)
            print(png_url)
            download_country_image(str(countryIndex),country,"map",png_url,globePath)
            

if __name__ == "__main__":
    download_country_images(csv_file)