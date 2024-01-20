import csv
import re
import requests
import wikipedia
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))

csv_file = '../files/country_landmarks.csv'
imagesPath = "../files/images/"

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

def askChatGPT(country,landmark):
    # Crafting the prompt to ask for landmarks of the countries in input
    prompt_user = f"Please provide the url of an image of the famous landmark `{landmark}` of the country `{country}`."
    print(prompt_user)

    completion = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "user", "content": prompt_user},
    ],
    max_tokens=2000,  # Increased to accommodate longer response
    n=1,
    stop=None,
    temperature=0)

    # Extracting the response content
    response_text = completion.choices[0].message.content
    print(response_text)

    return response_text


def download_landmarks_images(csv_file):
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
                print(f"Searching for {landmark_name} using wikipedia")
                try:
                    page = wikipedia.page(f"{landmark_name}, {country}")
                    if page.images:
                        print(f"Found {len(page.images)} images in wikipedia for {landmark_name}")
                        # Print all the page.images URLs
                        for image_url in page.images:
                            print(f"image url: {image_url}")
                            if image_url.lower().endswith('.jpg') and 'location_map' not in image_url:
                                print(f"Downloading image for {landmark_name} and url {image_url}")
                                download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                                # continue with the next landmark
                                continue
                    else:
                        print(f"No images found for {landmark_name}")
                except wikipedia.exceptions.PageError:
                    print(f"No Wikipedia page found for {landmark_name}")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"Disambiguation error for {landmark_name}, possible options: {e.options}")
                    page = wikipedia.page(landmark_name + ' ' + country)
                    try:
                        page = wikipedia.page(landmark_name)
                        if page.images:
                            # Print all the page.images URLs
                            for image_url in page.images:
                                if image_url.lower().endswith('.jpg') and 'location_map' not in image_url:
                                    print(f"Downloading image for {landmark_name} and url {image_url}")
                                    download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                                    # continue with the next landmark
                                    continue
                        else:
                            print(f"No images found for {landmark_name}")
                    except wikipedia.exceptions.PageError:
                        print(f"No Wikipedia page found for {landmark_name}")
                    except wikipedia.exceptions.DisambiguationError as e:
                        print(f"Disambiguation error for {landmark_name}, possible options: {e.options}")
                    

if __name__ == "__main__":
    download_landmarks_images(csv_file)
