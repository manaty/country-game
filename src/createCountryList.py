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
    prompt_user = f"""Please provide JSON formated information for the following countries: {countries_list},
    """

    completion = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": prompt_user},
    ],
    max_tokens=5000,  # Increased to accommodate longer response
    n=1,
    stop=None,
    temperature=0)

    # Extracting the response content
    response_text = completion.choices[0].message.content

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
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for country in countries:
            row = [country]
            landmarks = landmarks_data.get(country, {})
            for landmark in landmarks:
                row.append(landmark.get("name", "") + ", " + landmark.get("location", ""))
            writer.writerow(row)

# Path to your input and output CSV files
input_csv_file = '../files/country_names.csv'
output_csv_file = '../files/country_landmarks.csv'

# Reading countries from the input CSV file
countries = get_countries_from_csv(input_csv_file)

# Fetching landmarks data
landmarks_data = fetch_country_data(countries)

# Writing landmarks to the output CSV file
write_landmarks_to_csv(countries, landmarks_data, output_csv_file)