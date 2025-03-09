"""
play_manager.py
Created by RSGrizz

Manages play data, selection, and basic play information
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

class PlayManager:
    def __init__(self):
        """Initialize PlayManager"""
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Set paths
        self.base_path = Path("desktop_creator/data/static/plays")
        
        # Initialize storage
        self.current_play = None
        self.available_plays = []
        self.play_data = {}
        
        # Load available plays on initialization
        self.refresh_available_plays()

    def refresh_available_plays(self) -> List[str]:
        """
        Refresh the list of available plays from the data directory
        
        Returns:
            List[str]: List of available play names
        """
        try:
            # Get all directories in plays folder that contain play_data.json
            self.available_plays = [
                d.name for d in self.base_path.iterdir()
                if d.is_dir() and (d / "play_data.json").exists()
            ]
            self.logger.info(f"Found {len(self.available_plays)} plays")
            return self.available_plays
        except Exception as e:
            self.logger.error(f"Error refreshing plays: {e}")
            return []

    def get_available_plays(self) -> List[str]:
        """
        Get list of available plays
        
        Returns:
            List[str]: List of play names
        """
        return self.available_plays

    def load_play(self, play_name: str) -> bool:
        """
        Load a specific play's data
        
        Args:
            play_name (str): Name of play to load
            
        Returns:
            bool: Success status
        """
        play_dir = self.base_path / play_name
        
        try:
            # Load main play data
            with open(play_dir / "play_data.json") as f:
                self.play_data = json.load(f)
                
            self.current_play = play_name
            self.logger.info(f"Successfully loaded play: {play_name}")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"Play data not found for: {play_name}")
            return False
        except json.JSONDecodeError:
            self.logger.error(f"Invalid play data format for: {play_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error loading play {play_name}: {e}")
            return False

    def get_characters(self) -> List[str]:
        """
        Get list of characters in current play
        
        Returns:
            List[str]: List of character names
        """
        if not self.play_data:
            self.logger.warning("No play currently loaded")
            return []
        
        return list(self.play_data.get("characters", {}).keys())

    def get_character_info(self, character_name: str) -> Dict:
        """
        Get information about a specific character
        
        Args:
            character_name (str): Name of character
            
        Returns:
            Dict: Character information
        """
        if not self.play_data:
            return {}
            
        return self.play_data.get("characters", {}).get(character_name, {})

    def get_play_summary(self) -> Dict:
        """
        Get summary of current play
        
        Returns:
            Dict: Play summary
        """
        if not self.play_data:
            return {"error": "No play loaded"}
            
        return {
            "title": self.play_data.get("title", "Unknown"),
            "character_count": len(self.get_characters()),
            "scenes": len(self.play_data.get("dialogue", [])),
            "loaded": bool(self.current_play)
        }

    def get_character_lines(self, character_name: str) -> List[Dict]:
        """
        Get all lines spoken by a character
        
        Args:
            character_name (str): Name of character
            
        Returns:
            List[Dict]: List of character's lines with scene info
        """
        if not self.play_data:
            return []
            
        lines = []
        for scene in self.play_data.get("dialogue", []):
            scene_lines = [
                {
                    "text": line["text"],
                    "scene": scene["scene_number"]
                }
                for line in scene["lines"]
                if line["speaker"] == character_name
            ]
            lines.extend(scene_lines)
            
        return lines

    def get_character_interactions(self, character_name: str) -> Dict:
        """
        Get characters that interact with specified character
        
        Args:
            character_name (str): Name of character
            
        Returns:
            Dict: Dictionary of interactions
        """
        if not self.play_data:
            return {}
            
        interactions = {}
        
        for scene in self.play_data.get("dialogue", []):
            if character_name in scene["speakers"]:
                for speaker in scene["speakers"]:
                    if speaker != character_name:
                        interactions[speaker] = interactions.get(speaker, 0) + 1
                        
        return interactions

    def search_dialogue(self, keyword: str) -> List[Dict]:
        """
        Search play dialogue for keyword
        
        Args:
            keyword (str): Keyword to search for
            
        Returns:
            List[Dict]: Matching lines with context
        """
        if not self.play_data:
            return []
            
        matches = []
        for scene in self.play_data.get("dialogue", []):
            for line in scene["lines"]:
                if keyword.lower() in line["text"].lower():
                    matches.append({
                        "speaker": line["speaker"],
                        "text": line["text"],
                        "scene": scene["scene_number"]
                    })
                    
        return matches

def main():
    # Example usage
    pm = PlayManager()
    
    # Show available plays
    print("Available plays:", pm.get_available_plays())
    
    # Load a play
    if pm.get_available_plays():
        play_name = pm.get_available_plays()[0]
        pm.load_play(play_name)
        
        # Show play summary
        print("\nPlay Summary:", pm.get_play_summary())
        
        # Show characters
        print("\nCharacters:", pm.get_characters())

if __name__ == "__main__":
    main()

