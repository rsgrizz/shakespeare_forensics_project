import subprocess
import logging
import os
from datetime import datetime, timedelta
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
import time

@dataclass
class CallRecord:
    """Represents a phone call record"""
    number: str
    timestamp: int
    duration: int
    call_type: int  # 1=incoming, 2=outgoing, 3=missed
    name: str
    is_video_call: bool = False
    is_conference: bool = False

class CallDatabaseHandler:
    """Handles database operations for call logs"""
    
    def __init__(self):
        self.db_paths = {
            'samsung': '/data/data/com.android.providers.contacts/databases/calllog.db',
            'default': '/data/data/com.android.providers.contacts/databases/contacts2.db',
            'samsung_alt': '/data/data/com.samsung.android.dialer/databases/calllog.db'
        }
        self.current_db = None
        self.provider_uri = None
        self.logger = logging.getLogger(__name__)

    def detect_database(self) -> bool:
        """Detect the correct call log database"""
        try:
            # Check Samsung paths first
            for db_type, path in self.db_paths.items():
                cmd = f'adb shell "if [ -f {path} ]; then echo exists; fi"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if 'exists' in result.stdout:
                    self.current_db = path
                    self.provider_uri = 'content://com.android.contacts/call_log' if 'samsung' in db_type else 'content://call_log/calls'
                    self.logger.info(f"Found call log database: {db_type} at {path}")
                    return True

            # Verify content provider accessibility
            cmd = 'adb shell content query --uri content://call_log/calls --projection _id limit 1'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.provider_uri = 'content://call_log/calls'
                self.logger.info("Using default call log provider")
                return True

            return False

        except Exception as e:
            self.logger.error(f"Database detection error: {e}")
            return False

    def verify_database_access(self) -> bool:
        """Verify database access and permissions"""
        try:
            # Test write permission
            test_cmd = f'''
            adb shell content insert --uri {self.provider_uri} 
            --bind number:s:"1234567890" 
            --bind date:l:{int(time.time() * 1000)} 
            --bind duration:i:0 
            --bind type:i:3 
            --bind new:i:1
            '''
            result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Clean up test entry
                cleanup_cmd = f'adb shell content delete --uri {self.provider_uri} --where "number=\'1234567890\'"'
                subprocess.run(cleanup_cmd, shell=True)
                return True

            return False

        except Exception as e:
            self.logger.error(f"Database access verification failed: {e}")
            return False

    def inject_call(self, call: CallRecord) -> bool:
        """Inject a single call record into the database"""
        try:
            # Base command parts
            cmd_parts = [
                'adb shell content insert',
                f'--uri {self.provider_uri}',
                f'--bind number:s:{call.number}',
                f'--bind date:l:{call.timestamp}',
                f'--bind duration:i:{call.duration}',
                f'--bind type:i:{call.call_type}',
                f'--bind new:i:0',
                f'--bind name:s:{call.name}'
            ]

            # Add Samsung-specific fields if needed
            if 'samsung' in self.current_db:
                cmd_parts.extend([
                    '--bind presentation:i:1',
                    '--bind countryiso:s:US',
                    '--bind geocoded_location:s:United States',
                    f'--bind formatted_number:s:{call.number}'
                ])

            # Add video call flag if applicable
            if call.is_video_call:
                cmd_parts.append('--bind features:i:3')  # 3 = video call feature flag

            # Execute command
            result = subprocess.run(' '.join(cmd_parts), shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"Call injection failed: {result.stderr}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Call injection error: {e}")
            return False

    def verify_call_exists(self, call: CallRecord) -> bool:
        """Verify a call record exists in the database"""
        try:
            cmd = f'''
            adb shell content query --uri {self.provider_uri} 
            --projection _id:number:date:duration:type 
            --where "number='{call.number}' AND date={call.timestamp}"
            '''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return call.number in result.stdout and str(call.timestamp) in result.stdout

        except Exception as e:
            self.logger.error(f"Call verification error: {e}")
            return False

class CallLogGenerator:
    def __init__(self):
        # Setup logging
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f'call_log_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize database handler
        self.db_handler = CallDatabaseHandler()
        if not self.db_handler.detect_database():
            raise Exception("Failed to detect call log database")

        # Initialize other attributes (relationships, patterns, etc.)
        # ... (previous initialization code remains the same)

    def inject_calls(self, calls: List[CallRecord]) -> Dict[str, int]:
        """Inject call records with verification"""
        results = {'successful': 0, 'failed': 0, 'verified': 0}

        try:
            # Verify database access first
            if not self.db_handler.verify_database_access():
                raise Exception("No write access to call log database")

            for call in calls:
                if self.db_handler.inject_call(call):
                    # Verify the call was actually inserted
                    if self.db_handler.verify_call_exists(call):
                        results['verified'] += 1
                    results['successful'] += 1
                    self.logger.info(f"Injected and verified call: {call.name} - {call.duration}s")
                else:
                    results['failed'] += 1
                    self.logger.error(f"Failed to inject call: {call.name}")

                # Add delay between injections
                time.sleep(0.5)

            return results

        except Exception as e:
            self.logger.error(f"Error injecting calls: {e}")
            return results

    # ... (rest of the CallLogGenerator class remains the same)

# Example usage
if __name__ == "__main__":
    try:
        # Sample contacts
        contacts = {
            "Hamlet": "7035554259",
            "Ophelia": "7035558874",
            "Gertrude": "7035551234",
            "Claudius": "7035559876"
        }

        generator = CallLogGenerator()
        
        # Verify database access
        if not generator.db_handler.verify_database_access():
            print("Error: Cannot access call log database")
            exit(1)

        # Generate and inject calls
        print("Generating calls...")
        calls = generator.generate_calls(contacts)
        special_calls = generator.generate_special_events(contacts)
        calls.extend(special_calls)
        
        print(f"Injecting {len(calls)} calls...")
        results = generator.inject_calls(calls)
        
        print("\nCall injection results:")
        print(f"Successful: {results['successful']}")
        print(f"Verified: {results['verified']}")
        print(f"Failed: {results['failed']}")

    except Exception as e:
        print(f"Error: {e}")
