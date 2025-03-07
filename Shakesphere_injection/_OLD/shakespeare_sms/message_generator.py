import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import logging
import os
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Character:
    """Represents a character from the play"""
    name: str
    phone_number: str
    relationships: Dict[str, str]  # Other characters and their relationship types
    personality: str  # Character's personality traits
    common_phrases: List[str]  # Character-specific phrases

class MessageGenerator:
    def __init__(self):
        # Configure logging
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f'message_generator_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Initialize character data
        self.characters: Dict[str, Character] = {}
        self.conversations: Dict[str, List[str]] = {}
        self.contacts: Dict[str, str] = {}
        
        # Load modernization mappings
        self.load_language_mappings()
        
        # Initialize message patterns
        self.init_message_patterns()

    def load_language_mappings(self):
        """Load modernization mappings for language conversion"""
        self.modern_mappings = {
            # Basic replacements
            'thou': 'you', 'thee': 'you', 'thy': 'your', 'thine': 'yours',
            'art': 'are', 'hath': 'has', 'doth': 'does', 'wherefore': 'why',
            'ere': 'before', 'twas': 'it was', 'tis': "it's",
            
            # Extended replacements
            'prithee': 'please', 'forsooth': 'honestly', 'methinks': 'I think',
            'perchance': 'maybe', 'mayhap': 'perhaps', 'verily': 'truly',
            'anon': 'soon', 'hence': 'from here', 'whence': 'from where',
            'whereat': 'at which', 'withal': 'with', 'nay': 'no',
            'ay': 'yes', 'alas': 'oh no', 'alack': 'oh no',
            
            # Phrases
            'how now': "what's up",
            'what say you': 'what do you think',
            'I pray you': 'please',
            'pray tell': 'tell me',
            'make haste': 'hurry',
            'give ear': 'listen',
            'take heed': 'be careful',
            'by my troth': 'honestly',
            'fare thee well': 'goodbye',
            'get thee gone': 'go away',
        }

        # Emoji mappings based on context
        self.emoji_mappings = {
            'love': ['💕', '❤️', '💗'], 'death': ['💀', '⚰️', '😱'],
            'ghost': ['👻', '😨'], 'sword': ['⚔️', '🗡️'],
            'king': ['👑', '🤴'], 'queen': ['👸', '👑'],
            'sad': ['😢', '😭', '💔'], 'mad': ['😡', '🤬', '😤'],
            'think': ['🤔', '💭'], 'fight': ['⚔️', '💢', '👊'],
            'drink': ['🍷', '🍺'], 'secret': ['🤫', '🤐'],
            'crazy': ['🤪', '😵'], 'revenge': ['😈', '🗡️'],
        }

    def init_message_patterns(self):
        """Initialize message patterns for different characters"""
        self.character_patterns = {
            'Hamlet': {
                'greetings': ['Hey', 'Hi', 'Hello'],
                'farewells': ['Bye', 'Later', 'Goodbye'],
                'emotions': ['melancholy', 'thoughtful', 'angry'],
                'topics': ['revenge', 'death', 'philosophy'],
                'emoji_frequency': 0.3
            },
            'Ophelia': {
                'greetings': ['Hello', 'Hi there', 'Hey'],
                'farewells': ['Goodbye', 'Take care', 'Bye'],
                'emotions': ['sad', 'confused', 'loving'],
                'topics': ['love', 'family', 'loyalty'],
                'emoji_frequency': 0.5
            },
            # Add more characters...
        }

    def scrape_hamlet(self) -> Dict[str, List[str]]:
        """Scrape Hamlet from MIT Shakespeare website"""
        try:
            url = "http://shakespeare.mit.edu/hamlet/full.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            conversations = {}
            current_speaker = None
            current_act = "Act I"
            
            for element in soup.find_all(['h3', 'a', 'blockquote']):
                if element.name == 'h3':
                    current_act = element.text.strip()
                elif element.name == 'a' and element.get('name'):
                    current_speaker = element.text.strip().title()
                    if current_speaker not in conversations:
                        conversations[current_speaker] = []
                elif element.name == 'blockquote' and current_speaker:
                    text = element.text.strip()
                    sentences = [s.strip() for s in re.split(r'([.!?]+)', text) if s.strip()]
                    
                    for sentence in sentences:
                        if len(sentence) > 10:
                            conversations[current_speaker].append(
                                f"[{current_act}] {sentence}"
                            )
            
            self.conversations = conversations
            self.logger.info(f"Scraped {len(conversations)} characters' dialogues")
            return conversations
            
        except Exception as e:
            self.logger.error(f"Error scraping Hamlet: {e}")
            return {}

    def read_contacts_from_vcf(self, vcf_path: str) -> Dict[str, str]:
        """Read contacts from VCF file"""
        try:
            with open(vcf_path, 'r') as file:
                content = file.read()
                vcards = content.split('BEGIN:VCARD')
                
                for vcard in vcards:
                    if vcard.strip():
                        name_match = re.search(r'FN:(.*?)\n', vcard)
                        phone_match = re.search(r'TEL;TYPE=CELL:([\d-]+)', vcard)
                        
                        if name_match and phone_match:
                            name = name_match.group(1).strip()
                            phone = phone_match.group(1).replace('-', '')
                            self.contacts[name] = phone
                
                self.logger.info(f"Read {len(self.contacts)} contacts from VCF")
                return self.contacts
                
        except Exception as e:
            self.logger.error(f"Error reading contacts: {e}")
            return {}

    def modernize_text(self, text: str, character: str = None) -> str:
        """Convert Shakespeare text to modern format with emojis"""
        # Convert to modern English
        modern_text = text.lower()
        
        # Apply word replacements
        for old, new in self.modern_mappings.items():
            modern_text = re.sub(r'\b' + old + r'\b', new, modern_text, flags=re.IGNORECASE)
        
        # Add character-specific patterns
        if character and character in self.character_patterns:
            pattern = self.character_patterns[character]
            if random.random() < pattern['emoji_frequency']:
                # Add relevant emojis based on content and character
                for keyword, emojis in self.emoji_mappings.items():
                    if keyword in modern_text.lower():
                        modern_text += f" {random.choice(emojis)}"
        
        # Capitalize sentences
        modern_text = '. '.join(s.capitalize() for s in modern_text.split('. '))
        
        return modern_text

    def generate_messages(self, days_of_history: int = 360) -> List[Dict]:
        """Generate messages for all characters"""
        messages = []
        start_date = datetime.now() - timedelta(days=days_of_history)
        current_date = start_date
        
        try:
            # Ensure we have conversations and contacts
            if not self.conversations:
                self.scrape_hamlet()
            
            for character, speeches in self.conversations.items():
                if character not in self.contacts:
                    continue
                
                phone_number = self.contacts[character]
                
                for speech in speeches:
                    # Add random time progression
                    current_date += timedelta(minutes=random.randint(1, 180))
                    if random.random() < 0.2:  # 20% chance to skip to next day
                        current_date += timedelta(days=random.randint(1, 3))
                    
                    # Ensure messages are during waking hours (7 AM to 11 PM)
                    while current_date.hour < 7 or current_date.hour > 23:
                        current_date += timedelta(hours=1)
                    
                    timestamp = int(current_date.timestamp() * 1000)
                    modern_message = self.modernize_text(speech, character)
                    is_incoming = random.random() > 0.5
                    
                    messages.append({
                        'phone_number': phone_number,
                        'message': modern_message,
                        'timestamp': timestamp,
                        'is_incoming': is_incoming,
                        'character': character
                    })
            
            # Sort messages by timestamp
            messages.sort(key=lambda x: x['timestamp'])
            self.logger.info(f"Generated {len(messages)} messages")
            return messages
            
        except Exception as e:
            self.logger.error(f"Error generating messages: {e}")
            return []

    def generate_group_messages(self, group_chat) -> Dict[str, List[str]]:
        """Generate messages for a group chat"""
        messages_dict = {}
        
        try:
            for member in group_chat.members.values():
                if member.name in self.conversations:
                    # Select relevant messages for group context
                    messages = []
                    for speech in self.conversations[member.name]:
                        if len(speech) < 100:  # Keep group messages shorter
                            modern_message = self.modernize_text(speech, member.name)
                            messages.append(modern_message)
                    
                    messages_dict[member.phone_number] = messages
            
            return messages_dict
            
        except Exception as e:
            self.logger.error(f"Error generating group messages: {e}")
            return {}

    def generate_conversation_flow(self, char1: str, char2: str, duration_minutes: int = 30) -> List[Dict]:
        """Generate a realistic conversation flow between two characters"""
        messages = []
        current_time = int(time.time() * 1000)
        
        try:
            # Get relevant speeches for both characters
            speeches1 = self.conversations.get(char1, [])
            speeches2 = self.conversations.get(char2, [])
            
            # Create conversation flow
            time_between_messages = duration_minutes * 60 * 1000 / (len(speeches1) + len(speeches2))
            
            for i in range(min(len(speeches1), len(speeches2))):
                # First character's message
                messages.append({
                    'phone_number': self.contacts[char1],
                    'message': self.modernize_text(speeches1[i], char1),
                    'timestamp': current_time,
                    'is_incoming': False,
                    'character': char1
                })
                current_time += int(time_between_messages)
                
                # Add typing delay
                current_time += random.randint(5000, 15000)
                
                # Second character's response
                messages.append({
                    'phone_number': self.contacts[char2],
                    'message': self.modernize_text(speeches2[i], char2),
                    'timestamp': current_time,
                    'is_incoming': True,
                    'character': char2
                })
                current_time += int(time_between_messages)
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error generating conversation flow: {e}")
            return []

# Example usage
if __name__ == "__main__":
    generator = MessageGenerator()
    
    # Read contacts
    generator.read_contacts_from_vcf("shakespeare_contacts.vcf")
    
    # Generate messages
    messages = generator.generate_messages(days_of_history=360)
    
    # Print sample messages
    for msg in messages[:5]:
        print(f"{msg['character']} ({'incoming' if msg['is_incoming'] else 'outgoing'}): {msg['message']}")
    
    # Generate a conversation between Hamlet and Ophelia
    conversation = generator.generate_conversation_flow("Hamlet", "Ophelia", duration_minutes=30)
    
    print("\nSample conversation:")
    for msg in conversation[:6]:
        print(f"{msg['character']}: {msg['message']}")
