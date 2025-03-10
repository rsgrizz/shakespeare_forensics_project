import json
from pathlib import Path

def create_play_data_json(directory):
    # Ensure directory exists
    path = Path(directory)
    if not path.exists():
        print(f"Directory not found: {directory}")
        return

    # Create play_data.json
    file_path = path / "play_data.json"
    if not file_path.exists():
        data = {
            "title": path.name,
            "description": "Example play data",
            "characters": {},
            "dialogue": []
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
            print(f"Created: {file_path}")
    else:
        print(f"Already exists: {file_path}")

# List of play directories
plays = [
    "desktop_creator/data/static/plays/Alls_Well_That_Ends_Well",
    "desktop_creator/data/static/plays/Antony_and_Cleopatra",
    "desktop_creator/data/static/plays/As_You_Like_It",
    "desktop_creator/data/static/plays/A_Midsummer_Nights_Dream",
    "desktop_creator/data/static/plays/Coriolanus",
    "desktop_creator/data/static/plays/Cymbeline",
    "desktop_creator/data/static/plays/Hamlet",
    "desktop_creator/data/static/plays/Henry_IV_Part_1",
    "desktop_creator/data/static/plays/Henry_IV_Part_2",
    "desktop_creator/data/static/plays/Henry_V",
    "desktop_creator/data/static/plays/Henry_VIII",
    "desktop_creator/data/static/plays/Henry_VI_Part_1",
    "desktop_creator/data/static/plays/Henry_VI_Part_2",
    "desktop_creator/data/static/plays/Henry_VI_Part_3",
    "desktop_creator/data/static/plays/Julius_Caesar",
    "desktop_creator/data/static/plays/King_John",
    "desktop_creator/data/static/plays/King_Lear",
    "desktop_creator/data/static/plays/Loves_Labours_Lost",
    "desktop_creator/data/static/plays/Macbeth",
    "desktop_creator/data/static/plays/Measure_for_Measure",
    "desktop_creator/data/static/plays/Much_Ado_About_Nothing",
    "desktop_creator/data/static/plays/Othello",
    "desktop_creator/data/static/plays/Pericles_Prince_of_Tyre",
    "desktop_creator/data/static/plays/Richard_II",
    "desktop_creator/data/static/plays/Richard_III",
    "desktop_creator/data/static/plays/Romeo_and_Juliet",
    "desktop_creator/data/static/plays/The_Comedy_of_Errors",
    "desktop_creator/data/static/plays/The_Merchant_of_Venice",
    "desktop_creator/data/static/plays/The_Merry_Wives_of_Windsor",
    "desktop_creator/data/static/plays/The_Taming_of_the_Shrew",
    "desktop_creator/data/static/plays/The_Tempest",
    "desktop_creator/data/static/plays/The_Two_Noble_Kinsmen",
    "desktop_creator/data/static/plays/The_Winters_Tale",
    "desktop_creator/data/static/plays/Timon_of_Athens",
    "desktop_creator/data/static/plays/Titus_Andronicus",
    "desktop_creator/data/static/plays/Troilus_and_Cressida",
    "desktop_creator/data/static/plays/Twelfth_Night",
    "desktop_creator/data/static/plays/Two_Gentlemen_of_Verona"
]

# Create play_data.json for each play
for play in plays:
    create_play_data_json(play)
