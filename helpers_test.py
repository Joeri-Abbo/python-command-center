"""Test the helpers module"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from helpers import (
    write_file_json,
    get_settings,
    get_setting_path,
    get_server_path,
    get_servers,
    update_servers,
)


class TestWriteFileJson(unittest.TestCase):
    """Test the write_file_json function"""

    def test_write_file_json(self):
        """Test writing a json file"""
        with tempfile.NamedTemporaryFile() as temp_file:
            path = Path(temp_file.name)
            content = {"key": "value"}

            write_file_json(path, content)

            with path.open("r", encoding="utf-8") as file:
                self.assertEqual(json.load(file), content)


class TestGetSettings(unittest.TestCase):
    """Test the get_settings function"""

    @patch("helpers.get_setting_path")
    def test_get_settings(self, mock_get_setting_path):
        """Test getting the settings"""
        mock_file = mock_open(read_data=json.dumps({"key": "value"}))
        mock_get_setting_path.return_value.open.return_value = mock_file()

        settings = get_settings()

        self.assertEqual(settings, {"key": "value"})


class TestGetSettingPath(unittest.TestCase):
    """Test the get_setting_path function"""

    def test_get_setting_path(self):
        """Test getting the setting path"""
        with patch.object(Path, "home", return_value=Path("/home/user")):
            setting_path = get_setting_path()
            self.assertEqual(setting_path, Path("/home/user/.pcc/settings.json"))


class TestGetServerPath(unittest.TestCase):
    """Test the get_server_path function"""

    def test_get_server_path(self):
        """Test getting the server path"""
        with patch.object(Path, "home", return_value=Path("/home/user")):
            server_path = get_server_path()
            self.assertEqual(server_path, Path("/home/user/.pcc/servers.json"))


class TestGetServers(unittest.TestCase):
    """Test the get_servers function"""

    @patch("helpers.get_server_path")
    def test_get_servers(self, mock_get_server_path):
        """Test getting the servers"""
        mock_file = mock_open(read_data=json.dumps({"key": "value"}))
        mock_get_server_path.return_value.open.return_value = mock_file()

        servers = get_servers()

        self.assertEqual(servers, {"key": "value"})


class TestUpdateServers(unittest.TestCase):
    """Test the update_servers function"""

    @patch("helpers.get_setting")
    @patch("helpers.get_server_path")
    @patch("os.system")
    def test_update_servers(self, mock_system, mock_get_server_path, mock_get_setting):
        """Test updating the servers"""
        mock_get_setting.return_value = "fetch_command"
        mock_get_server_path.return_value = Path("/path/to/servers.json")

        update_servers()

        mock_system.assert_called_once_with("scp fetch_command /path/to/servers.json")
