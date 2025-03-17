# Shakespeare Forensics Training Data Generator

Created by RSGrizz

shakespeare_forensics_project/
├── LICENSE.md
├── README.md
├── CHANGELOG.md
├── CREDITS.md
├── DEVELOPMENT_SEQUENCE.txt
├── requirements.txt
│
├── desktop_creator/
│   ├── src/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── play_manager.py
│   │   │   ├── character_manager.py
│   │   │   └── timeline_manager.py
│   │   ├── generators/
│   │   │   ├── __init__.py
│   │   │   ├── contact_generator.py
│   │   │   ├── sms_generator.py
│   │   │   └── call_generator.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── data_validator.py
│   │
│   ├── data/
│   │   ├── static/
│   │   │   ├── plays/
│   │   │   │   ├── julius_caesar/
│   │   │   │   │   ├── script.json
│   │   │   │   │   ├── characters.json
│   │   │   │   │   └── relationships.json
│   │   │   │   ├── hamlet/
│   │   │   │   ├── othello/
│   │   │   │   └── macbeth/
│   │   │   │
│   │   │   ├── modern_mappings/
│   │   │   │   ├── business/
│   │   │   │   │   ├── titles.json
│   │   │   │   │   ├── companies.json
│   │   │   │   │   └── departments.json
│   │   │   │   ├── government/
│   │   │   │   │   ├── positions.json
│   │   │   │   │   └── agencies.json
│   │   │   │   └── locations/
│   │   │   │       ├── cities.json
│   │   │   │       └── area_codes.json
│   │   │   │
│   │   │   ├── templates/
│   │   │   │   ├── sms/
│   │   │   │   │   ├── formal.json
│   │   │   │   │   └── casual.json
│   │   │   │   ├── calls/
│   │   │   │   │   ├── patterns.json
│   │   │   │   │   └── durations.json
│   │   │   │   └── web/
│   │   │   │       ├── sites.json
│   │   │   │       └── searches.json
│   │   │   │
│   │   │   └── assets/
│   │   │       ├── profile_pics/
│   │   │       ├── logos/
│   │   │       └── documents/
│   │   │
│   │   └── output/
│   │       ├── contacts/
│   │       ├── messages/
│   │       ├── calls/
│   │       └── web/
│   │
│   └── tests/
│       ├── unit/
│       └── integration/
│
├── android_injector/
│   ├forked from sms-db. 
