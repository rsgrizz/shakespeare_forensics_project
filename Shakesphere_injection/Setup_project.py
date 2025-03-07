import os
import sys
import shutil
import requests
import zipfile
from pathlib import Path

class ProjectSetup:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.platform_tools_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        
        # Define structure to add to existing directories
        self.directories = {
            'tools': {
                'fixer': {},
                'debugger': {}
            },
            'data': {},
            'config': {}
        }

        # Current structure
        self.existing_dirs = [
            'backup',
            'logs',
            'platform-tools',
            'shakespeare_sms'
        ]

    def verify_existing_structure(self):
        """Verify existing directory structure"""
        print("\nVerifying existing structure...")
        missing_dirs = []
        for dir_name in self.existing_dirs:
            if not os.path.exists(os.path.join(self.base_dir, dir_name)):
                missing_dirs.append(dir_name)
                print(f"Missing directory: {dir_name}")
        
        return len(missing_dirs) == 0

    def create_directory_structure(self):
        """Create additional directory structure"""
        print("\nCreating additional directories...")
        try:
            for main_dir, sub_dirs in self.directories.items():
                main_path = os.path.join(self.base_dir, main_dir)
                os.makedirs(main_path, exist_ok=True)
                print(f"Created/Verified: {main_dir}/")
                
                for sub_dir in sub_dirs:
                    sub_path = os.path.join(main_path, sub_dir)
                    os.makedirs(sub_path, exist_ok=True)
                    print(f"Created/Verified: {main_dir}/{sub_dir}/")
            
            return True
        except Exception as e:
            print(f"Error creating directories: {e}")
            return False

    def verify_platform_tools(self):
        """Verify platform-tools installation"""
        print("\nVerifying platform-tools...")
        adb_path = os.path.join(self.base_dir, 'platform-tools', 'adb.exe')
        if not os.path.exists(adb_path):
            print("ADB not found. Downloading platform-tools...")
            return self.download_platform_tools()
        else:
            print("Platform-tools verified.")
            return True

    def download_platform_tools(self):
        """Download Android platform-tools if needed"""
        try:
            temp_zip = "platform-tools.zip"
            
            # Download the file
            response = requests.get(self.platform_tools_url)
            with open(temp_zip, 'wb') as f:
                f.write(response.content)

            # Extract the file
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(self.base_dir)

            # Clean up
            os.remove(temp_zip)
            print("Platform-tools installed successfully.")
            return True
            
        except Exception as e:
            print(f"Error downloading platform-tools: {e}")
            return False

    def create_initial_files(self):
        """Create initial configuration and script files"""
        print("\nCreating initial files...")
        
        files = {
            # Config files
            os.path.join('config', 'config.json'): '''{
    "database": {
        "sms_path": "/data/data/com.android.providers.telephony/databases/mmssms.db",
        "call_log_path": "/data/data/com.android.providers.contacts/databases/calllog.db"
    },
    "backup": {
        "enabled": true,
        "interval": "daily"
    },
    "logging": {
        "level": "INFO",
        "file_enabled": true
    }
}''',

            # Shakespeare SMS files
            os.path.join('shakespeare_sms', '__init__.py'): '',
            os.path.join('shakespeare_sms', 'database.py'): '# Database handling for SMS and call logs\n',
            os.path.join('shakespeare_sms', 'message_generator.py'): '# Message generation logic\n',
            os.path.join('shakespeare_sms', 'group_chat.py'): '# Group chat functionality\n',
            os.path.join('shakespeare_sms', 'verification.py'): '# Verification utilities\n',
            os.path.join('shakespeare_sms', 'utils.py'): '# Utility functions\n',
            os.path.join('shakespeare_sms', 'config.py'): '# Configuration settings\n',
            os.path.join('shakespeare_sms', 'call_log_generator.py'): '# Call log generation logic\n',
            os.path.join('shakespeare_sms', 'main.py'): '# Main execution script\n',

            # Tools - Fixer
            os.path.join('tools', 'fixer', '__init__.py'): '',
            os.path.join('tools', 'fixer', 'database_fixer.py'): '# Database fixer tool\n',
            os.path.join('tools', 'fixer', 'permissions_fixer.py'): '# Permission fixing utilities\n',
            os.path.join('tools', 'fixer', 'run_fix.bat'): '@echo off\necho Running Database Fixer...\npython database_fixer.py\npause\n',

            # Tools - Debugger
            os.path.join('tools', 'debugger', '__init__.py'): '',
            os.path.join('tools', 'debugger', 'log_analyzer.py'): '# Log analysis tools\n',
            os.path.join('tools', 'debugger', 'database_checker.py'): '# Database verification tools\n',
            os.path.join('tools', 'debugger', 'adb_debugger.py'): '# ADB debugging utilities\n',

            # Backup tools
            os.path.join('backup', '__init__.py'): '',
            os.path.join('backup', 'backup_manager.py'): '# Backup management utilities\n',
            os.path.join('backup', 'restore_utils.py'): '# Restore utilities\n',

            # Root level files
            'requirements.txt': '''requests>=2.31.0
beautifulsoup4>=4.12.2
colorama>=0.4.6
''',
            'README.md': '''# Shakespeare Injection Project

Tool for injecting Shakespeare-themed messages and call logs into Android devices.

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Run setup: `python setup_project.py`
3. Configure settings in `config/config.json`

## Usage
- Main application: Run `python shakespeare_sms/main.py`
- Database fixes: Run `tools/fixer/run_fix.bat`
- Debugging: Use tools in `tools/debugger/`
'''
        }

        try:
            for file_path, content in files.items():
                full_path = os.path.join(self.base_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                if not os.path.exists(full_path):
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Created: {file_path}")
                else:
                    print(f"File exists: {file_path}")
            return True
        except Exception as e:
            print(f"Error creating files: {e}")
            return False

    def print_directory_tree(self):
        """Print the current directory structure"""
        print("\nCurrent Project Structure:")
        print("-------------------------")
        for root, dirs, files in os.walk(self.base_dir):
            level = root.replace(self.base_dir, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            print(f'{indent}{os.path.basename(root)}/')
            for f in files:
                indent = '│   ' * level + '├── '
                print(f'{indent}{f}')

    def setup(self):
        """Run the complete setup"""
        print("Starting Project Setup...")
        
        # Verify existing structure
        if not self.verify_existing_structure():
            response = input("Some directories are missing. Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return False

        # Create additional directories
        if not self.create_directory_structure():
            return False

        # Verify platform-tools
        if not self.verify_platform_tools():
            return False

        # Create initial files
        if not self.create_initial_files():
            return False

        # Print final structure
        self.print_directory_tree()
        
        print("\nSetup completed successfully!")
        return True

def main():
    setup = ProjectSetup()
    if setup.setup():
        print("\nYou can now start using the project tools.")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Configure settings in config/config.json")
        print("3. Start with the main application or fixer tools")
    else:
        print("\nSetup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
