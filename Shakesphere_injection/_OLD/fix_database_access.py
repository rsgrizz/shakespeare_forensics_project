# fix_database_access.py
import subprocess
import time
import os
import sys
from datetime import datetime
import locale
import json
import re
from typing import Dict, List, Optional, Tuple
import platform
import shutil

class DeviceError(Exception):
    """Custom exception for device-related errors"""
    pass

class DatabaseError(Exception):
    """Custom exception for database-related errors"""
    pass

class PermissionError(Exception):
    """Custom exception for permission-related errors"""
    pass

class DeviceChecker:
    """Handles device checking and diagnostics"""
    
    def __init__(self, adb_path: str):
        self.adb_path = adb_path
        self.device_info = {}
        self.known_issues = self.load_known_issues()

    def load_known_issues(self) -> Dict:
        """Load known device issues and solutions"""
        issues_path = os.path.join(os.path.dirname(__file__), 'device_issues.json')
        try:
            if os.path.exists(issues_path):
                with open(issues_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default known issues
        return {
            "unauthorized": {
                "symptoms": ["unauthorized", "no permissions"],
                "solutions": [
                    "Enable USB debugging",
                    "Revoke USB debugging authorizations and reconnect",
                    "Check USB cable connection"
                ]
            },
            "no_device": {
                "symptoms": ["no device", "device not found"],
                "solutions": [
                    "Check USB connection",
                    "Try different USB port",
                    "Update device drivers"
                ]
            },
            "permission_denied": {
                "symptoms": ["permission denied", "access denied"],
                "solutions": [
                    "Grant necessary permissions",
                    "Check app installation",
                    "Verify SELinux status"
                ]
            }
        }

    async def get_detailed_device_info(self) -> Dict:
        """Get comprehensive device information"""
        try:
            info = {
                'basic_info': await self._get_basic_info(),
                'system_info': await self._get_system_info(),
                'security_info': await self._get_security_info(),
                'storage_info': await self._get_storage_info(),
                'connection_info': await self._get_connection_info()
            }
            
            # Analyze device state
            info['status'] = self._analyze_device_state(info)
            return info
            
        except Exception as e:
            raise DeviceError(f"Failed to get device info: {e}")

    async def _get_basic_info(self) -> Dict:
        """Get basic device information"""
        props = {
            'model': 'ro.product.model',
            'manufacturer': 'ro.product.manufacturer',
            'brand': 'ro.product.brand',
            'device': 'ro.product.device',
            'android_version': 'ro.build.version.release',
            'sdk_version': 'ro.build.version.sdk',
            'serial': 'ro.serialno'
        }
        
        info = {}
        for name, prop in props.items():
            result = await self._run_adb_command(['shell', 'getprop', prop])
            info[name] = result.strip() if result else 'Unknown'
        
        return info

    async def _get_system_info(self) -> Dict:
        """Get system-related information"""
        info = {}
        
        # Check RAM
        mem_info = await self._run_adb_command(['shell', 'cat', '/proc/meminfo'])
        if mem_info:
            mem_total = re.search(r'MemTotal:\s+(\d+)', mem_info)
            if mem_total:
                info['total_ram'] = int(mem_total.group(1)) // 1024  # Convert to MB

        # Check CPU
        cpu_info = await self._run_adb_command(['shell', 'cat', '/proc/cpuinfo'])
        if cpu_info:
            processors = len(re.findall(r'processor\s+:', cpu_info))
            info['cpu_cores'] = processors

        # Check SELinux status
        selinux = await self._run_adb_command(['shell', 'getenforce'])
        info['selinux_status'] = selinux.strip() if selinux else 'Unknown'

        return info

    async def _get_security_info(self) -> Dict:
        """Get security-related information"""
        info = {}
        
        # Check USB debugging status
        adb_status = await self._run_adb_command(['shell', 'settings', 'get', 'global', 'adb_enabled'])
        info['usb_debugging'] = adb_status.strip() == '1'

        # Check device encryption status
        encryption = await self._run_adb_command(['shell', 'getprop', 'ro.crypto.state'])
        info['encrypted'] = encryption.strip() == 'encrypted'

        # Check secure boot status
        secure_boot = await self._run_adb_command(['shell', 'getprop', 'ro.boot.secure_boot'])
        info['secure_boot'] = secure_boot.strip() == '1'

        return info

    async def _get_storage_info(self) -> Dict:
        """Get storage-related information"""
        info = {}
        
        # Check internal storage
        df_output = await self._run_adb_command(['shell', 'df', '/data'])
        if df_output:
            matches = re.search(r'/data\s+(\d+)\s+(\d+)\s+(\d+)', df_output)
            if matches:
                info['internal_storage'] = {
                    'total': int(matches.group(1)) // 1024,  # Convert to MB
                    'used': int(matches.group(2)) // 1024,
                    'free': int(matches.group(3)) // 1024
                }

        # Check SD card
        sd_output = await self._run_adb_command(['shell', 'df', '/storage/sdcard0'])
        info['sd_card_present'] = 'No such file or directory' not in sd_output

        return info

    async def _get_connection_info(self) -> Dict:
        """Get connection-related information"""
        info = {}
        
        # Check USB connection type
        usb_config = await self._run_adb_command(['shell', 'getprop', 'sys.usb.config'])
        info['usb_config'] = usb_config.strip()

        # Check USB state
        usb_state = await self._run_adb_command(['shell', 'getprop', 'sys.usb.state'])
        info['usb_state'] = usb_state.strip()

        # Check ADB connection
        devices = await self._run_adb_command(['devices'])
        info['adb_status'] = 'device' in devices

        return info

    def _analyze_device_state(self, info: Dict) -> Dict:
        """Analyze device state and identify potential issues"""
        issues = []
        warnings = []
        recommendations = []

        # Check Android version compatibility
        if info['basic_info'].get('sdk_version'):
            sdk = int(info['basic_info']['sdk_version'])
            if sdk < 21:  # Android 5.0
                issues.append("Android version too old")
                recommendations.append("Update Android to version 5.0 or higher")

        # Check USB debugging
        if not info['security_info'].get('usb_debugging'):
            issues.append("USB debugging not enabled")
            recommendations.append("Enable USB debugging in Developer Options")

        # Check storage space
        if info['storage_info'].get('internal_storage'):
            free_space = info['storage_info']['internal_storage']['free']
            if free_space < 1000:  # Less than 1GB
                warnings.append("Low storage space")
                recommendations.append("Free up storage space")

        # Check SELinux status
        if info['system_info'].get('selinux_status') == 'Enforcing':
            warnings.append("SELinux is enforcing")
            recommendations.append("Consider setting SELinux to permissive")

        return {
            'issues': issues,
            'warnings': warnings,
            'recommendations': recommendations,
            'is_ready': len(issues) == 0
        }

    async def _run_adb_command(self, args: List[str]) -> str:
        """Run ADB command safely"""
        try:
            cmd = [self.adb_path] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except subprocess.TimeoutExpired:
            raise DeviceError("ADB command timed out")
        except Exception as e:
            raise DeviceError(f"ADB command failed: {e}")

class AutomatedFixer:
    """Handles automated fixes for common issues"""
    
    def __init__(self, adb_path: str, logger):
        self.adb_path = adb_path
        self.logger = logger
        self.fixes_applied = []
        self.backup_created = False

    async def fix_common_issues(self, device_info: Dict) -> Dict:
        """Apply automated fixes based on device diagnostics"""
        results = {
            'fixes_applied': [],
            'failed_fixes': [],
            'warnings': [],
            'needs_restart': False
        }

        try:
            # Create backup if needed
            if not self.backup_created:
                await self._create_backup()
                self.backup_created = True

            # Fix USB debugging issues
            if not device_info['security_info'].get('usb_debugging'):
                if await self._fix_usb_debugging():
                    results['fixes_applied'].append('USB debugging enabled')
                else:
                    results['failed_fixes'].append('USB debugging')

            # Fix SELinux issues
            if device_info['system_info'].get('selinux_status') == 'Enforcing':
                if await self._fix_selinux():
                    results['fixes_applied'].append('SELinux set to permissive')
                    results['needs_restart'] = True
                else:
                    results['failed_fixes'].append('SELinux modification')

            # Fix permissions
            perm_results = await self._fix_permissions()
            results['fixes_applied'].extend(perm_results['fixed'])
            results['failed_fixes'].extend(perm_results['failed'])

            # Fix database access
            db_results = await self._fix_database_access()
            results['fixes_applied'].extend(db_results['fixed'])
            results['failed_fixes'].extend(db_results['failed'])

            return results

        except Exception as e:
            self.logger.error(f"Error during automated fixes: {e}")
            results['failed_fixes'].append(f"General error: {str(e)}")
            return results

    async def _create_backup(self):
        """Create backup of critical data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_{timestamp}"
            
            # Backup call logs
            await self._run_adb_command([
                'shell', 'content', 'query', '--uri', 'content://call_log/calls',
                '>', f'{backup_path}_calls.txt'
            ])
            
            # Backup SMS
            await self._run_adb_command([
                'shell', 'content', 'query', '--uri', 'content://sms',
                '>', f'{backup_path}_sms.txt'
            ])
            
            self.logger.info(f"Backup created at {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return False

    async def _fix_usb_debugging(self) -> bool:
        """Fix USB debugging issues"""
        try:
            # Enable developer options
            await self._run_adb_command([
                'shell', 'settings', 'put', 'global',
                'development_settings_enabled', '1'
            ])
            
            # Enable USB debugging
            await self._run_adb_command([
                'shell', 'settings', 'put', 'global',
                'adb_enabled', '1'
            ])
            
            return True
        except Exception as e:
            self.logger.error(f"USB debugging fix failed: {e}")
            return False

    async def _fix_selinux(self) -> bool:
        """Temporarily set SELinux to permissive"""
        try:
            result = await self._run_adb_command(['shell', 'setenforce', '0'])
            return 'Permission denied' not in result
        except Exception as e:
            self.logger.error(f"SELinux fix failed: {e}")
            return False

    async def _fix_permissions(self) -> Dict[str, List[str]]:
        """Fix permission-related issues"""
        results = {'fixed': [], 'failed': []}
        permissions = [
            'android.permission.READ_CALL_LOG',
            'android.permission.WRITE_CALL_LOG',
            'android.permission.READ_SMS',
            'android.permission.WRITE_SMS',
            'android.permission.READ_CONTACTS',
            'android.permission.WRITE_CONTACTS'
        ]

        for permission in permissions:
            try:
                # Try to grant permission
                result = await self._run_adb_command([
                    'shell', 'pm', 'grant', 'com.android.shell', permission
                ])
                
                # Verify permission was granted
                verify = await self._run_adb_command([
                    'shell', 'pm', 'list', 'permissions', '-g', '|', 'grep', permission
                ])
                
                if 'granted' in verify.lower():
                    results['fixed'].append(f"Permission: {permission}")
                else:
                    results['failed'].append(f"Permission: {permission}")
                    
            except Exception as e:
                self.logger.error(f"Permission fix failed for {permission}: {e}")
                results['failed'].append(f"Permission: {permission}")

        return results

    async def _fix_database_access(self) -> Dict[str, List[str]]:
        """Fix database access issues"""
        results = {'fixed': [], 'failed': []}
        
        try:
            # Check and fix database permissions
            databases = [
                '/data/data/com.android.providers.contacts/databases/calllog.db',
                '/data/data/com.android.providers.telephony/databases/mmssms.db'
            ]
            
            for db_path in databases:
                try:
                    # Try to fix permissions
                    await self._run_adb_command(['shell', 'chmod', '666', db_path])
                    
                    # Verify access
                    test_result = await self._run_adb_command([
                        'shell', 'ls', '-l', db_path
                    ])
                    
                    if 'Permission denied' not in test_result:
                        results['fixed'].append(f"Database access: {db_path}")
                    else:
                        results['failed'].append(f"Database access: {db_path}")
                        
                except Exception as e:
                    self.logger.error(f"Database fix failed for {db_path}: {e}")
                    results['failed'].append(f"Database access: {db_path}")

            return results
            
        except Exception as e:
            self.logger.error(f"Database access fix failed: {e}")
            results['failed'].append("Database access: General error")
            return results

    async def _run_adb_command(self, args: List[str]) -> str:
        """Run ADB command with error handling"""
        try:
            cmd = [self.adb_path] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                raise Exception(f"Command failed: {result.stderr}")
                
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise Exception("Command timed out")
        except Exception as e:
            raise Exception(f"Command failed: {e}")

    async def verify_fixes(self) -> Dict:
        """Verify that fixes were applied successfully"""
        verification = {
            'permissions': await self._verify_permissions(),
            'database_access': await self._verify_database_access(),
            'usb_debugging': await self._verify_usb_debugging(),
            'selinux': await self._verify_selinux()
        }
        
        return {
            'all_passed': all(verification.values()),
            'details': verification
        }

    async def _verify_permissions(self) -> bool:
        """Verify permissions are properly set"""
        try:
            result = await self._run_adb_command([
                'shell', 'pm', 'list', 'permissions', '-g'
            ])
            return all(perm in result for perm in [
                'READ_CALL_LOG', 'WRITE_CALL_LOG', 'READ_SMS', 'WRITE_SMS'
            ])
        except Exception:
            return False

    async def _verify_database_access(self) -> bool:
        """Verify database access"""
        try:
            # Test SMS access
            sms_test = await self._run_adb_command([
                'shell', 'content', 'query', '--uri', 'content://sms', '--projection', '_id', 'limit', '1'
            ])
            
            # Test call log access
            call_test = await self._run_adb_command([
                'shell', 'content', 'query', '--uri', 'content://call_log/calls', '--projection', '_id', 'limit', '1'
            ])
            
            return 'Exception' not in sms_test and 'Exception' not in call_test
            
        except Exception:
            return False

    async def _verify_usb_debugging(self) -> bool:
        """Verify USB debugging is enabled"""
        try:
            result = await self._run_adb_command([
                'shell', 'settings', 'get', 'global', 'adb_enabled'
            ])
            return result.strip() == '1'
        except Exception:
            return False

    async def _verify_selinux(self) -> bool:
        """Verify SELinux status"""
        try:
            result = await self._run_adb_command(['shell', 'getenforce'])
            return result.strip().lower() == 'permissive'
        except Exception:
            return False
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Shakespeare Database Access Fixer')
    parser.add_argument('adb_path', help='Path to ADB executable')
    parser.add_argument('--full-fix', action='store_true', help='Run full fix')
    parser.add_argument('--fix-permissions', action='store_true', help='Fix permissions only')
    parser.add_argument('--verify', action='store_true', help='Verify database access')
    parser.add_argument('--backup', action='store_true', help='Create backup')
    
    args = parser.parse_args()
    
    try:
        fixer = DatabaseAccessFixer(args.adb_path)
        
        if args.full_fix:
            fixer.fix_all()
        elif args.fix_permissions:
            fixer.fix_permissions()
        elif args.verify:
            fixer.verify_database_state()
        elif args.backup:
            fixer._create_backup()
        else:
            # Interactive menu mode
            while True:
                print("\nAvailable options:")
                print("1. Run all fixes and verify")
                print("2. Check device connection and info")
                print("3. Verify database access")
                print("4. Fix permissions")
                print("5. Test database injection")
                print("6. Exit")
                
                choice = input("\nEnter your choice (1-6): ")
                
                if choice == '1':
                    fixer.fix_all()
                elif choice == '2':
                    fixer.check_adb_connection()
                elif choice == '3':
                    fixer.verify_database_state()
                elif choice == '4':
                    fixer.fix_permissions()
                elif choice == '5':
                    fixer.test_database_access()
                elif choice == '6':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")

    except Exception as e:
        print(f"Error: {e}")
        print("Please check the log file for details.")
        sys.exit(1)
