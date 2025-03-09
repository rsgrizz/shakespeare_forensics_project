# In main.py
from call_log_generator import CallLogGenerator
from message_generator import MessageGenerator
from database import SMSDatabase
from verification import MessageVerification
from group_chat import GroupChat
from utils import LogUtils, FileUtils
import config

class ShakespeareDataInjector:
    def __init__(self):
        self.sms_db = SMSDatabase()
        self.message_generator = MessageGenerator()
        self.call_generator = CallLogGenerator()
        self.verifier = MessageVerification()
        
        # Setup logging
        self.logger = LogUtils.setup_logging(config.LOG_DIR, "shakespeare_injection")

    def run(self):
        try:
            # First inject SMS messages
            self.logger.info("Starting SMS injection...")
            sms_results = self.inject_sms_messages()

            # Then inject call logs
            self.logger.info("Starting call log injection...")
            call_results = self.inject_call_logs()

            # Verify everything
            self.logger.info("Verifying data injection...")
            self.verify_injection(sms_results, call_results)

        except Exception as e:
            self.logger.error(f"Injection failed: {e}")
            return False

    def inject_sms_messages(self):
        # Your existing SMS injection code
        pass

    def inject_call_logs(self):
        try:
            # Initialize call generator
            if not self.call_generator.db_handler.detect_database():
                raise Exception("Failed to detect call log database")

            # Generate calls
            calls = self.call_generator.generate_calls(self.message_generator.contacts)
            special_calls = self.call_generator.generate_special_events(
                self.message_generator.contacts
            )
            calls.extend(special_calls)

            # Inject calls
            self.logger.info(f"Injecting {len(calls)} calls...")
            results = self.call_generator.inject_calls(calls)

            success_rate = (results['verified'] / len(calls)) * 100 if calls else 0
            self.logger.info(f"Call Log Injection Results:")
            self.logger.info(f"Total Calls: {len(calls)}")
            self.logger.info(f"Successfully Injected: {results['successful']}")
            self.logger.info(f"Verified: {results['verified']} ({success_rate:.1f}%)")
            self.logger.info(f"Failed: {results['failed']}")

            return results

        except Exception as e:
            self.logger.error(f"Call log injection failed: {e}")
            return None

    def verify_injection(self, sms_results, call_results):
        verification_report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sms': sms_results,
            'calls': call_results
        }

        # Save verification report
        report_path = os.path.join(
            config.LOG_DIR,
            f'verification_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        with open(report_path, 'w') as f:
            json.dump(verification_report, f, indent=4)

        self.logger.info(f"Verification report saved to: {report_path}")
        return verification_report

def main():
    injector = ShakespeareDataInjector()
    success = injector.run()
    
    if success:
        print("\n✅ Data injection completed successfully!")
    else:
        print("\n❌ Data injection failed. Check logs for details.")

if __name__ == "__main__":
    main()
