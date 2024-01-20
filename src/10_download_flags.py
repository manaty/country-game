import requests
import os
import csv
import pycountry
import cairosvg
from PIL import Image


csv_file = '../files/country game - no landmarks.csv'
outputMapPath = "../files/flag/"

def get_iso_code(country_name):
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2
    if country_name == "Czech Republic":
        return "cz"
    if country_name == "Iran":
        return "ir"
    if country_name == "Russia":
        return "ru"
    if country_name == "South Korea":
        return "kr"
    if country_name == "Tanzania":
        return "tz"
    if country_name == "Turkey":
        return "tr"
    if country_name == "United Arab Emirates":
        return "ae"
    if country_name == "Venezuela":
        return "ve"
    if country_name == "Vietnam":
        return "vn"

def download_flag(country_id, country_name, image_folder):
    #get the alpha2 code for the country
    country_code = get_iso_code(country_name)
    if not country_code:
        print(f"Could not find country code for {country_name}")
        return
    country_code = country_code.lower()
    svg_url = f"https://flagicons.lipis.dev/flags/4x3/{country_code}.svg"
    image_svg_path = os.path.join(image_folder, f"{country_id}_{country_name.replace(' ', '_')}_flag.svg")
    image_png_path = os.path.join(image_folder, f"{country_id}_{country_name.replace(' ', '_')}_flag.png")
    os.makedirs(os.path.dirname(image_svg_path), exist_ok=True)

    print(f"Downloading image for {country_name} from {svg_url}")
    #download the image from the url
    response = requests.get(svg_url)
    with open(image_svg_path, 'wb') as file:
        file.write(response.content)

    # Resize the image 
    cairosvg.svg2png(url=image_svg_path, write_to=image_png_path, output_width=400, output_height=300)
    img = Image.open(image_png_path)
    img = img.resize((352,228), Image.LANCZOS)
    flag = Image.new('RGB', (356, 232), '#000000')
    #add border
    flag.paste(img, (2, 2))
    flag.save(image_png_path, optimize=True, scale=True)
    print(f"Image resized to 232x356 pixels")

def download_country_flags(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        countryIndex = 0
        for row in reader:
            countryIndex+=1
            country = row[0]
            download_flag(countryIndex, country, outputMapPath)


if __name__ == "__main__":
    download_country_flags(csv_file)
