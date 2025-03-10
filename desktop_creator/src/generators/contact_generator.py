"""
contact_generator.py
Created by RSGrizz

Generates realistic contact information and exports VCF files.
"""

import random
from typing import Dict, List
import logging
from pathlib import Path
import json
from datetime import datetime

class ContactGenerator:
    """
    Generates realistic contact information and exports VCF files.
    """

    def __init__(self):
        """Initialize ContactGenerator."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Set logging level

        # Load configuration data
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load configuration data from JSON file.

        Returns:
            Dict: Configuration data.
        """
        config_file = Path("desktop_creator/data/static/templates/contacts/config.json")

        try:
            with open(config_file) as f:
                return json.load(f)
        except FileNotFoundError as e:
            self.logger.error(f"Config file not found: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return {}
        except Exception as e:
            self.logger.exception(f"Error loading config file: {e}")
            return {}

    def generate_contact(self, character: Dict) -> Dict:
        """
        Generate contact information for a character.

        Args:
            character (Dict): Character data.

        Returns:
            Dict: Contact information.
        """
        contact: Dict = {
            'first_name': self._generate_first_name(character),
            'last_name': self._generate_last_name(character),
            'phone_number': self._generate_phone_number(character),
            'email': self._generate_email(character),
            'address': self._generate_address(character),
            'organization': self._generate_organization(character),
            'title': self._generate_title(character),
            'notes': self._generate_notes(character)
        }
        return contact

    def _generate_first_name(self, character: Dict) -> str:
        """Generate first name for a character."""
        # Use modern name if available, otherwise use original name
        if 'modern_details' in character and 'display_name' in character['modern_details']:
            return character['modern_details']['display_name'].split()[0]
        return character['original_name'].split()[0]

    def _generate_last_name(self, character: Dict) -> str:
        """Generate last name for a character."""
        # Use modern name if available, otherwise use original name
        if 'modern_details' in character and 'display_name' in character['modern_details']:
            name_parts = character['modern_details']['display_name'].split()
            if len(name_parts) > 1:
                return name_parts[-1]  # Use the last part as the last name
        return character['original_name'].split()[-1]

    def _generate_phone_number(self, character: Dict) -> str:
        """Generate phone number for a character."""
        if 'modern_details' in character and 'phone' in character['modern_details']:
            return character['modern_details']['phone']
        return "555-123-4567"  # Default phone number

    def _generate_email(self, character: Dict) -> str:
        """Generate email address for a character."""
        if 'modern_details' in character and 'email' in character['modern_details']:
            return character['modern_details']['email']
        return "default@example.com"  # Default email

    def _generate_address(self, character: Dict) -> str:
        """Generate address for a character."""
        if 'location' in character:
            city = character['location']
            street = f"{random.randint(100, 9999)} Main St"
            return f"{street}, {city}, {character['context'].upper()}"
        return "123 Example St, Anytown, USA"  # Default address

    def _generate_organization(self, character: Dict) -> str:
        """Generate organization for a character."""
        if 'organization' in character:
            return character['organization']
        return "Example Corp"  # Default organization

    def _generate_title(self, character: Dict) -> str:
        """Generate title for a character."""
        if 'role' in character:
            return character['role']
        return "Employee"  # Default title

    def _generate_notes(self, character: Dict) -> str:
        """Generate notes for a character."""
        return f"Character from {character.get('metadata', {}).get('play', 'Unknown Play')}"

    def create_vcf_string(self, contact: Dict) -> str:
        """
        Create a VCF string from contact information.

        Args:
            contact (Dict): Contact information.

        Returns:
            str: VCF string.
        """
        vcf_string = f"""BEGIN:VCARD
VERSION:3.0
N:{contact['last_name']};{contact['first_name']};;;
FN:{contact['first_name']} {contact['last_name']}
ORG:{contact['organization']}
TITLE:{contact['title']}
TEL;TYPE=CELL:{contact['phone_number']}
EMAIL:{contact['email']}
ADR;TYPE=WORK:;;{contact['address']}
NOTE:{contact['notes']}
REV:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
END:VCARD
"""
        return vcf_string

    def export_to_vcf(self, contacts: List[Dict], output_file: str) -> None:
        """
        Export contacts to a VCF file.

        Args:
            contacts (List[Dict]): List of contact information.
            output_file (str): Output file path.
        """
        try:
            with open(output_file, 'w') as f:
                for contact in contacts:
                    vcf_string = self.create_vcf_string(contact)
                    f.write(vcf_string)
            self.logger.info(f"Exported contacts to {output_file}")
        except Exception as e:
            self.logger.exception(f"Error exporting contacts: {e}")

def main():
    """Example usage of ContactGenerator."""
    # Create an instance of ContactGenerator
    cg = ContactGenerator()

    # Example character data
    characters = [
        {
            'original_name': 'Julius Caesar',
            'modern_details': {'display_name': 'Julius Caesar', 'phone': '202-555-1000', 'email': 'caesar@example.com'},
            'location': 'Washington D.C.',
            'organization': 'U.S. Senate',
            'role': 'Senator',
            'metadata': {'play': 'Julius Caesar'}
        },
        {
            'original_name': 'Brutus',
            'modern_details': {'display_name': 'Marcus Brutus', 'phone': '202-555-1001', 'email': 'brutus@example.com'},
            'location': 'Washington D.C.',
            'organization': 'U.S. Senate',
            'role': 'Senator',
            'metadata': {'play': 'Julius Caesar'}
        }
    ]

    # Generate contact information for each character
    contacts = [cg.generate_contact(character) for character in characters]

    # Export contacts to VCF file
    cg.export_to_vcf(contacts, "example_contacts.vcf")

if __name__ == "__main__":
    main()

