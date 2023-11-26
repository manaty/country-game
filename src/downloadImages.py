import csv
import requests
import wikipedia
import os

csv_file = '../files/country_landmarks.csv'
imagesPath = "../files/images/"

def download_image(url, country_name, landmark_name):
    headers = {
        'User-Agent': 'game-country/1.0 (https://github.com/manaty/country-game)'
    }

    # Construct the relative path
    relative_path = os.path.join(imagesPath,f"{country_name+'_'+landmark_name.replace(' ', '_')}.jpg")

    # Ensure directory exists
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)

    # Download and save the image
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(relative_path, 'wb') as file:
            print(f"Size of content: {len(response.content)} bytes")
            file.write(response.content)


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
                print(f"Searching for {landmark_name} using wikipedia")
                try:
                    page = wikipedia.page(landmark_name)
                    if page.images:
                        # Print all the page.images URLs
                        for image_url in page.images:
                            if image_url.lower().endswith('.jpg') and 'location_map' not in image_url:
                                print(f"Downloading image for {landmark_name} and url {image_url}")
                                download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                                # continue with the next landmark
                                break
                    else:
                        print(f"No images found for {landmark_name}")
                except wikipedia.exceptions.PageError:
                    print(f"No Wikipedia page found for {landmark_name}")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"Disambiguation error for {landmark_name}, possible options: {e.options}")

                    

if __name__ == "__main__":
    download_landmarks_images(csv_file)
