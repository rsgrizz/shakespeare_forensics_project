"""
sms_generator.py
Created by RSGrizz

Generates realistic SMS messages based on timeline data.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from pathlib import Path
import json

class SMSGenerator:
    """
    Generates realistic SMS messages based on timeline data.
    """

    def __init__(self):
        """Initialize SMSGenerator."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Set logging level

        # Load SMS templates
        self.templates: Dict = self._load_templates()

    def _load_templates(self) -> Dict:
        """
        Load SMS templates from JSON file.

        Returns:
            Dict: SMS templates.
        """
        template_file = Path("desktop_creator/data/static/templates/sms/patterns.json")

        try:
            with open(template_file) as f:
                return json.load(f)
        except FileNotFoundError as e:
            self.logger.error(f"SMS templates file not found: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in SMS templates file: {e}")
            return {}
        except Exception as e:
            self.logger.exception(f"Error loading SMS templates: {e}")
            return {}

    def generate_sms_messages(self,
                             timeline: List[Dict],
                             characters: Dict) -> List[Dict]:
        """
        Generate SMS messages based on timeline events.

        Args:
            timeline (List[Dict]): List of timeline events.
            characters (Dict): Character information.

        Returns:
            List[Dict]: List of SMS messages.
        """
        sms_messages: List[Dict] = []

        for event in timeline:
            if event['type'] == 'sms':
                sms = self._create_sms_message(event, characters)
                sms_messages.append(sms)

        return sms_messages

    def _create_sms_message(self,
                           event: Dict,
                           characters: Dict) -> Dict:
        """
        Create a single SMS message.

        Args:
            event (Dict): Timeline event.
            characters (Dict): Character information.

        Returns:
            Dict: SMS message.
        """
        # Extract data from event
        from_number = self._get_character_phone(event['from'], characters)
        to_number = self._get_character_phone(event['to'], characters)

        # Generate SMS details
        text = self._generate_sms_text(event['context'])

        sms: Dict = {
            'from_number': from_number,
            'to_number': to_number,
            'timestamp': event['timestamp'].isoformat(),
            'text': text,
            'context': event.get('context', 'normal')
        }

        return sms

    def _get_character_phone(self,
                            character_name: str,
                            characters: Dict) -> str:
        """
        Get phone number for a character.

        Args:
            character_name (str): Name of character.
            characters (Dict): Character information.

        Returns:
            str: Phone number.
        """
        # Check for modernized character data
        if character_name in characters:
            character_data = characters[character_name]
            # Get phone from modern details if available
            if 'modern_details' in character_data and 'phone' in character_data['modern_details']:
                return character_data['modern_details']['phone']
            # Fallback to direct phone number
            elif 'phone' in character_:
                return character_data['phone']
        return '555-1234'  # Default number

    def _generate_sms_text(self, context: str) -> str:
        """
        Generate SMS text based on context.

        Args:
            context (str): Context of the SMS.

        Returns:
            str: SMS text.
        """
        # Select a template based on context
        if context in self.templates:
            template = random.choice(self.templates[context])
            return template
        return "Default message."  # Default message

    def export_sms_messages(self, sms_messages: List[Dict], output_file: str) -> None:
        """
        Export SMS messages to JSON file.

        Args:
            sms_messages (List[Dict]): List of SMS messages.
            output_file (str): Output file path.
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(sms_messages, f, indent=4)
            self.logger.info(f"SMS messages exported to {output_file}")
        except Exception as e:
            self.logger.exception(f"Error exporting SMS messages: {e}")

def main():
    """Example usage of SMSGenerator."""
    # Create an instance of SMSGenerator
    sms_gen = SMSGenerator()

    # Example timeline and character data
    timeline = [{
        'type': 'sms',
        'from': 'BRUTUS',
        'to': 'CASSIUS',
        'timestamp': datetime.now() - timedelta(hours=1),
        'context': 'conspiracy'
    }]

    characters = {
        'BRUTUS': {
            'modern_details': {'phone': '202-555-1111'},
            'phone': '555-1111'
        },
        'CASSIUS': {
            'modern_details': {'phone': '202-555-2222'},
            'phone': '555-2222'
        }
    }

    # Set example SMS templates
    sms_gen.templates = {
        'conspiracy': [
            "Meet me tonight.",
            "The plan is set.",
            "Be ready."
        ]
    }

    # Generate SMS messages
    sms_messages = sms_gen.generate_sms_messages(timeline, characters)

    # Export to JSON
    sms_gen.export_sms_messages(sms_messages, "example_sms_messages.json")

if __name__ == "__main__":
    main()
