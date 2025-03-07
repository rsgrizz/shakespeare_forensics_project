"""
Shakespeare Forensics Training Data Generator
Created by RSGrizz

WARNING: Use at your own risk for forensic training only.
This is FOSS software - see LICENSE.md for details.
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    # Create base directories
    directories = [
        "desktop_creator/src/core",
        "desktop_creator/src/generators",
        "desktop_creator/src/utils",
        "desktop_creator/data/plays",
        "desktop_creator/data/templates",
        "desktop_creator/output",
        "android_injector/src/main",
        "android_injector/src/test",
        "android_injector/assets",
        "android_injector/docs",
        "docs/setup",
        "docs/usage",
        "docs/warnings"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")

def create_initial_files():
    # Create necessary files
    files = {
        "README.md": "# Shakespeare Forensics Training Data Generator\n\nCreated by RSGrizz",
        "LICENSE.md": "# FOSS License\n\n[License details]",
        "CHANGELOG.md": "# Changelog\n\n## [0.1.0] - Initial Release",
        "CREDITS.md": "# Credits\n\nCreated by RSGrizz"
    }
    
    for filename, content in files.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created: {filename}")

def main():
    print("Initializing Shakespeare Forensics Project...")
    create_directory_structure()
    create_initial_files()
    print("\nInitialization complete!")

if __name__ == "__main__":
    main()
