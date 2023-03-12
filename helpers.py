import json
from pathlib import Path


def write_file_json(path, content):
    with open(path, 'w') as fp:
        json.dump(content, fp, indent=4)


def update_settings(settings):
    settings_file = Path.home() / ".pcc" / "settings.json"
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    with settings_file.open(mode="w") as f:
        json.dump(settings, f, indent=4)
