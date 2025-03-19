"""
Generate_Character_Data.py
Created by RSGrizz
Date: March 2024
Version: 1.0

Interactive generator for character data files within play folders.
Allows user to select play, city, and generates appropriate modern mappings.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List
import random
from datetime import datetime

class CharacterDataGenerator:
    def __init__(self):
        self.base_dir = Path("desktop_creator/data/static/plays")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = logging.getLogger(__name__)
        
        # Initialize default cities in case file loading fails
        self.default_cities = [
            "New York City",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose"
        ]
        
        # Load available cities and other data
        self.cities = self._load_cities()
        self.titles = self._load_business_titles()
        
        # Default titles in case file loading fails
        self.default_titles = {
            "executive": [
                "CEO",
                "CFO",
                "COO",
                "CTO",
                "President",
                "Vice President",
                "Director",
                "Executive Director"
            ],
            "management": [
                "Senior Manager",
                "Department Manager",
                "Program Director",
                "Project Manager"
            ],
            "department": [
                "Operations",
                "Finance",
                "Technology",
                "Sales",
                "Marketing",
                "Legal",
                "Human Resources",
                "Research & Development"
            ]
        }

    def _load_cities(self) -> List[str]:
        """Load available cities from static data."""
        try:
            cities_file = Path("desktop_creator/data/static/modern_mappings/cities/major_cities.json")
            if not cities_file.exists():
                self.logger.warning("Cities file not found. Using default cities.")
                return self.default_cities
                
            with open(cities_file, 'r') as f:
                city_data = json.load(f)
                cities = self._extract_city_names(city_data)
                return cities if cities else self.default_cities
        except Exception as e:
            self.logger.error(f"Error loading cities: {e}")
            return self.default_cities

    def _extract_city_names(self, city_data: Dict) -> List[str]:
        """Extract city names from city data structure."""
        cities = []
        try:
            regions = city_data.get("data", {}).get("regions", {})
            for region in regions.values():
                if "major_cities" in region:
                    for city_info in region["major_cities"].values():
                        cities.append(city_info.get("name", ""))
        except Exception as e:
            self.logger.error(f"Error extracting city names: {e}")
        return sorted([city for city in cities if city])

    def _load_business_titles(self) -> Dict:
        """Load available business titles."""
        try:
            titles_file = Path("desktop_creator/data/static/modern_mappings/business/titles.json")
            if not titles_file.exists():
                self.logger.warning("Titles file not found. Using default titles.")
                return self.default_titles
                
            with open(titles_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading titles: {e}")
            return self.default_titles

    def get_play_list(self) -> List[str]:
        """Get list of all plays."""
        plays = [
            "Macbeth",
            "Hamlet",
            "Romeo_and_Juliet",
            "Othello",
            "King_Lear",
            "Julius_Caesar",
            "A_Midsummer_Nights_Dream",
            "The_Tempest",
            "Twelfth_Night",
            "Much_Ado_About_Nothing"
        ]
        return sorted(plays)

    def prompt_for_play(self) -> str:
        """Prompt user to select a play."""
        plays = self.get_play_list()
        print("\nAvailable plays:")
        for i, play in enumerate(plays, 1):
            print(f"{i}. {play}")
        
        while True:
            try:
                choice = int(input("\nSelect a play (enter number): "))
                if 1 <= choice <= len(plays):
                    return plays[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def prompt_for_city(self) -> str:
        """Prompt user to select a primary city."""
        cities = self.cities
        print("\nAvailable cities:")
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city}")
        
        while True:
            try:
                choice = int(input("\nSelect primary city (enter number): "))
                if 1 <= choice <= len(cities):
                    return cities[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def check_existing_data(self, play_name: str) -> bool:
        """Check if character data already exists for the play."""
        character_file = self.base_dir / play_name / "characters.json"
        if character_file.exists():
            while True:
                response = input(f"\nCharacter data already exists for {play_name}. Override? (y/n): ").lower()
                if response in ['y', 'n']:
                    return response == 'y'
                print("Please enter 'y' or 'n'.")
        return True

    def generate_character_data(self, play_name: str, city: str) -> Dict:
        """Generate character data with user input."""
        print(f"\nGenerating character data for {play_name} set in {city}")
        
        # Get number of characters
        while True:
            try:
                num_characters = int(input("\nHow many characters to generate? "))
                if num_characters > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

        characters = {}
        for i in range(num_characters):
            char_name = input(f"\nEnter name for character {i+1}: ").upper()
            role = input(f"Enter original role for {char_name}: ")
            
            # Randomly assign modern details
            modern_role = random.choice(self.titles.get("executive", self.default_titles["executive"]))
            department = random.choice(self.titles.get("department", self.default_titles["department"]))
            
            characters[char_name] = {
                "original_role": role,
                "modern_role": {
                    "title": modern_role,
                    "organization": f"{city} Global Enterprises",
                    "department": department,
                    "location": city
                },
                "relationships": {
                    "allies": [],
                    "opponents": [],
                    "subordinates": []
                }
            }

        return {
            "metadata": {
                "play_name": play_name,
                "generated_by": "RSGrizz",
                "generated_date": self.timestamp,
                "version": "1.0",
                "primary_location": city
            },
            "characters": characters
        }

    def save_character_data(self, play_name: str, data: Dict):
        """Save character data to file."""
        play_dir = self.base_dir / play_name
        play_dir.mkdir(parents=True, exist_ok=True)
        
        character_file = play_dir / "characters.json"
        with open(character_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nCharacter data saved to {character_file}")

def main():
    """Main execution function."""
    print("\nCharacter Data Generator for Shakespeare Forensics Project")
    print("Created by RSGrizz")
    print(f"Version 1.0 - {datetime.now().strftime('%B %Y')}")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    generator = CharacterDataGenerator()
    
    # Get user input
    play_name = generator.prompt_for_play()
    
    # Check for existing data
    if not generator.check_existing_data(play_name):
        print("\nOperation cancelled.")
        return
    
    # Get city selection
    city = generator.prompt_for_city()
    
    # Generate and save data
    character_data = generator.generate_character_data(play_name, city)
    generator.save_character_data(play_name, character_data)
    
    print("\nCharacter data generation complete!")

if __name__ == "__main__":
    main()
