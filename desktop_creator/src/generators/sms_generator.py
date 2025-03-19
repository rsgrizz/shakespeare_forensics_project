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

# Set up logging
logging.basicConfig(level=logging.INFO)

def create_template_structure():
    """Create the necessary directory structure and template file if they don't exist."""
    base_path = Path("desktop_creator/data/static/templates/sms")
    base_path.mkdir(parents=True, exist_ok=True)
    
    patterns_file = base_path / "patterns.json"
    if not patterns_file.exists():
        default_templates = {
            "plot": [
                "Hello the day is today🙄",
                "The deed must be done tonight 🗡️",
                "Remember our plan 👑"
            ],
            "general": [
                "Hey, what's up?",
                "Can we talk?",
                "Important message for you"
            ]
        }
        
        with open(patterns_file, 'w') as f:
            json.dump(default_templates, f, indent=4)

class SMSGenerator:
    """
    Generates realistic SMS messages based on timeline data.
    """

    def __init__(self):
        """Initialize SMSGenerator."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.templates: Dict = self._load_templates()
        self.thread_counter = 1

    def _load_templates(self) -> Dict:
        """Load SMS templates from JSON file."""
        # Get the current file's directory
        current_dir = Path(__file__).parent.parent
        template_file = current_dir / "data" / "static" / "templates" / "sms" / "patterns.json"
        
        try:
            if not template_file.exists():
                self.logger.warning(f"Template file not found at {template_file}")
                return {}
                
            with open(template_file) as f:
                return json.load(f)
        except Exception as e:
            self.logger.exception(f"Error loading SMS templates: {e}")
            return {}

    def verify_templates(self) -> bool:
        """Verify that templates are loaded correctly."""
        if not self.templates:
            self.logger.error("No templates loaded")
            return False
        return True

    def _create_sms_message(self, event: Dict, characters: Dict) -> Dict:
        """Create a single SMS message in the required format."""
        # Get character info
        sender_name = event['from']
        sender_data = characters.get(sender_name, {})
        
        # Generate timestamp in milliseconds
        timestamp = int(event['timestamp'].timestamp() * 1000)
        
        # Create message in required format
        sms = {
            "_id": str(self.thread_counter),
            "thread_id": str(self.thread_counter),
            "address": sender_data.get('modern_details', {}).get('phone', '').replace('-', ''),
            "date": str(timestamp),
            "date_sent": "0",
            "read": "1",
            "status": "-1",
            "type": "2",  # 2 for received message
            "body": self._generate_sms_text(event['context']),
            "locked": "0",
            "error_code": "-1",
            "sub_id": "0",
            "creator": "com.samsung.android.messaging",
            "seen": "1",
            "deletable": "0",
            "sim_slot": "0",
            "hidden": "0",
            "app_id": "0",
            "msg_id": "0",
            "reserved": "1",
            "pri": "0",
            "teleservice_id": "0",
            "svc_cmd": "0",
            "roam_pending": "0",
            "spam_report": "0",
            "secret_mode": "0",
            "safe_message": "0",
            "favorite": "0",
            "d_rpt_cnt": "0",
            "using_mode": "0",
            "announcements_subtype": "0",
            "__display_name": sender_name
        }
        
        self.thread_counter += 1
        return sms

    def generate_sms_messages(self, timeline: List[Dict], characters: Dict) -> List[Dict]:
        """Generate SMS messages based on timeline events."""
        sms_messages = []
        self.thread_counter = 1  # Reset counter
        
        for event in timeline:
            if event['type'] == 'sms':
                sms = self._create_sms_message(event, characters)
                sms_messages.append(sms)
        
        return sms_messages

    def _generate_sms_text(self, context: str) -> str:
        """Generate SMS text based on context."""
        if context in self.templates:
            return random.choice(self.templates[context])
        return "Default message."

    def export_sms_messages(self, sms_messages: List[Dict], output_file: str) -> None:
        """Export SMS messages to JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(sms_messages, f, indent=4)
            self.logger.info(f"SMS messages exported to {output_file}")
        except Exception as e:
            self.logger.exception(f"Error exporting SMS messages: {e}")

def main():
    """Example usage of SMSGenerator."""
    # Create template structure if it doesn't exist
    create_template_structure()
    
    sms_gen = SMSGenerator()
    
    # Verify templates are loaded
    if not sms_gen.verify_templates():
        logging.error("Failed to load templates")
        return

    # Example timeline
    timeline = [{
        'type': 'sms',
        'from': 'Lady Macbeth',
        'to': 'Macbeth',
        'timestamp': datetime(2025, 1, 15, 12, 29),  # specific date/time
        'context': 'plot'
    }]

    # Example characters
    characters = {
        'Lady Macbeth': {
            'modern_details': {'phone': '404-771-2079'},
            'phone': '4047712079'
        }
    }

    # Generate and export
    sms_messages = sms_gen.generate_sms_messages(timeline, characters)
    sms_gen.export_sms_messages(sms_messages, "sms_messages.json")

if __name__ == "__main__":
    main()
