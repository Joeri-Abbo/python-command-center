import json
from pathlib import Path
import os


def write_file_json(path: Path, content: dict) -> None:
    path.write_text(json.dumps(content, indent=4))


def update_settings(settings: dict) -> None:
    settings_file = get_setting_path()
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(json.dumps(settings, indent=4))


def get_setting(setting: str) -> str:
    return get_settings()[setting]


def get_settings() -> dict:
    with get_setting_path().open("r") as json_file:
        return json.load(json_file)


def get_pcc_base() -> Path:
    return Path.home() / ".pcc"


def get_setting_path() -> Path:
    return get_pcc_base() / "settings.json"


def get_server_path() -> Path:
    return get_pcc_base() / "servers.json"


def get_servers() -> dict:
    with get_server_path().open("r") as json_file:
        return json.load(json_file)


def update_servers() -> None:
    os.system("scp {fetch_command} {servers_path}".format(
        fetch_command=get_setting("fetch_command"),
        servers_path=get_server_path()
    ))
