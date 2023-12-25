import os
import csv
import pycountry

csv_file = '../files/country game - no landmarks.csv'
inputMapPath = "../files/allmaps/"
outputMapPath = "../files/map/"


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
    if country_name == "United Arab Emirat":
        return "ae"
    if country_name == "Venezuela":
        return "ve"
    if country_name == "Vietnam":
        return "vn"

def copy_map_image(country_id, country_name, image_folder, origin_image_folder):
    #get the alpha2 code for the country
    country_code = get_iso_code(country_name)
    if not country_code:
        print(f"Could not find country code for {country_name}")
        return
    country_code = country_code.lower()
    image_path = os.path.join(image_folder, f"{country_id}_{country_name.replace(' ', '_')}_map.gif")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Copy the image in origin_image_folder/<country_code>/<country_code>_blu.gif to image_path
    origin_image_path = os.path.join(origin_image_folder, country_code, f"{country_code}_blu.gif")
    if os.path.exists(origin_image_path):
        with open(origin_image_path, 'rb') as origin_image_file:
            with open(image_path, 'wb') as image_file:
                image_file.write(origin_image_file.read())
        print(f"Image copied successfully as {image_path}")
    else:
        print(f"Image not found at {origin_image_path}")

def download_country_images(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        countryIndex = 0
        for row in reader:
            countryIndex+=1
            country = row[0]
            copy_map_image(countryIndex, country, outputMapPath, inputMapPath)


if __name__ == "__main__":
    download_country_images(csv_file)
