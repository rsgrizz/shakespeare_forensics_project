"""
generate_play_data.py
Author: RSGrizz
Date: 3/12/2025
Location: shakespeare_forensics_project/desktop_creator/src/generate_play_data.py
"""

import json
import os
from bs4 import BeautifulSoup
import re
import random
from datetime import datetime, timedelta
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Industry definitions
INDUSTRIES = {
    "ROYAL": {
        "companies": [
            {"name": "Crown Holdings International", "domain": "crownholdings.com"},
            {"name": "Dynasty Global Investments", "domain": "dynastyglobal.com"},
            {"name": "Sovereign Wealth Partners", "domain": "sovereignwealth.com"},
            {"name": "Monarch Capital Group", "domain": "monarchcap.com"},
            {"name": "Imperial Ventures", "domain": "imperialventures.com"},
            {"name": "Regency Financial", "domain": "regencyfinancial.com"}
        ],
        "titles": [
            "Chief Executive Officer",
            "Chairman of the Board",
            "President",
            "Executive Chairman",
            "Managing Director",
            "Global President"
        ]
    },
    "NOBLE": {
        "companies": [
            {"name": "Heritage Private Equity", "domain": "heritagepe.com"},
            {"name": "Noble & Sterling Partners", "domain": "noblesterling.com"},
            {"name": "Pinnacle Investment Group", "domain": "pinnacleinv.com"},
            {"name": "Elite Management Associates", "domain": "elitema.com"},
            {"name": "Legacy Capital Partners", "domain": "legacycap.com"},
            {"name": "Prestige Holdings", "domain": "prestigeholdings.com"}
        ],
        "titles": [
            "Senior Partner",
            "Managing Partner",
            "Executive Director",
            "Senior Vice President",
            "Chief Investment Officer",
            "Portfolio Director"
        ]
    },
    "MILITARY": {
        "companies": [
            {"name": "Vanguard Defense Technologies", "domain": "vanguardtech.com"},
            {"name": "Strategic Operations Group", "domain": "stratops.com"},
            {"name": "Guardian Security International", "domain": "guardiansi.com"},
            {"name": "Sentinel Defense Systems", "domain": "sentineldef.com"},
            {"name": "Aegis Protection Services", "domain": "aegisprotect.com"},
            {"name": "Fortress Global Security", "domain": "fortresssecurity.com"}
        ],
        "titles": [
            "Security Director",
            "Chief Security Officer",
            "Operations Director",
            "Strategic Defense Coordinator",
            "Head of Special Operations",
            "Security Operations Manager"
        ]
    },
    "ADVISORY": {
        "companies": [
            {"name": "Wisdom Tree Consulting", "domain": "wisdomtree.com"},
            {"name": "Strategic Minds Group", "domain": "strategicminds.com"},
            {"name": "Insight Partners LLC", "domain": "insightpartners.com"},
            {"name": "Maven Strategy Consultants", "domain": "mavenstrategy.com"},
            {"name": "Catalyst Advisory Group", "domain": "catalystadvisory.com"},
            {"name": "Nexus Consulting Partners", "domain": "nexuscp.com"}
        ],
        "titles": [
            "Senior Strategy Advisor",
            "Management Consultant",
            "Chief Strategy Officer",
            "Principal Consultant",
            "Senior Advisor",
            "Executive Consultant"
        ]
    },
    "DIPLOMATIC": {
        "companies": [
            {"name": "Global Relations Institute", "domain": "globalrelations.org"},
            {"name": "International Dialog Group", "domain": "idgroup.com"},
            {"name": "Unity Diplomatic Solutions", "domain": "unitydiplomacy.com"},
            {"name": "Alliance International", "domain": "allianceintl.com"},
            {"name": "Concord Mediation Group", "domain": "concordmediation.com"},
            {"name": "Bridge Builders Associates", "domain": "bridgebuilders.com"}
        ],
        "titles": [
            "International Relations Director",
            "Diplomatic Affairs Manager",
            "Public Relations Director",
            "External Relations Head",
            "International Development Director",
            "Global Communications Director"
        ]
    },
    "MERCHANT": {
        "companies": [
            {"name": "Commerce & Trade Solutions", "domain": "commercetrade.com"},
            {"name": "Market Dynamics International", "domain": "marketdyn.com"},
            {"name": "Trade Winds Corporation", "domain": "tradewinds.com"},
            {"name": "Merchant's Exchange Group", "domain": "merchantsexchange.com"},
            {"name": "Global Trade Partners", "domain": "globaltradepart.com"},
            {"name": "Commerce Link Worldwide", "domain": "commercelink.com"}
        ],
        "titles": [
            "Business Development Director",
            "Trade Relations Manager",
            "Commercial Director",
            "Chief Commercial Officer",
            "Trading Operations Manager",
            "Market Development Director"
        ]
    },
    "RELIGIOUS": {
        "companies": [
            {"name": "Faith Heritage Foundation", "domain": "faithheritage.org"},
            {"name": "Spirit & Soul Wellness", "domain": "spiritsoul.org"},
            {"name": "Divine Guidance Counsel", "domain": "divineguidance.org"},
            {"name": "Sacred Trust Services", "domain": "sacredtrust.org"},
            {"name": "Spiritual Wellness Institute", "domain": "spiritualwellness.org"},
            {"name": "Harmony & Peace Foundation", "domain": "harmonypeace.org"}
        ],
        "titles": [
            "Spiritual Advisor",
            "Wellness Director",
            "Program Director",
            "Community Relations Director",
            "Guidance Counselor",
            "Outreach Coordinator"
        ]
    },
    "ACADEMIC": {
        "companies": [
            {"name": "Knowledge Quest Institute", "domain": "kqi.edu"},
            {"name": "Scholars Academy Group", "domain": "scholarsacademy.edu"},
            {"name": "Wisdom Gate University", "domain": "wisdomgate.edu"},
            {"name": "Learning Tree Institute", "domain": "learningtree.edu"},
            {"name": "Academic Excellence Center", "domain": "academicexcellence.edu"},
            {"name": "Mind & Matter Research", "domain": "mindmatter.edu"}
        ],
        "titles": [
            "Research Director",
            "Academic Dean",
            "Department Chair",
            "Research Fellow",
            "Professor",
            "Education Director"
        ]
    },
    "ARTISTIC": {
        "companies": [
            {"name": "Creative Minds Studio", "domain": "creativeminds.art"},
            {"name": "Artistic Vision Group", "domain": "artisticvision.com"},
            {"name": "Performance Arts Collective", "domain": "performarts.com"},
            {"name": "Dramatic Works Productions", "domain": "dramaticworks.com"},
            {"name": "Stage & Screen Studios", "domain": "stagescreen.com"},
            {"name": "Arts & Entertainment Global", "domain": "artsglobal.com"}
        ],
        "titles": [
            "Creative Director",
            "Artistic Director",
            "Performance Director",
            "Production Manager",
            "Entertainment Director",
            "Arts Program Manager"
        ]
    }
}

def get_character_type(character_name, character_lines):
    """Determine character type based on name and context"""
    name_upper = character_name.upper()
    
    # Royal characters
    if any(title in name_upper for title in ["KING", "QUEEN", "PRINCE", "DUKE", "PRINCESS"]):
        return "ROYAL"
    
    # Military characters
    if any(title in name_upper for title in ["CAPTAIN", "GENERAL", "SOLDIER", "LIEUTENANT", "COMMANDER"]):
        return "MILITARY"
        
    # Noble characters
    if any(title in name_upper for title in ["LORD", "LADY", "COUNT", "BARON", "SIR", "DUCHESS"]):
        return "NOBLE"
    
    # Religious characters
    if any(word in name_upper for word in ["PRIEST", "FRIAR", "MONK", "NUN", "CARDINAL"]):
        return "RELIGIOUS"
    
    # Academic characters
    if any(word in name_upper for word in ["SCHOLAR", "STUDENT", "TEACHER", "TUTOR"]):
        return "ACADEMIC"
    
    # Artistic characters
    if any(word in name_upper for word in ["PLAYER", "MUSICIAN", "ARTIST", "FOOL", "CLOWN"]):
        return "ARTISTIC"
    
    # Advisors/counselors
    if any(word in name_upper for word in ["POLONIUS", "COUNSELLOR", "ADVISOR"]):
        return "ADVISORY"
    
    # Diplomatic characters
    if "AMBASSADOR" in name_upper or "MESSENGER" in name_upper:
        return "DIPLOMATIC"
    
    # Default to merchant/civilian
    return "MERCHANT"

def scrape_character_names(play_name, full_path):
    """Extract character names from the play's HTML file."""
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        characters = set()
        for speaker in soup.find_all('b'):
            name = speaker.text.strip()
            if (name and 
                not name.startswith('First') and 
                not name.startswith('Second') and
                not name in ['All', 'Both', 'Ghost']):
                characters.add(name)

        return list(characters)
    except FileNotFoundError:
        print(f"Play text file not found: {full_path}")
        return []
    except Exception as e:
        print(f"Error scraping play text: {e}")
        return []

def modernize_character(character_name, city_data):
    """Modernize character information with more varied companies"""
    # Determine character type
    char_type = get_character_type(character_name, [])
    
    # Get industry data
    industry = INDUSTRIES[char_type]
    
    # Select company and title
    company_info = random.choice(industry["companies"])
    title = random.choice(industry["titles"])
    
    # Clean the character name for email
    clean_name = re.sub(r'[^\w\s-]', '', character_name.lower())
    email_name = clean_name.replace(' ', '.')
    
    area_code = random.choice(city_data["area_codes"])
    
    modern_details = {
        "title": title,
        "company": company_info["name"],
        "industry": char_type.lower().capitalize(),
        "location": city_data["city"],
        "phone": f"{area_code}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "email": f"{email_name}@{company_info['domain']}"
    }
    return modern_details

def generate_call_data(characters):
    """Generate call data between characters"""
    call_data = []
    for i in range(len(characters)):
        for j in range(i + 1, len(characters)):
            character1 = characters[i]
            character2 = characters[j]
            num_calls = random.randint(1, 3)
            for _ in range(num_calls):
                days_ago = random.randint(0, 7)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                call_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
                
                call = {
                    "from": character1,
                    "to": character2,
                    "timestamp": call_time.isoformat(),
                    "duration": random.randint(60, 300)
                }
                call_data.append(call)
    return call_data

def generate_contact_data(characters, city_data):
    """Generate contact data for each character"""
    contacts = {}
    for character in characters:
        char_type = get_character_type(character, [])
        industry = INDUSTRIES[char_type]
        company_info = random.choice(industry["companies"])
        
        clean_name = re.sub(r'[^\w\s-]', '', character.lower())
        email_name = clean_name.replace(' ', '.')
        
        phone = f"{random.choice(city_data['area_codes'])}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        contacts[character] = {
            "phone": phone,
            "email": f"{email_name}@{company_info['domain']}",
            "title": random.choice(industry["titles"]),
            "company": company_info["name"],
            "industry": char_type.lower().capitalize()
        }
    return contacts

def main():
    """Main function to generate data for all plays"""
    
    # Define paths relative to project root
    cities_json_path = os.path.join(PROJECT_ROOT, "data", "static", "modern_mappings", "locations", "cities.json")
    plays_directory = os.path.join(PROJECT_ROOT, "data", "static", "plays")

    print(f"Looking for cities.json at: {cities_json_path}")
    print(f"Looking for plays at: {plays_directory}")

    try:
        with open(cities_json_path, 'r') as f:
            city_data_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: cities.json not found at {cities_json_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in cities.json")
        return

    if not os.path.exists(plays_directory):
        print(f"Error: Plays directory not found at {plays_directory}")
        return

    for play_name in os.listdir(plays_directory):
        play_path = os.path.join(plays_directory, play_name)
        
        if os.path.isdir(play_path):
            full_html_path = os.path.join(play_path, "full.html")
            if not os.path.exists(full_html_path):
                print(f"Skipping {play_name}: No full.html found")
                continue
                
            print(f"Processing play: {play_name}")
            output_directory = os.path.join(play_path, "data")
            characters = scrape_character_names(play_name, full_html_path)

            if characters:
                print(f"Successfully loaded {len(characters)} characters from {play_name}")

                modernized_characters = {}
                for character in characters:
                    city_data = random.choice(city_data_list)
                    modernized_characters[character] = modernize_character(character, city_data)

                call_data = generate_call_data(characters)
                city_data = random.choice(city_data_list)
                contact_data = generate_contact_data(characters, city_data)

                play_data = {
                    "characters": modernized_characters,
                    "call_data": call_data,
                    "contact_data": contact_data
                }

                os.makedirs(output_directory, exist_ok=True)
                output_file = os.path.join(output_directory, "data.json")
                
                with open(output_file, "w", encoding='utf-8') as f:
                    json.dump(play_data, f, indent=4, ensure_ascii=False)

            print(f"Successfully generated data for {play_name} and saved to {output_file}")
            print(f"Generated data for {len(characters)} characters")
            print(f"Generated {len(call_data)} call records")
            print("----------------------------------------")

    else:
                print(f"Could not extract characters from {play_name}")
                print("----------------------------------------")

    if __name__ == "__main__":
            main()
    else:
                print(f"Could not extract characters from {play_name}")
                print("----------------------------------------")

    if __name__ == "__main__":
            main()
            print(f"Could not extract characters from {play_name}")
            print("----------------------------------------")
            print(f"Could not extract characters from {play_name}")
            print("----------------------------------------")

if __name__ == "__main__":
    main()
