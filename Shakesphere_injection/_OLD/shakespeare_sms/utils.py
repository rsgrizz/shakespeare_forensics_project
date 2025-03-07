import os
import json
import random
import time
from datetime import datetime, timedelta
import logging
import re
import hashlib
import base64
from typing import Dict, List, Union, Optional, Tuple
import subprocess
from pathlib import Path

class MessageUtils:
    """Utility functions for message handling and processing"""
    
    @staticmethod
    def generate_message_id() -> str:
        """Generate a unique message ID"""
        timestamp = int(time.time() * 1000)
        random_bits = random.getrandbits(32)
        return f"{timestamp}_{random_bits}"

    @staticmethod
    def format_phone_number(number: str) -> str:
        """Format phone number to standard format"""
        # Remove any non-digit characters
        cleaned = re.sub(r'\D', '', number)
        if len(cleaned) == 10:
            return cleaned
        elif len(cleaned) == 11 and cleaned.startswith('1'):
            return cleaned[1:]
        return cleaned

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        """Convert millisecond timestamp to datetime"""
        return datetime.fromtimestamp(timestamp / 1000)

    @staticmethod
    def datetime_to_timestamp(dt: datetime) -> int:
        """Convert datetime to millisecond timestamp"""
        return int(dt.timestamp() * 1000)

class FileUtils:
    """File handling utilities"""
    
    @staticmethod
    def ensure_directory(directory: str) -> None:
        """Ensure directory exists, create if it doesn't"""
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def safe_file_name(filename: str) -> str:
        """Convert string to safe filename"""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

    @staticmethod
    def get_file_hash(filepath: str) -> str:
        """Generate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

class DatabaseUtils:
    """Database utility functions"""
    
    @staticmethod
    def backup_database(db_path: str, backup_dir: str) -> Optional[str]:
        """Backup database file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
            
            # Create backup command
            cmd = f'adb pull {db_path} {backup_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return backup_path
            return None
        except Exception as e:
            logging.error(f"Database backup failed: {e}")
            return None

    @staticmethod
    def restore_database(backup_path: str, db_path: str) -> bool:
        """Restore database from backup"""
        try:
            cmd = f'adb push {backup_path} {db_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logging.error(f"Database restore failed: {e}")
            return False

class TextUtils:
    """Text processing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove unsafe characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text

    @staticmethod
    def truncate_text(text: str, max_length: int = 160) -> str:
        """Truncate text to SMS length limit"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    @staticmethod
    def split_long_message(text: str, max_length: int = 160) -> List[str]:
        """Split long message into SMS-sized chunks"""
        if len(text) <= max_length:
            return [text]
        
        parts = []
        words = text.split()
        current_part = ""
        
        for word in words:
            if len(current_part) + len(word) + 1 <= max_length:
                current_part += " " + word if current_part else word
            else:
                parts.append(current_part)
                current_part = word
        
        if current_part:
            parts.append(current_part)
        
        return parts

class ValidationUtils:
    """Validation utilities"""
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = re.compile(r'^\d{10}$')
        return bool(pattern.match(MessageUtils.format_phone_number(phone)))

    @staticmethod
    def is_valid_timestamp(timestamp: int) -> bool:
        """Validate timestamp"""
        try:
            # Check if timestamp is within reasonable range
            dt = MessageUtils.timestamp_to_datetime(timestamp)
            return datetime(2000, 1, 1) <= dt <= datetime.now() + timedelta(days=1)
        except:
            return False

class ConfigUtils:
    """Configuration utilities"""
    
    @staticmethod
    def load_config(config_path: str) -> Dict:
        """Load configuration file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return {}

    @staticmethod
    def save_config(config: Dict, config_path: str) -> bool:
        """Save configuration file"""
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
            return False

class LogUtils:
    """Logging utilities"""
    
    @staticmethod
    def setup_logging(log_dir: str, name: str) -> logging.Logger:
        """Setup logging configuration"""
        FileUtils.ensure_directory(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(name)

class ADBUtils:
    """ADB command utilities"""
    
    @staticmethod
    def check_device_connected() -> bool:
        """Check if device is connected via ADB"""
        try:
            result = subprocess.run(
                'adb devices', 
                shell=True, 
                capture_output=True, 
                text=True
            )
            return 'device' in result.stdout
        except:
            return False

    @staticmethod
    def execute_adb_command(command: str) -> Tuple[bool, str]:
        """Execute ADB command and return result"""
        try:
            result = subprocess.run(
                f'adb {command}',
                shell=True,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)

class ProgressTracker:
    """Track and display progress"""
    
    def __init__(self, total: int, description: str = "Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()

    def update(self, amount: int = 1) -> None:
        """Update progress"""
        self.current += amount
        self._display_progress()

    def _display_progress(self) -> None:
        """Display progress bar"""
        percentage = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        
        print(f"\r{self.description}: [{'=' * int(percentage/2)}{' ' * (50-int(percentage/2))}] "
              f"{percentage:.1f}% ({self.current}/{self.total}) "
              f"Rate: {rate:.1f}/s", end='')

# Example usage
if __name__ == "__main__":
    # Setup logging
    logger = LogUtils.setup_logging("logs", "utils_test")
    
    # Test phone number formatting
    phone = "1-703-555-4259"
    formatted = MessageUtils.format_phone_number(phone)
    logger.info(f"Formatted phone: {formatted}")
    
    # Test text processing
    text = "This is a very long message that needs to be split into multiple parts because it exceeds the SMS length limit of 160 characters. Let's see how it handles this situation."
    parts = TextUtils.split_long_message(text)
    logger.info(f"Split into {len(parts)} parts")
    
    # Test progress tracker
    progress = ProgressTracker(100, "Processing messages")
    for i in range(100):
        progress.update()
        time.sleep(0.1)
