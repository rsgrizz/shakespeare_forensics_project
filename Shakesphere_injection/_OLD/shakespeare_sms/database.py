import subprocess
import time
from datetime import datetime
import logging
from typing import Dict, Optional, Union, List
import os
import base64
import json

class MMSPart:
    """Handles MMS message parts (text, images, etc.)"""
    def __init__(self, content_type: str, data: Union[str, bytes], filename: Optional[str] = None):
        self.content_type = content_type
        self.data = data
        self.filename = filename

    def to_base64(self) -> str:
        """Convert data to base64 for storage"""
        if isinstance(self.data, str):
            return base64.b64encode(self.data.encode()).decode()
        return base64.b64encode(self.data).decode()

class SMSDatabase:
    """Enhanced SMS/MMS database handler with verification"""
    
    def __init__(self):
        self.db_path: Optional[str] = None
        self.db_type: Optional[str] = None
        self.table_name: Optional[str] = None
        self.provider_uri: Optional[str] = None
        self.last_error: Optional[str] = None
        self.verification_results: Dict = {}
        
        # Configure logging
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f'sms_database_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    # ... (previous methods remain the same) ...

    def inject_mms(self, 
                  phone_number: str,
                  parts: List[MMSPart],
                  timestamp: int,
                  subject: Optional[str] = None,
                  thread_id: Optional[int] = None) -> bool:
        """
        Injects an MMS message with multiple parts (text, images, etc.).
        
        Args:
            phone_number: Recipient phone number
            parts: List of MMSPart objects
            timestamp: Message timestamp
            subject: Optional MMS subject
            thread_id: Optional thread ID
        """
        try:
            # Create MMS parts
            for i, part in enumerate(parts):
                # Store part data in temporary file
                temp_path = f"/sdcard/temp_mms_part_{i}"
                if isinstance(part.data, str):
                    cmd = f'adb shell "echo -n \'{part.data}\' > {temp_path}"'
                else:
                    # For binary data (images, etc.)
                    with open(f"temp_part_{i}", "wb") as f:
                        f.write(part.data)
                    cmd = f'adb push temp_part_{i} {temp_path}'
                
                subprocess.run(cmd, shell=True, check=True)

                # Insert MMS part
                cmd_parts = [
                    'adb shell content insert',
                    '--uri content://mms/part',
                    f'--bind seq:i:{i}',
                    f'--bind content_type:s:{part.content_type}',
                    f'--bind _data:s:{temp_path}'
                ]
                if part.filename:
                    cmd_parts.append(f'--bind name:s:{part.filename}')
                
                subprocess.run(' '.join(cmd_parts), shell=True, check=True)

            # Create MMS message
            cmd_parts = [
                'adb shell content insert',
                '--uri content://mms',
                f'--bind address:s:{phone_number}',
                f'--bind date:l:{timestamp}',
                '--bind read:i:1',
                '--bind msg_box:i:1',  # 1 for inbox
                '--bind seen:i:1'
            ]
            
            if subject:
                cmd_parts.append(f'--bind subject:s:{subject}')
            if thread_id:
                cmd_parts.append(f'--bind thread_id:i:{thread_id}')

            result = subprocess.run(' '.join(cmd_parts), shell=True, capture_output=True, text=True)
            
            # Cleanup temporary files
            subprocess.run('adb shell rm /sdcard/temp_mms_part_*', shell=True)
            for i in range(len(parts)):
                if os.path.exists(f"temp_part_{i}"):
                    os.remove(f"temp_part_{i}")

            return result.returncode == 0

        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"MMS injection error: {e}")
            return False

    def verify_database_integrity(self) -> Dict:
        """
        Comprehensive database integrity verification.
        """
        results = {
            'structure': self._verify_structure(),
            'permissions': self._verify_permissions(),
            'content': self._verify_content(),
            'threading': self._verify_threading(),
            'mms_capability': self._verify_mms_capability()
        }
        self.verification_results = results
        return results

    def _verify_structure(self) -> Dict:
        """Verifies database structure"""
        structure = {
            'sms_table': False,
            'mms_table': False,
            'threads_table': False,
            'parts_table': False
        }
        
        try:
            # Check each table
            for table in structure.keys():
                cmd = f'adb shell "sqlite3 {self.db_path} \".tables {table}\""'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                structure[table] = table in result.stdout
        except Exception as e:
            self.logger.error(f"Structure verification error: {e}")
        
        return structure

    def _verify_permissions(self) -> Dict:
        """Verifies database permissions"""
        permissions = {
            'read': False,
            'write': False,
            'execute': False
        }
        
        try:
            cmd = f'adb shell ls -l {self.db_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                perms = result.stdout.split()[0]
                permissions['read'] = 'r' in perms
                permissions['write'] = 'w' in perms
                permissions['execute'] = 'x' in perms
        except Exception as e:
            self.logger.error(f"Permissions verification error: {e}")
        
        return permissions

    def _verify_content(self) -> Dict:
        """Verifies message content integrity"""
        content = {
            'total_messages': 0,
            'valid_messages': 0,
            'corrupted_messages': 0,
            'sample_checked': 100  # Number of messages to check
        }
        
        try:
            cmd = f'''
            adb shell "sqlite3 {self.db_path} 
            'SELECT body, date FROM sms ORDER BY date DESC LIMIT {content['sample_checked']}'"
            '''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                messages = result.stdout.split('\n')
                content['total_messages'] = len(messages)
                
                for msg in messages:
                    if msg and not any(c in msg for c in '\x00\xff'):  # Check for corruption
                        content['valid_messages'] += 1
                    else:
                        content['corrupted_messages'] += 1
        except Exception as e:
            self.logger.error(f"Content verification error: {e}")
        
        return content

    def _verify_threading(self) -> Dict:
        """Verifies message threading integrity"""
        threading = {
            'total_threads': 0,
            'valid_threads': 0,
            'orphaned_messages': 0
        }
        
        try:
            # Count threads
            cmd = 'adb shell content query --uri content://mms-sms/conversations --projection thread_id'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            threading['total_threads'] = len([l for l in result.stdout.split('\n') if 'thread_id=' in l])
            
            # Check for orphaned messages
            cmd = 'adb shell content query --uri content://sms --projection thread_id --where "thread_id NOT IN (SELECT thread_id FROM threads)"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            threading['orphaned_messages'] = len([l for l in result.stdout.split('\n') if 'thread_id=' in l])
            
            threading['valid_threads'] = threading['total_threads'] - (threading['orphaned_messages'] > 0)
        except Exception as e:
            self.logger.error(f"Threading verification error: {e}")
        
        return threading

    def _verify_mms_capability(self) -> Dict:
        """Verifies MMS functionality"""
        mms = {
            'provider_available': False,
            'parts_table_accessible': False,
            'can_write_mms': False
        }
        
        try:
            # Check MMS provider
            cmd = 'adb shell content query --uri content://mms --projection _id limit 1'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            mms['provider_available'] = result.returncode == 0
            
            # Check parts table
            cmd = 'adb shell content query --uri content://mms/part --projection _id limit 1'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            mms['parts_table_accessible'] = result.returncode == 0
            
            # Test MMS write
            test_mms = MMSPart('text/plain', 'Test MMS capability')
            mms['can_write_mms'] = self.inject_mms('1234567890', [test_mms], int(time.time() * 1000))
        except Exception as e:
            self.logger.error(f"MMS capability verification error: {e}")
        
        return mms

    def generate_verification_report(self) -> str:
        """Generates a detailed verification report"""
        if not self.verification_results:
            self.verify_database_integrity()
        
        report = ["SMS/MMS Database Verification Report"]
        report.append("=" * 40 + "\n")
        
        # Database Info
        report.append(f"Database Type: {self.db_type}")
        report.append(f"Database Path: {self.db_path}\n")
        
        # Structure
        report.append("Database Structure:")
        for table, exists in self.verification_results['structure'].items():
            report.append(f"  - {table}: {'✓' if exists else '✗'}")
        
        # Permissions
        report.append("\nPermissions:")
        for perm, granted in self.verification_results['permissions'].items():
            report.append(f"  - {perm}: {'✓' if granted else '✗'}")
        
        # Content
        report.append("\nContent Integrity:")
        content = self.verification_results['content']
        report.append(f"  - Messages checked: {content['sample_checked']}")
        report.append(f"  - Valid messages: {content['valid_messages']}")
        report.append(f"  - Corrupted messages: {content['corrupted_messages']}")
        
        # Threading
        report.append("\nMessage Threading:")
        threading = self.verification_results['threading']
        report.append(f"  - Total threads: {threading['total_threads']}")
        report.append(f"  - Valid threads: {threading['valid_threads']}")
        report.append(f"  - Orphaned messages: {threading['orphaned_messages']}")
        
        # MMS Capability
        report.append("\nMMS Capability:")
        mms = self.verification_results['mms_capability']
        report.append(f"  - Provider available: {'✓' if mms['provider_available'] else '✗'}")
        report.append(f"  - Parts table accessible: {'✓' if mms['parts_table_accessible'] else '✗'}")
        report.append(f"  - Can write MMS: {'✓' if mms['can_write_mms'] else '✗'}")
        
        return "\n".join(report)

