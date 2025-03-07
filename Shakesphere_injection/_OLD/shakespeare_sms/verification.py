import logging
import os
import subprocess
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time
import re

@dataclass
class VerificationResult:
    """Store verification results"""
    success: bool
    details: Dict
    errors: List[str]
    timestamp: int = int(time.time() * 1000)

class MessageVerification:
    """Comprehensive message verification system"""
    
    def __init__(self):
        # Setup logging
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f'verification_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize counters
        self.total_messages = 0
        self.successful = 0
        self.failed = 0
        self.errors = []
        self.verification_results = {}

    def verify_database_structure(self) -> VerificationResult:
        """Verify SMS database structure and tables"""
        try:
            tables_to_check = {
                'sms': False,
                'threads': False,
                'attachments': False,
                'pending_msgs': False,
                'words': False
            }
            
            cmd = 'adb shell "sqlite3 /data/data/com.android.providers.telephony/databases/mmssms.db .tables"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                existing_tables = result.stdout.split()
                for table in tables_to_check:
                    tables_to_check[table] = table in existing_tables
                
                return VerificationResult(
                    success=all(tables_to_check.values()),
                    details={'tables': tables_to_check},
                    errors=[]
                )
            
            return VerificationResult(
                success=False,
                details={},
                errors=['Failed to query database tables']
            )
            
        except Exception as e:
            self.logger.error(f"Database structure verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def verify_message_content(self, message_id: int) -> VerificationResult:
        """Verify content of a specific message"""
        try:
            cmd = f'''
            adb shell content query --uri content://sms/{message_id} 
            --projection _id:address:date:body:type:read
            '''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse message details
                details = {}
                for pair in result.stdout.split(' '):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        details[key] = value
                
                # Verify message integrity
                validations = {
                    'has_body': bool(details.get('body')),
                    'valid_date': self._validate_timestamp(details.get('date')),
                    'valid_type': details.get('type') in ['1', '2'],  # 1=incoming, 2=outgoing
                    'valid_address': self._validate_phone_number(details.get('address'))
                }
                
                return VerificationResult(
                    success=all(validations.values()),
                    details=validations,
                    errors=[]
                )
            
            return VerificationResult(
                success=False,
                details={},
                errors=['Failed to query message content']
            )
            
        except Exception as e:
            self.logger.error(f"Message content verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def verify_message_threading(self) -> VerificationResult:
        """Verify message threading integrity"""
        try:
            cmd = '''
            adb shell content query --uri content://mms-sms/conversations 
            --projection thread_id:message_count:recipient_ids
            '''
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                threads = {}
                orphaned_messages = 0
                
                # Check each thread
                for line in result.stdout.split('\n'):
                    if 'thread_id=' in line:
                        thread_id = re.search(r'thread_id=(\d+)', line)
                        if thread_id:
                            threads[thread_id.group(1)] = {
                                'message_count': self._extract_count(line),
                                'has_recipients': 'recipient_ids' in line
                            }
                
                # Check for orphaned messages
                cmd = 'adb shell content query --uri content://sms --projection thread_id --where "thread_id NOT IN (SELECT _id FROM threads)"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    orphaned_messages = len(result.stdout.split('\n'))
                
                return VerificationResult(
                    success=orphaned_messages == 0,
                    details={
                        'thread_count': len(threads),
                        'threads': threads,
                        'orphaned_messages': orphaned_messages
                    },
                    errors=[]
                )
            
            return VerificationResult(
                success=False,
                details={},
                errors=['Failed to verify message threading']
            )
            
        except Exception as e:
            self.logger.error(f"Threading verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def verify_character_interactions(self, contacts: Dict[str, str]) -> VerificationResult:
        """Verify message interactions between characters"""
        try:
            interactions = {}
            invalid_interactions = []
            
            for name, number in contacts.items():
                # Check outgoing messages
                cmd = f'''
                adb shell content query --uri content://sms 
                --projection count\(*\) as count 
                --where "address='{number}' AND type=2"
                '''
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    outgoing = self._extract_count(result.stdout)
                    
                    # Check incoming messages
                    cmd = cmd.replace('type=2', 'type=1')
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        incoming = self._extract_count(result.stdout)
                        
                        interactions[name] = {
                            'incoming': incoming,
                            'outgoing': outgoing,
                            'total': incoming + outgoing
                        }
                        
                        # Check for suspicious patterns
                        if incoming == 0 or outgoing == 0:
                            invalid_interactions.append(f"No {incoming == 0 and 'incoming' or 'outgoing'} messages for {name}")
                
            return VerificationResult(
                success=len(invalid_interactions) == 0,
                details={'interactions': interactions},
                errors=invalid_interactions
            )
            
        except Exception as e:
            self.logger.error(f"Character interaction verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def verify_timeline_consistency(self) -> VerificationResult:
        """Verify message timeline consistency"""
        try:
            cmd = 'adb shell content query --uri content://sms --projection date --sort date ASC'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                timestamps = []
                for line in result.stdout.split('\n'):
                    if 'date=' in line:
                        timestamp = int(line.split('=')[1])
                        timestamps.append(timestamp)
                
                if timestamps:
                    # Check for chronological order
                    is_ordered = all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1))
                    
                    # Check time gaps
                    gaps = []
                    for i in range(len(timestamps)-1):
                        gap = timestamps[i+1] - timestamps[i]
                        if gap > 86400000:  # More than 24 hours
                            gaps.append({
                                'start': datetime.fromtimestamp(timestamps[i]/1000).strftime('%Y-%m-%d %H:%M:%S'),
                                'end': datetime.fromtimestamp(timestamps[i+1]/1000).strftime('%Y-%m-%d %H:%M:%S'),
                                'gap_hours': gap/3600000
                            })
                    
                    return VerificationResult(
                        success=is_ordered,
                        details={
                            'message_count': len(timestamps),
                            'time_span': {
                                'start': datetime.fromtimestamp(timestamps[0]/1000).strftime('%Y-%m-%d %H:%M:%S'),
                                'end': datetime.fromtimestamp(timestamps[-1]/1000).strftime('%Y-%m-%d %H:%M:%S')
                            },
                            'significant_gaps': gaps
                        },
                        errors=[] if is_ordered else ['Messages not in chronological order']
                    )
            
            return VerificationResult(
                success=False,
                details={},
                errors=['Failed to verify timeline']
            )
            
        except Exception as e:
            self.logger.error(f"Timeline verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def verify_message_distribution(self) -> VerificationResult:
        """Verify message distribution patterns"""
        try:
            # Get message counts by hour
            distribution = {i: 0 for i in range(24)}
            
            cmd = 'adb shell content query --uri content://sms --projection date'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'date=' in line:
                        timestamp = int(line.split('=')[1])
                        hour = datetime.fromtimestamp(timestamp/1000).hour
                        distribution[hour] += 1
                
                # Check for realistic distribution
                night_messages = sum(distribution[h] for h in range(2, 6))  # 2 AM to 6 AM
                total_messages = sum(distribution.values())
                
                is_realistic = (
                    total_messages > 0 and
                    night_messages / total_messages < 0.1  # Less than 10% messages at night
                )
                
                return VerificationResult(
                    success=is_realistic,
                    details={
                        'hourly_distribution': distribution,
                        'total_messages': total_messages,
                        'night_messages': night_messages,
                        'night_percentage': (night_messages / total_messages * 100) if total_messages > 0 else 0
                    },
                    errors=[] if is_realistic else ['Unrealistic message distribution pattern']
                )
            
            return VerificationResult(
                success=False,
                details={},
                errors=['Failed to verify message distribution']
            )
            
        except Exception as e:
            self.logger.error(f"Distribution verification failed: {e}")
            return VerificationResult(
                success=False,
                details={},
                errors=[str(e)]
            )

    def perform_full_verification(self, contacts: Dict[str, str], messages: List[Dict]) -> Dict:
        """Perform all verification checks"""
        self.verification_results = {
            'database_structure': self.verify_database_structure(),
            'message_threading': self.verify_message_threading(),
            'character_interactions': self.verify_character_interactions(contacts),
            'timeline_consistency': self.verify_timeline_consistency(),
            'message_distribution': self.verify_message_distribution()
        }
        
        return self.verification_results

    def generate_verification_report(self) -> str:
        """Generate detailed verification report"""
        if not self.verification_results:
            return "No verification results available"
        
        report = ["Shakespeare Message Injection Verification Report"]
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for check_name, result in self.verification_results.items():
            report.append(f"\n{check_name.replace('_', ' ').title()}")
            report.append("-" * len(check_name))
            report.append(f"Status: {'✓ Pass' if result.success else '✗ Fail'}")
            
            if result.details:
                report.append("\nDetails:")
                for key, value in result.details.items():
                    report.append(f"  {key}: {value}")
            
            if result.errors:
                report.append("\nErrors:")
                for error in result.errors:
                    report.append(f"  • {error}")
        
        return "\n".join(report)

    def _validate_timestamp(self, timestamp_str: str) -> bool:
        """Validate timestamp is within acceptable range"""
        try:
            timestamp = int(timestamp_str)
            dt = datetime.fromtimestamp(timestamp/1000)
            return datetime(2000, 1, 1) <= dt <= datetime.now() + timedelta(days=1)
        except:
            return False

    def _validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        return bool(re.match(r'^\+?\d{10,15}$', phone.replace('-', '')))

    def _extract_count(self, output: str) -> int:
        """Extract count from query output"""
        match = re.search(r'count=(\d+)', output)
        return int(match.group(1)) if match else 0

# Example usage
if __name__ == "__main__":
    verifier = MessageVerification()
    
    # Sample contacts for testing
    contacts = {
        "Hamlet": "7035554259",
        "Ophelia": "7035558874",
        "Gertrude": "7035551234"
    }
    
    # Perform verification
    results = verifier.perform_full_verification(contacts, [])
    
    # Generate and print report
    report = verifier.generate_verification_report()
    print(report)
    
    # Save report to file
    with open(f'verification_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
        f.write(report)
