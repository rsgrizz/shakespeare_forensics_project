"""
generate_play_data.py
Author: RSGrizz
Date: 3/12/2025
Location: shakespeare_forensics_project/scripts/generate_play_data.py

Generates character data, call data, and contacts for a specific play, and scrapes the full play text.
"""

import json
import os
import requests
from bs4 import BeautifulSoup
import re
import random
from datetime import datetime, timedelta
import argparse  # Import the argparse module

def get_all_plays():
    """Get a list of all play names from the GitHub repository."""
    base_url = "https://raw.githubusercontent.com/TheMITTech/shakespeare/master/characters/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Extract all JSON files
        pattern = re.compile(r'href="([^"]+\.json)"')
        matches = pattern.findall(response.text)
        
        play_names = [match.replace(".json", "") for match in matches]
        return play_names
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Error getting play list: {e}")
        return []

def scrape_character_names(play_name):
    """Scrape character names from a JSON file in the GitHub repository."""
    base_url = "https://raw.githubusercontent.com/TheMITTech/shakespeare/master/characters/"
    url = f"{base_url}{play_name}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        character_names = list(data.keys())
        return character_names
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        return []
    except Exception as e:
        print(f"Error scraping character names: {e}")
        return []

def modernize_character(character_name, city_data):
    """Modernize character information"""
    #Get random title
    title = random.choice(city_data["titles"])
    #Get random area code
    area_code = random.choice(city_data["area_codes"])
    modern_details = {
        "title": title,
        "company": "Acme Consulting",
        "location": city_data["city"],
        "phone": f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "email": f"{character_name.lower().replace(' ', '.')}@acme.com"
    }
    return modern_details

def generate_call_data(characters):
    """Generate call data between characters"""
    call_data = []
    for i in range(len(characters)):
        for j in range(i + 1, len(characters)):
            character1 = characters[i]
            character2 = characters[j]
            
            # Generate a few calls between each pair of characters
            num_calls = random.randint(1, 3)
            for _ in range(num_calls):
                call = {
                    "from": character1,
                    "to": character2,
                    "timestamp": datetime.now().isoformat(),
                    "duration": random.randint(60, 300)
                }
                call_data.append(call)
    return call_data

def generate_contact_data(characters, city_data):
    """Generate contact data for each character"""
    contacts = {}
    for character in characters:
        phone = f"{random.choice(city_data['area_codes'])}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        contacts[character] = {
            "phone": phone,
            "email": f"{character.lower().replace(' ', '.')}@example.com",
            "title": random.choice(city_data["titles"]),
            "company": "Example Corp"
        }
    return contacts

def main():
    """Main function to generate data for all plays"""
    # Load City Information
    with open('desktop_creator/data/static/modern_mappings/locations/cities.json', 'r') as f:
        city_data_list = json.load(f)
        
    # Get all play names from the GitHub repository
    all_plays = get_all_plays()
    
    # Process each play
    for play_name in all_plays:
        # Create directory path
        directory = f"desktop_creator/data/static/plays/{play_name}"
        
        # Create character list
        characters = scrape_character_names(play_name)
        
        if characters:
            print(f"Successfully scraped characters from {play_name}")
            
            # Modernize characters
            modernized_characters = {}
            for character in characters:
                #Get the city
                city_data = random.choice(city_data_list)
                modernized_characters[character] = modernize_character(character, city_data)
                
            # Generate call data
            call_data = generate_call_data(characters)
            
            # Generate contact data
            #Get the city
            city_data = random.choice(city_data_list)
            contact_data = generate_contact_data(characters, city_data)
            
            # Save all data to a JSON file
            play_data = {
                "characters": modernized_characters,
                "call_data": call_data,
                "contact_data": contact_data
            }
            
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            # Write the data to the json file
            with open(os.path.join(directory, "data.json"), "w") as f:
                json.dump(play_data, f, indent=4)
            
            print(f"Successfully generated data for {play_name} and saved to {directory}/data.json")
        else:
            print(f"Could not scrape data from {play_name}")

if __name__ == "__main__":
    main()
