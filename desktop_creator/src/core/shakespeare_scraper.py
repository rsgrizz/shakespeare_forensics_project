"""
shakespeare_scraper.py
Created by RSGrizz

Scrapes play data from MIT Shakespeare website
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

class ShakespeareScraper:
    def __init__(self):
        self.base_url = "http://shakespeare.mit.edu/"
        self.output_dir = Path("desktop_creator/data/static/plays")

    def scrape_play(self, play_name):
        """
        Scrapes entire play including:
        - Characters
        - Dialogue
        - Scene information
        """
        print(f"Scraping {play_name}...")
        
        # Create URL-friendly name
        play_url = play_name.lower().replace(" ", "")
        url = f"{self.base_url}{play_url}/full.html"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get character list
            characters = self._extract_characters(soup)
            
            # Get dialogue
            dialogue = self._extract_dialogue(soup)

            # Create play data structure
            play_data = {
                "title": play_name,
                "characters": characters,
                "dialogue": dialogue
            }

            # Save to JSON
            self._save_play_data(play_name, play_data)
            
            print(f"Successfully scraped {play_name}")
            return play_data

        except Exception as e:
            print(f"Error scraping {play_name}: {e}")
            return None

    def _extract_characters(self, soup):
        """Extract character list from play"""
        characters = {}
        dramatis_personae = soup.find('blockquote')
        
        if dramatis_personae:
            for line in dramatis_personae.text.split('\n'):
                if line.strip():
                    # Usually characters are in CAPS
                    match = re.match(r'^([A-Z][A-Z\s]+)', line)
                    if match:
                        char_name = match.group(1).strip()
                        characters[char_name] = {
                            "description": line.replace(char_name, '').strip(),
                            "lines": 0,  # Will count later
                            "scenes": []  # Will fill later
                        }
        
        return characters

    def _extract_dialogue(self, soup):
        """Extract all dialogue from play"""
        dialogue = []
        scenes = soup.find_all('scene')
        
        for scene in scenes:
            scene_data = {
                "scene_number": len(dialogue) + 1,
                "speakers": [],
                "lines": []
            }
            
            # Find all dialogue
            speeches = scene.find_all('speech')
            for speech in speeches:
                speaker = speech.find('speaker')
                if speaker:
                    speaker_name = speaker.text.strip()
                    scene_data["speakers"].append(speaker_name)
                    
                    lines = speech.find_all('line')
                    for line in lines:
                        scene_data["lines"].append({
                            "speaker": speaker_name,
                            "text": line.text.strip()
                        })
            
            dialogue.append(scene_data)
        
        return dialogue

    def _save_play_data(self, play_name, data):
        """Save play data to JSON files"""
        play_dir = self.output_dir / play_name.lower().replace(" ", "_")
        play_dir.mkdir(parents=True, exist_ok=True)

        # Save full play data
        with open(play_dir / "play_data.json", 'w') as f:
            json.dump(data, f, indent=4)

        # Save character list separately
        with open(play_dir / "characters.json", 'w') as f:
            json.dump(data["characters"], f, indent=4)

def main():
    scraper = ShakespeareScraper()
    
    # List of plays to scrape
    plays = [
        "Julius Caesar",
        "Hamlet",
        "Othello",
        "Macbeth"
    ]
    
    for play in plays:
        scraper.scrape_play(play)

if __name__ == "__main__":
    main()
