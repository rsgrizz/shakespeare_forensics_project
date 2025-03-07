# In config.py
import os

# Directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VCF_PATH = os.path.join(BASE_DIR, "shakespeare_contacts.vcf")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Database settings
DATABASES = {
    'sms': {
        'samsung': '/data/data/com.samsung.android.messaging/databases/message.db',
        'default': '/data/data/com.android.providers.telephony/databases/mmssms.db'
    },
    'calls': {
        'samsung': '/data/data/com.android.providers.contacts/databases/calllog.db',
        'samsung_alt': '/data/data/com.samsung.android.dialer/databases/calllog.db',
        'default': '/data/data/com.android.providers.contacts/databases/contacts2.db'
    }
}

# Time settings
MESSAGE_DELAY = 1  # seconds between messages
CALL_DELAY = 0.5  # seconds between calls
DAYS_OF_HISTORY = 360

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
