"""Module helpers"""
import json
from pathlib import Path
import os


def write_file_json(path: Path, content: dict) -> None:
    """Write a json file"""
    path.write_text(json.dumps(content, indent=4))


def update_settings(settings: dict) -> None:
    """Update the settings"""
    settings_file = get_setting_path()
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(json.dumps(settings, indent=4))


def get_setting(setting: str) -> str:
    """Get a setting"""
    return get_settings()[setting]


def get_settings() -> dict:
    """Get the settings"""
    with get_setting_path().open("r") as json_file:
        return json.load(json_file)


def get_pcc_base() -> Path:
    """Get the base path for pcc"""
    return Path.home() / ".pcc"


def get_setting_path() -> Path:
    """Get the path to the settings file"""
    return get_pcc_base() / "settings.json"


def get_server_path() -> Path:
    """Get the path to the servers file"""
    return get_pcc_base() / "servers.json"


def get_servers() -> dict:
    """Get the servers"""
    with get_server_path().open("r") as json_file:
        return json.load(json_file)


def update_servers() -> None:
    """Update the servers"""
    os.system("scp {fetch_command} {server_path}".format(
        fetch_command=get_setting("fetch_command"),
        server_path=get_server_path()
    ))
