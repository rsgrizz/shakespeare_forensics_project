from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import random
import logging
import os
from dataclasses import dataclass
import json
import time

@dataclass
class GroupMember:
    """Represents a member in a group chat"""
    name: str
    phone_number: str
    join_date: int  # timestamp
    is_admin: bool = False
    last_active: Optional[int] = None

@dataclass
class GroupMessage:
    """Represents a message in a group chat"""
    sender: GroupMember
    content: str
    timestamp: int
    message_type: str = "text"  # text, image, system
    replied_to: Optional[int] = None  # message_id of replied message
    mentions: List[str] = None  # list of mentioned phone numbers

class GroupChat:
    """Handles group chat creation and message management"""
    
    def __init__(self, name: str, creator: GroupMember):
        self.name = name
        self.created_at = int(time.time() * 1000)
        self.thread_id = self._generate_thread_id()
        self.members: Dict[str, GroupMember] = {creator.phone_number: creator}
        self.messages: List[GroupMessage] = []
        self.creator = creator
        self.group_image: Optional[str] = None
        
        # Configure logging
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f'group_chat_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _generate_thread_id(self) -> int:
        """Generates a unique thread ID for the group"""
        return int(time.time() * 1000) + random.randint(1000, 9999)

    def add_member(self, member: GroupMember) -> bool:
        """Adds a new member to the group"""
        try:
            if member.phone_number not in self.members:
                self.members[member.phone_number] = member
                system_message = GroupMessage(
                    sender=self.creator,
                    content=f"{member.name} joined the group",
                    timestamp=int(time.time() * 1000),
                    message_type="system"
                )
                self.messages.append(system_message)
                self.logger.info(f"Added member {member.name} to group {self.name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding member: {e}")
            return False

    def remove_member(self, phone_number: str, removed_by: GroupMember) -> bool:
        """Removes a member from the group"""
        try:
            if phone_number in self.members:
                if not removed_by.is_admin and removed_by.phone_number != self.creator.phone_number:
                    self.logger.warning(f"Unauthorized removal attempt by {removed_by.name}")
                    return False
                
                removed_member = self.members.pop(phone_number)
                system_message = GroupMessage(
                    sender=removed_by,
                    content=f"{removed_member.name} was removed from the group",
                    timestamp=int(time.time() * 1000),
                    message_type="system"
                )
                self.messages.append(system_message)
                self.logger.info(f"Removed member {removed_member.name} from group {self.name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing member: {e}")
            return False

    def add_message(self, message: GroupMessage) -> bool:
        """Adds a message to the group chat"""
        try:
            if message.sender.phone_number in self.members:
                self.messages.append(message)
                self.members[message.sender.phone_number].last_active = message.timestamp
                self.logger.info(f"Added message from {message.sender.name} to group {self.name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding message: {e}")
            return False

    def get_messages_since(self, timestamp: int) -> List[GroupMessage]:
        """Returns all messages since the given timestamp"""
        return [msg for msg in self.messages if msg.timestamp > timestamp]

    def get_active_members(self, hours: int = 24) -> List[GroupMember]:
        """Returns members active within the last specified hours"""
        cutoff_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        return [member for member in self.members.values() if member.last_active and member.last_active > cutoff_time]

    def create_shakespeare_groups(contacts: Dict[str, str]) -> List['GroupChat']:
        """Creates predefined Shakespeare-themed group chats"""
        groups = []
        
        # Define group configurations
        group_configs = [
            {
                "name": "Royal Court of Denmark 👑",
                "members": ["Hamlet", "Claudius", "Gertrude", "Polonius"],
                "admin": "Claudius"
            },
            {
                "name": "Hamlet's Friends 🤝",
                "members": ["Hamlet", "Horatio", "Rosencrantz", "Guildenstern"],
                "admin": "Hamlet"
            },
            {
                "name": "Guard Duty 💂",
                "members": ["Horatio", "Marcellus", "Bernardo", "Francisco"],
                "admin": "Horatio"
            },
            {
                "name": "Family Drama 👪",
                "members": ["Hamlet", "Gertrude", "Ophelia", "Laertes"],
                "admin": "Gertrude"
            },
            {
                "name": "Conspirators 🗡️",
                "members": ["Claudius", "Laertes", "Rosencrantz", "Guildenstern"],
                "admin": "Claudius"
            }
        ]

        # Create groups
        for config in group_configs:
            try:
                # Create admin member
                admin = GroupMember(
                    name=config["admin"],
                    phone_number=contacts[config["admin"]],
                    join_date=int(time.time() * 1000),
                    is_admin=True
                )
                
                # Create group
                group = GroupChat(config["name"], admin)
                
                # Add other members
                for member_name in config["members"]:
                    if member_name != config["admin"] and member_name in contacts:
                        member = GroupMember(
                            name=member_name,
                            phone_number=contacts[member_name],
                            join_date=int(time.time() * 1000)
                        )
                        group.add_member(member)
                
                groups.append(group)
                
            except Exception as e:
                logging.error(f"Error creating group {config['name']}: {e}")
                continue
        
        return groups

    def inject_group_messages(self, db, messages_dict: Dict[str, List[str]]):
        """Injects messages into the group chat"""
        try:
            base_time = int((datetime.now() - timedelta(days=360)).timestamp() * 1000)
            current_time = base_time
            
            for member_phone, messages in messages_dict.items():
                if member_phone not in self.members:
                    continue
                    
                member = self.members[member_phone]
                
                for message_text in messages:
                    # Add some random time progression
                    current_time += random.randint(60000, 3600000)  # 1 minute to 1 hour
                    
                    # Create group message
                    message = GroupMessage(
                        sender=member,
                        content=message_text,
                        timestamp=current_time
                    )
                    
                    # Add to group history
                    self.add_message(message)
                    
                    # Inject into database
                    for recipient in self.members.values():
                        if recipient.phone_number != member_phone:
                            db.inject_message(
                                phone_number=recipient.phone_number,
                                message=f"[{self.name}] {member.name}: {message_text}",
                                timestamp=current_time,
                                is_incoming=True,
                                thread_id=self.thread_id
                            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting group messages: {e}")
            return False

    def export_chat_history(self, filename: str):
        """Exports chat history to a JSON file"""
        try:
            chat_data = {
                "name": self.name,
                "created_at": self.created_at,
                "thread_id": self.thread_id,
                "members": [
                    {
                        "name": member.name,
                        "phone_number": member.phone_number,
                        "join_date": member.join_date,
                        "is_admin": member.is_admin
                    }
                    for member in self.members.values()
                ],
                "messages": [
                    {
                        "sender": msg.sender.name,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                        "type": msg.message_type
                    }
                    for msg in self.messages
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(chat_data, f, indent=4)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting chat history: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Sample contacts
    contacts = {
        "Hamlet": "7035554259",
        "Claudius": "7035551234",
        "Gertrude": "7035555678",
        "Ophelia": "7035559012"
    }
    
    # Create groups
    groups = GroupChat.create_shakespeare_groups(contacts)
    
    # Sample messages for a group
    messages_dict = {
        "7035554259": [  # Hamlet
            "Something is rotten in the state of Denmark 🤔",
            "To be, or not to be, that is the question 💭",
            "Anyone else seen any ghosts lately? 👻"
        ],
        "7035551234": [  # Claudius
            "Everything's fine here 😅",
            "Nothing to worry about 👑",
            "Who's up for a drink? 🍷"
        ]
    }
    
    # Inject messages (requires database instance)
    # for group in groups:
    #     group.inject_group_messages(db, messages_dict)
