"""
character_manager.py
Created by RSGrizz

Enhanced character modernization with comprehensive mapping rules
"""

import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class CharacterManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Load all mapping data
        self.mapping_path = Path("desktop_creator/data/static/modern_mappings")
        self._load_all_mappings()
        
        # Initialize character storage
        self.modern_mappings = {}
        self.relationship_graph = {}
        
        # Modern context settings
        self.current_context = None
        self.current_organization = None

    def _load_all_mappings(self):
        """Load all mapping files"""
        # Play-specific mappings
        self.play_mappings = {
            "julius_caesar": {
                "context": "government",
                "organization": "United States Congress",
                "location": "Washington DC",
                "roles": {
                    "CAESAR": "Speaker of the House",
                    "BRUTUS": "House Majority Leader",
                    "CASSIUS": "House Minority Whip",
                    "ANTONY": "Senior Senator",
                    "CICERO": "Senate Parliamentarian"
                }
            },
            "hamlet": {
                "context": "business",
                "organization": "Denmark Global Enterprises",
                "location": "New York",
                "roles": {
                    "HAMLET": "CEO",
                    "CLAUDIUS": "Chairman of the Board",
                    "POLONIUS": "Chief Legal Officer",
                    "HORATIO": "Chief Operating Officer",
                    "OPHELIA": "Head of Innovation"
                }
            },
            "othello": {
                "context": "military_contractor",
                "organization": "Venice Security Solutions",
                "location": "Chicago",
                "roles": {
                    "OTHELLO": "Chief Executive Officer",
                    "IAGO": "Chief Operations Officer",
                    "CASSIO": "Vice President of Operations",
                    "DESDEMONA": "Chief Innovation Officer",
                    "RODERIGO": "Regional Director"
                }
            },
            "macbeth": {
                "context": "politics",
                "organization": "Scottish National Party",
                "location": "Edinburgh",
                "roles": {
                    "MACBETH": "Party Leader",
                    "LADY MACBETH": "Campaign Manager",
                    "BANQUO": "Deputy Leader",
                    "MACDUFF": "Opposition Leader",
                    "DUNCAN": "Prime Minister"
                }
            },
            "romeo_and_juliet": {
                "context": "business_rivalry",
                "organization": "Tech Industry",
                "location": "San Francisco",
                "roles": {
                    "ROMEO": "CTO, Montague Tech",
                    "JULIET": "CEO, Capulet Innovations",
                    "MERCUTIO": "Venture Capitalist",
                    "TYBALT": "Head of Security",
                    "FRIAR LAURENCE": "Industry Consultant"
                }
            }
        }

        # Generic role mappings by context
        self.generic_roles = {
            "business": {
                "noble": ["Executive", "Director", "Vice President"],
                "advisor": ["Consultant", "Analyst", "Advisor"],
                "servant": ["Assistant", "Coordinator", "Associate"],
                "soldier": ["Security Officer", "Protection Specialist", "Guard"],
                "messenger": ["Communications Manager", "PR Representative", "Spokesperson"]
            },
            "government": {
                "noble": ["Senator", "Representative", "Secretary"],
                "advisor": ["Chief of Staff", "Policy Advisor", "Legislative Director"],
                "servant": ["Staff Assistant", "Administrative Aide", "Coordinator"],
                "soldier": ["Security Detail", "Federal Agent", "Protection Officer"],
                "messenger": ["Press Secretary", "Communications Director", "Media Liaison"]
            }
        }

    def _generate_modern_name(self, original_name: str, context: str) -> Dict:
        """Generate modern name and contact details"""
        # Clean original name
        clean_name = original_name.lower().replace(" ", "")
        
        # Generate email based on context and organization
        org_domain = self.current_organization.lower().replace(" ", "")
        email = f"{clean_name}@{org_domain}.com"
        
        # Generate phone number based on location
        area_codes = {
            "Washington DC": ["202", "703"],
            "New York": ["212", "646"],
            "Chicago": ["312", "773"],
            "San Francisco": ["415", "628"],
            "Los Angeles": ["213", "323"]
        }
        
        area_code = random.choice(area_codes.get(self.current_context["location"], ["555"]))
        phone = f"{area_code}-{random.randint(200,999)}-{random.randint(1000,9999)}"
        
        return {
            "display_name": original_name,
            "email": email,
            "phone": phone,
            "title": self._generate_title(original_name)
        }

    def _generate_title(self, name: str) -> str:
        """Generate professional title"""
        titles = {
            "business": ["MBA", "PhD", "CPA"],
            "government": ["JD", "PhD", "MA"],
            "military_contractor": ["ret.", "MBA", "MS"],
            "politics": ["MP", "PhD", "JD"]
        }
        
        if random.random() < 0.3:  # 30% chance of having a title
            return random.choice(titles.get(self.current_context["context"], []))
        return ""
    def _create_relationship_mapping(self, play_name: str) -> Dict:
        """Create modern relationship mappings"""
        relationships = {
            "julius_caesar": {
                "CAESAR": {
                    "allies": ["ANTONY", "CALPURNIA"],
                    "opponents": ["BRUTUS", "CASSIUS"],
                    "subordinates": ["CINNA", "DECIUS"]
                },
                "BRUTUS": {
                    "allies": ["CASSIUS", "CICERO"],
                    "opponents": ["CAESAR", "ANTONY"],
                    "subordinates": ["LUCIUS"]
                }
            },
            "hamlet": {
                "HAMLET": {
                    "allies": ["HORATIO", "OPHELIA"],
                    "opponents": ["CLAUDIUS", "POLONIUS"],
                    "subordinates": ["ROSENCRANTZ", "GUILDENSTERN"]
                },
                "CLAUDIUS": {
                    "allies": ["POLONIUS", "GERTRUDE"],
                    "opponents": ["HAMLET"],
                    "subordinates": ["OSRIC"]
                }
            }
        }

        return relationships.get(play_name, {})

    def _modernize_relationships(self, character: str, relationships: Dict) -> Dict:
        """Convert relationships to modern context"""
        modern_rels = {
            "reports_to": [],
            "supervises": [],
            "collaborates_with": [],
            "conflicts_with": []
        }

        # Convert traditional relationships to modern organizational relationships
        if "allies" in relationships:
            modern_rels["collaborates_with"] = relationships["allies"]
        if "opponents" in relationships:
            modern_rels["conflicts_with"] = relationships["opponents"]
        if "subordinates" in relationships:
            modern_rels["supervises"] = relationships["subordinates"]

        return modern_rels
    def modernize_play_characters(self, play_name: str) -> Dict:
        """Modernize all characters for a specific play"""
        if play_name not in self.play_mappings:
            self.logger.error(f"No mapping found for play: {play_name}")
            return {}

        # Set current context
        self.current_context = self.play_mappings[play_name]
        self.current_organization = self.current_context["organization"]

        # Get relationship mappings
        relationships = self._create_relationship_mapping(play_name)

        modernized_characters = {}
        
        # Modernize each character
        for char_name, modern_role in self.current_context["roles"].items():
            modern_char = {
                "original_name": char_name,
                "modern_details": self._generate_modern_name(char_name, self.current_context["context"]),
                "role": modern_role,
                "organization": self.current_organization,
                "location": self.current_context["location"],
                "relationships": self._modernize_relationships(char_name, relationships.get(char_name, {})),
                "context": self.current_context["context"],
                "metadata": {
                    "modernized_date": datetime.now().isoformat(),
                    "play": play_name
                }
            }
            
            modernized_characters[char_name] = modern_char

        self.modern_mappings = modernized_characters
        return modernized_characters

def main():
    # Example usage
    cm = CharacterManager()
    
    # Modernize Julius Caesar
    modern_chars = cm.modernize_play_characters("julius_caesar")
    
    # Print example
    for char_name, details in modern_chars.items():
        print(f"\nModern version of {char_name}:")
        print(json.dumps(details, indent=2))

if __name__ == "__main__":
    main()

