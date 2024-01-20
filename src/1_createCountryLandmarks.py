import csv
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))


prompt_system = """Fetch for the provided list of countries their four main landmarks, 
    each landmark followed by its closest major city.
    Return the result as a JSON object where each property is a country name and the value is an array of landmarks.
    for each landmark provide the name and the closest city stored in a key "location", no need for a description
    """
def fetch_country_data(countries):
    # Joining all country names into a single string, each on a new line
    countries_list = "\n".join(countries)

    # Crafting the prompt to ask for landmarks of the countries in input
    prompt_user = f"Please provide JSON formated information for the following countries: {countries_list}"
    print(prompt_user)
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": prompt_user},
    ],
    max_tokens=2000,  # Increased to accommodate longer response
    n=1,
    stop=None,
    temperature=0)

    # Extracting the response content
    response_text = completion.choices[0].message.content
    print(response_text)
    # Parsing the JSON response
    try:
        landmarks_data = json.loads(response_text)
    except json.JSONDecodeError:
        landmarks_data = {}

    return landmarks_data

def get_countries_from_csv(file_path):
    countries = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Checking if the row is not empty
                countries.append(row[0])  # Assuming country name is in the first column
    return countries

def write_landmarks_to_csv(countries, landmarks_data, output_file):
    with open(output_file, 'a', newline='') as csvfile:  # Use 'a' mode to append instead of 'w' mode to overwrite
        writer = csv.writer(csvfile)
        for country in countries:
            row = [country]
            landmarks = landmarks_data.get(country, {})
            for landmark in landmarks:
                row.append(landmark.get("name", "") + ", " + landmark.get("location", ""))
            writer.writerow(row)

# Function to get countries already processed in the output CSV file
def get_processed_countries(output_file):
    processed_countries = set()
    with open(output_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Checking if the row is not empty
                processed_country = row[0]  # Assuming country name is in the first column
                processed_countries.add(processed_country)
    return processed_countries

# Path to your input and output CSV files
input_csv_file = '../files/country game - no landmarks.csv'
output_csv_file = '../files/country_landmarks.csv'

# Reading countries from the input CSV file
countries = get_countries_from_csv(input_csv_file)
print(f"# countries in input file: {len(countries)}")

# Reading countries already processed
processed_countries = get_processed_countries(output_csv_file)
print(f"# countries already processed: {len(processed_countries)}")

# Removing already processed countries from the list
countries = [country for country in countries if country not in processed_countries]
print(f"# fetching landmarks for {countries} ")

if(len(countries)>0):
    # Fetching landmarks data and writing landmarks to the output CSV file in batches of 10 countries
    batch_size = 10
    for i in range(0, len(countries), batch_size):
        batch_countries = countries[i:i+batch_size]
        landmarks_data = fetch_country_data(batch_countries)
        write_landmarks_to_csv(batch_countries, landmarks_data, output_csv_file)
