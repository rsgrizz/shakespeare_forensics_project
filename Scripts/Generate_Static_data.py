import json
import random
from pathlib import Path

def create_fake_companies(num_companies=100):
    """Generate a list of fake company data."""
    companies = []
    industries = ["Technology", "Finance", "Consulting", "Manufacturing", "Healthcare",
                  "Software", "Venture Capital", "Logistics", "Marketing", "Energy"]
    locations = ["New York", "San Francisco", "Chicago", "Houston", "Boston",
                 "Seattle", "Menlo Park", "Memphis", "Los Angeles", "San Diego"]

    for i in range(num_companies):
        company = {
            "name": f"Company {i+1}",
            "industry": random.choice(industries),
            "location": random.choice(locations)
        }
        companies.append(company)
    return companies

def create_fake_titles(num_titles=100):
    """Generate a list of fake job titles."""
    titles = [
        f"Job Title {i+1}" for i in range(num_titles)
    ]
    return titles

def create_play_characters(play_name):
    """Create character data for a play."""
    # This is a placeholder - replace with more sophisticated logic
    characters = {
        "CHARACTER_1": {
            "description": "Generic Character",
            "modern_role": "Employee",
            "department": "General",
            "location": "Anytown"
        },
        "CHARACTER_2": {
            "description": "Generic Character",
            "modern_role": "Manager",
            "department": "Management",
            "location": "Anytown"
        }
    }
    return characters

def write_json_file(data, filepath):
    """Write data to a JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated: {filepath}")

if __name__ == "__main__":
    import random

    # List of plays
    plays = [
        "Alls_Well_That_Ends_Well",
        "Antony_and_Cleopatra",
        "As_You_Like_It",
        "A_Midsummer_Nights_Dream",
        "Coriolanus",
        "Cymbeline",
        "Hamlet",
        "Henry_IV_Part_1",
        "Henry_IV_Part_2",
        "Henry_V",
        "Henry_VIII",
        "Henry_VI_Part_1",
        "Henry_VI_Part_2",
        "Henry_VI_Part_3",
        "Julius_Caesar",
        "King_John",
        "King_Lear",
        "Loves_Labours_Lost",
        "Macbeth",
        "Measure_for_Measure",
        "Much_Ado_About_Nothing",
        "Othello",
        "Pericles_Prince_of_Tyre",
        "Richard_II",
        "Richard_III",
        "Romeo_and_Juliet",
        "The_Comedy_of_Errors",
        "The_Merchant_of_Venice",
        "The_Merry_Wives_of_Windsor",
        "The_Taming_of_the_Shrew",
        "The_Tempest",
        "The_Two_Noble_Kinsmen",
        "The_Winters_Tale",
        "Timon_of_Athens",
        "Titus_Andronicus",
        "Troilus_and_Cressida",
        "Twelfth_Night",
        "Two_Gentlemen_of_Verona"
    ]

    # Create fake data
    companies = create_fake_companies()
    titles = create_fake_titles()

    # Define base directory
    base_dir = "desktop_creator/data/static/plays"

    # Generate character data for each play
    for play in plays:
        characters = create_play_characters(play)
        characters_path = f"{base_dir}/{play}/characters.json"
        write_json_file(characters, characters_path)

    # Define filepaths for companies and titles
    companies_path = "desktop_creator/data/static/modern_mappings/business/companies.json"
    titles_path = "desktop_creator/data/static/modern_mappings/business/titles.json"

    # Write to JSON files
    write_json_file(companies, companies_path)
    write_json_file(titles, titles_path)

    print("\nJSON data generation complete!")
