"""
add_characters_to_json.py
Author: RSGrizz
Date: 3/12/2025
Location: shakespeare_forensics_project/scripts/add_characters_to_json.py

Scrapes character names from a GitHub repository and populates the characters.json files.
"""

import json
import os
import requests
from bs4 import BeautifulSoup
import re
import argparse  # Import the argparse module

def is_file_empty(file_path):
    """Check if a file is empty"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return not bool(data)  # Check if the dictionary is empty
    except Exception:
        return True  # Treat as empty if there's an error

def add_characters_to_json(directory, force):
    """Adds character data to characters.json, scraping from MIT if empty or if force is True."""
    # Ensure directory exists
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    # Construct the file path
    file_path = os.path.join(directory, "characters.json")

    # Check if the file exists
    file_exists = os.path.exists(file_path)

    if force or (file_exists and is_file_empty(file_path)):
        # Extract play name from directory
        play_name = os.path.basename(directory)

        # Scrape character names from MIT Shakespeare website
        characters = scrape_character_names(play_name)

        if characters:
            data = {}
            for character in characters:
                data[character] = {
                    "description": "To be added",
                    "modern_role": "To be added",
                    "department": "To be added",
                    "location": "To be added"
                }

            # Write the updated data back to the file
            with open(file_path, 'w', encoding='utf-8') as f:  # Specify encoding
                json.dump(data, f, indent=4)
            print(f"Successfully added characters to {file_path}")
        else:
            print(f"Could not scrape data from {play_name}")
    else:
        print(f"Characters already exist in {file_path}")

def scrape_character_names(play_name):
    """Scrape character names from the given file"""
    base_url = "https://raw.githubusercontent.com/TheMITTech/shakespeare/master/characters"
    url = f"{base_url}/{play_name}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        character_names = list(data.keys())  # Extract character names from JSON keys
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

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Populate characters.json files with character names from a GitHub repository.")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing files.")
    args = parser.parse_args()

    # List of directories to process
    directories = [
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Alls_Well_That_Ends_Well",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Antony_and_Cleopatra",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/As_You_Like_It",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/A_Midsummer_Nights_Dream",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Coriolanus",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Cymbeline",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Hamlet",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_IV_Part_1",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_IV_Part_2",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_V",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_VIII",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_VI_Part_1",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_VI_Part_2",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Henry_VI_Part_3",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Julius_Caesar",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/King_John",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/King_Lear",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Loves_Labours_Lost",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Macbeth",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Measure_for_Measure",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Much_Ado_About_Nothing",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Othello",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Pericles_Prince_of_Tyre",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Richard_II",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Richard_III",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Romeo_and_Juliet",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Comedy_of_Errors",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Merchant_of_Venice",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Merry_Wives_of_Windsor",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Taming_of_the_Shrew",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Tempest",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Two_Noble_Kinsmen",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/The_Winters_Tale",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Timon_of_Athens",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Titus_Andronicus",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Troilus_and_Cressida",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Twelfth_Night",
        "C:/Users/ADMIN/Source/Repos/shakespeare_forensics_project/desktop_creator/data/static/plays/Two_Gentlemen_of_Verona"
    ]

    # Process each directory
    for directory in directories:
        add_characters_to_json(directory, args.force)
