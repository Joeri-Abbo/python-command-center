import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from helpers import (
    write_file_json,
    update_settings,
    get_setting,
    get_settings,
    get_pcc_base,
    get_setting_path,
    get_server_path,
    get_servers,
    update_servers,
)


class TestWriteFileJson(unittest.TestCase):
    def test_write_file_json(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            path = Path(temp_file.name)
            content = {"key": "value"}

            write_file_json(path, content)

            with path.open("r") as f:
                self.assertEqual(json.load(f), content)


class TestGetSettings(unittest.TestCase):
    @patch("helpers.get_setting_path")
    def test_get_settings(self, mock_get_setting_path):
        mock_file = mock_open(read_data=json.dumps({"key": "value"}))
        mock_get_setting_path.return_value.open.return_value = mock_file()

        settings = get_settings()

        self.assertEqual(settings, {"key": "value"})


class TestGetSettingPath(unittest.TestCase):
    def test_get_setting_path(self):
        with patch.object(Path, "home", return_value=Path("/home/user")):
            setting_path = get_setting_path()
            self.assertEqual(setting_path, Path("/home/user/.pcc/settings.json"))


class TestGetServerPath(unittest.TestCase):
    def test_get_server_path(self):
        with patch.object(Path, "home", return_value=Path("/home/user")):
            server_path = get_server_path()
            self.assertEqual(server_path, Path("/home/user/.pcc/servers.json"))


class TestGetServers(unittest.TestCase):
    @patch("helpers.get_server_path")
    def test_get_servers(self, mock_get_server_path):
        mock_file = mock_open(read_data=json.dumps({"key": "value"}))
        mock_get_server_path.return_value.open.return_value = mock_file()

        servers = get_servers()

        self.assertEqual(servers, {"key": "value"})


class TestUpdateServers(unittest.TestCase):
    @patch("helpers.get_setting")
    @patch("helpers.get_server_path")
    @patch("os.system")
    def test_update_servers(self, mock_system, mock_get_server_path, mock_get_setting):
        mock_get_setting.return_value = "fetch_command"
        mock_get_server_path.return_value = Path("/path/to/servers.json")

        update_servers()

        mock_system.assert_called_once_with("scp fetch_command /path/to/servers.json")
