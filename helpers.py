import json
from pathlib import Path
import os


def write_file_json(path, content):
    with open(path, 'w') as fp:
        json.dump(content, fp, indent=4)


def update_settings(settings):
    settings_file = get_setting_path()
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    with settings_file.open(mode="w") as f:
        json.dump(settings, f, indent=4)


def get_setting(setting):
    return get_settings()[setting]


def get_settings():
    with open(get_setting_path(), "r") as json_file:
        return json.load(json_file)


def get_pcc_base():
    return Path.home() / ".pcc"


def get_setting_path():
    return get_pcc_base() / "settings.json"


def get_server_path():
    return get_pcc_base() / "servers.json"


def get_servers():
    with open(get_server_path(), "r") as json_file:
        return json.load(json_file)


def update_servers():
    os.system("scp {fetch_command} {servers_path}".format(
        fetch_command=get_setting("fetch_command"),
        servers_path=get_server_path()
    ))
