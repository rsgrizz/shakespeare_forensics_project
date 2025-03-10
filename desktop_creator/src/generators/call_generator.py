"""
call_generator.py
Created by RSGrizz

Advanced call log generation with detailed CSV, duration patterns, and timeline
"""

import random
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import logging
from pathlib import Path
import json

class CallGenerator:
    """
    Generates realistic call logs for forensic training scenarios.
    """

    def __init__(self):
        """Initialize CallGenerator."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Set logging level

        # Load call duration patterns
        self.duration_patterns: Dict[str, Dict[str, int]] = self._load_duration_patterns()

        # Call types
        self.call_types: List[str] = ["incoming", "outgoing", "missed"]

        # Call results
        self.call_results: List[str] = ["answered", "no_answer", "busy", "rejected"]

    def _load_duration_patterns(self) -> Dict[str, Dict[str, int]]:
        """
        Load call duration patterns from JSON file.

        Returns:
            Dict[str, Dict[str, int]]: Duration patterns.
        """
        pattern_file = Path("desktop_creator/data/static/templates/calls/durations.json")

        try:
            with open(pattern_file) as f:
                return json.load(f)
        except FileNotFoundError as e:
            self.logger.error(f"Duration patterns file not found: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in duration patterns file: {e}")
            return {}
        except Exception as e:
            self.logger.exception(f"Error loading duration patterns: {e}")
            return {}

    def generate_call_logs(self,
                         timeline: List[Dict],
                         characters: Dict) -> List[Dict]:
        """
        Generate call logs based on timeline events.

        Args:
            timeline (List[Dict]): List of timeline events.
            characters (Dict): Character information.

        Returns:
            List[Dict]: List of call log entries.
        """
        call_logs: List[Dict] = []

        for event in timeline:
            if event['type'] == 'call':
                call_log = self._create_call_log(event, characters)
                call_logs.append(call_log)

        return call_logs

    def _create_call_log(self,
                        event: Dict,
                        characters: Dict) -> Dict:
        """
        Create a single call log entry.

        Args:
            event (Dict): Timeline event.
            characters (Dict): Character information.

        Returns:
            Dict: Call log entry.
        """
        # Extract data from event
        from_number = self._get_character_phone(event['from'], characters)
        to_number = self._get_character_phone(event['to'], characters)

        # Generate call details
        call_type = random.choice(self.call_types)
        call_result = random.choice(self.call_results)
        duration = self._generate_call_duration(event['context'])

        call_log: Dict = {
            'from_number': from_number,
            'to_number': to_number,
            'timestamp': event['timestamp'].isoformat(),
            'call_type': call_type,
            'call_result': call_result,
            'duration': duration,
            'event_context': event.get('context', 'normal'),  # Add context
            'location': characters.get(event['from'], {}).get('location', 'Unknown') # Add location
        }

        return call_log

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

    def _generate_call_duration(self, context: str) -> int:
        """
        Generate call duration based on context.

        Args:
            context (str): Context of the call.

        Returns:
            int: Call duration in seconds.
        """
        # Load duration range from configuration or use defaults
        duration_range: Dict[str, int] = self.duration_patterns.get(context, {"min": 30, "max": 180})

        # Adjust duration based on call type (longer for business, shorter for emergency)
        if context == "business":
            duration = random.randint(duration_range['min'], duration_range['max'] * 2)
        elif context == "emergency":
            duration = random.randint(10, duration_range['max'] // 2)
        else:
            duration = random.randint(duration_range['min'], duration_range['max'])

        return duration

    def export_call_logs(self, call_logs: List[Dict], output_file: str, format: str = "json") -> None:
        """
        Export call logs to specified format.

        Args:
            call_logs (List[Dict]): List of call logs.
            output_file (str): Output file path.
            format (str): Export format (json or csv).
        """
        if format == "json":
            self._export_to_json(call_logs, output_file)
        elif format == "csv":
            self._export_to_csv(call_logs, output_file)
        else:
            self.logger.error(f"Unsupported export format: {format}")

    def _export_to_json(self, call_logs: List[Dict], output_file: str) -> None:
        """
        Export call logs to JSON file.

        Args:
            call_logs (List[Dict]): List of call logs.
            output_file (str): Output file path.
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(call_logs, f, indent=4)
            self.logger.info(f"Call logs exported to {output_file}")
        except Exception as e:
            self.logger.exception(f"Error exporting call logs: {e}")

    def _export_to_csv(self, call_logs: List[Dict], output_file: str) -> None:
        """
        Export call logs to CSV file.

        Args:
            call_logs (List[Dict]): List of call logs.
            output_file (str): Output file path.
        """
        try:
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames: List[str] = ['from_number', 'to_number', 'timestamp', 'call_type',
                              'call_result', 'duration', 'event_context', 'location']  # More fields
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for log in call_logs:
                    writer.writerow(log)
            self.logger.info(f"Call logs exported to {output_file}")
        except Exception as e:
            self.logger.exception(f"Error exporting call logs: {e}")

def main():
    """Example usage of CallGenerator."""
    # Create an instance of CallGenerator
    cg = CallGenerator()

    # Load example duration patterns
    cg.duration_patterns = {
        "business": {"min": 60, "max": 300},
        "personal": {"min": 30, "max": 120},
        "emergency": {"min": 5, "max": 30}
    }

    # Example timeline and character data
    timeline = [{
        'type': 'call',
        'from': 'BRUTUS',
        'to': 'CASSIUS',
        'timestamp': datetime.now() - timedelta(hours=2),
        'context': 'conspiracy'
    }]

    characters = {
        'BRUTUS': {
            'phone': '555-1111',
            'modern_details': {'phone': '202-555-1212'},
            'location': 'Washington DC'
        },
        'CASSIUS': {
            'phone': '555-2222',
            'location': 'Washington DC'
        }
    }

    # Generate call logs
    call_logs = cg.generate_call_logs(timeline, characters)

    # Export to CSV
    cg.export_call_logs(call_logs, "example_call_logs.csv", format="csv")

if __name__ == "__main__":
    main()
