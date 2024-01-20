import csv
import openai
from openai import OpenAI
import requests
import os

csv_file = '../files/country_landmarks.csv'
imagesPath = "../files/images/"


client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))


def download_image(url, country_name, landmark_name):
    headers = {
        'User-Agent': 'game-country/1.0 (https://github.com/manaty/country-game)'
    }

    # Construct the relative path
    relative_path = os.path.join(imagesPath,f"{country_name+'_'+landmark_name.replace(' ', '_')}.jpg")
    
    if os.path.exists(relative_path):
        print(f"file {relative_path} already exists, skip the image download")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)

    # Download and save the image
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(relative_path, 'wb') as file:
            print(f"Size of content: {len(response.content)} bytes")
            file.write(response.content)

def fetch_landmark_image(country_name,landmark_name):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A photo without any text of the landmark '{landmark_name}' of the country '{country_name}'",
            size="1792x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    except openai.OpenAIError as e:
        print(e)
    
    return None


def generate_landmarks_images(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        countryIndex = 0
        for row in reader:
            countryIndex+=1
            country = row[0]
            landmarks = row[1:]
            index=0

            for landmark in landmarks:
                index+=1
                landmark_name = landmark.split(',')[0].strip()
                # if there is already an image for this landmark, skip it
                imageFilename = f"{countryIndex}_{country}_{index}_{landmark_name.replace(' ', '_')}.jpg"
                if os.path.exists(os.path.join(imagesPath,imageFilename)):
                    print(f"file {imageFilename} already exists, skip the image download")
                    continue
                print(f"generating for {landmark_name} using dall-e")
                image_url = fetch_landmark_image(landmark_name, country)
                if image_url is not None:
                    # Print all the page.images URLs
                    print(f"Downloading image for {landmark_name} and url {image_url}")
                    download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                    # continue with the next landmark
                    continue
                else:
                    print(f"No image generated for {landmark_name}")
               
                    
if __name__ == "__main__":
    generate_landmarks_images(csv_file)
