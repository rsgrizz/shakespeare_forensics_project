# database_fixer.py
import subprocess
import time
import os
import sys
from datetime import datetime
import logging

class DatabaseAccessFixer:
    def __init__(self, adb_path):
        self.adb_path = adb_path
        self.setup_logging()

    def setup_logging(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_file = f'logs/database_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def verify_database_state(self):
        print("\n=== Verifying Database State ===")
        self.logger.info("Starting database verification")
        
        try:
            # Check call log access
            print("Checking call log access...")
            call_log = self._check_call_log()
            print(f"Call Log Access: {'✓' if call_log else '✗'}")

            # Check SMS access
            print("Checking SMS access...")
            sms = self._check_sms()
            print(f"SMS Access: {'✓' if sms else '✗'}")

            # Check permissions
            print("\nChecking permissions...")
            perms = self._check_permissions()
            for perm, status in perms.items():
                print(f"{perm}: {'✓' if status else '✗'}")

        except Exception as e:
            self.logger.error(f"Verification failed: {e}")
            print(f"Error during verification: {e}")

    def fix_permissions(self):
        print("\n=== Fixing Permissions ===")
        self.logger.info("Starting permission fixes")
        
        permissions = [
            'android.permission.READ_CALL_LOG',
            'android.permission.WRITE_CALL_LOG',
            'android.permission.READ_SMS',
            'android.permission.WRITE_SMS'
        ]

        for permission in permissions:
            try:
                print(f"Fixing {permission}...")
                cmd = [self.adb_path, 'shell', 'pm', 'grant', 'com.android.shell', permission]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✓ Fixed: {permission}")
                    self.logger.info(f"Successfully fixed {permission}")
                else:
                    print(f"✗ Failed: {permission}")
                    self.logger.error(f"Failed to fix {permission}: {result.stderr}")
                
            except Exception as e:
                print(f"✗ Error fixing {permission}: {e}")
                self.logger.error(f"Error fixing {permission}: {e}")

    def _check_call_log(self):
        try:
            cmd = [self.adb_path, 'shell', 'content', 'query', '--uri', 'content://call_log/calls', '--projection', '_id', 'limit', '1']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Call log check failed: {e}")
            return False

    def _check_sms(self):
        try:
            cmd = [self.adb_path, 'shell', 'content', 'query', '--uri', 'content://sms', '--projection', '_id', 'limit', '1']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"SMS check failed: {e}")
            return False

    def _check_permissions(self):
        permissions = {
            'READ_CALL_LOG': False,
            'WRITE_CALL_LOG': False,
            'READ_SMS': False,
            'WRITE_SMS': False
        }
        
        try:
            cmd = [self.adb_path, 'shell', 'pm', 'list', 'permissions', '-g']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            for perm in permissions:
                permissions[perm] = perm.lower() in result.stdout.lower()
            
            return permissions
        except Exception as e:
            self.logger.error(f"Permission check failed: {e}")
            return permissions

    def fix_all(self):
        print("\n=== Running All Fixes ===")
        self.logger.info("Starting full fix")
        
        try:
            # Fix permissions
            self.fix_permissions()
            
            # Verify fixes
            print("\nVerifying fixes...")
            self.verify_database_state()
            
        except Exception as e:
            self.logger.error(f"Full fix failed: {e}")
            print(f"Error during full fix: {e}")

    def test_database_access(self):
        print("\n=== Testing Database Access ===")
        self.logger.info("Starting database access test")
        
        try:
            # Test SMS
            print("Testing SMS access...")
            sms_cmd = [
                self.adb_path, 'shell', 'content', 'insert',
                '--uri', 'content://sms/inbox',
                '--bind', 'address:s:TEST',
                '--bind', 'body:s:TEST'
            ]
            sms_result = subprocess.run(sms_cmd, capture_output=True, text=True)
            print(f"SMS Test: {'✓' if sms_result.returncode == 0 else '✗'}")

            # Test Call Log
            print("Testing Call Log access...")
            call_cmd = [
                self.adb_path, 'shell', 'content', 'insert',
                '--uri', 'content://call_log/calls',
                '--bind', 'number:s:TEST',
                '--bind', 'duration:i:0'
            ]
            call_result = subprocess.run(call_cmd, capture_output=True, text=True)
            print(f"Call Log Test: {'✓' if call_result.returncode == 0 else '✗'}")

        except Exception as e:
            self.logger.error(f"Database access test failed: {e}")
            print(f"Error during database test: {e}")
