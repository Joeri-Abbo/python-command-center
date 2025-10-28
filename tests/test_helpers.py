from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pytest

import helpers


@pytest.fixture()
def tmp_settings_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Dict[str, Path]:
    settings = tmp_path / "settings.json"
    servers = tmp_path / "servers.json"
    monkeypatch.setattr(helpers, "get_setting_path", lambda: settings)
    monkeypatch.setattr(helpers, "get_server_path", lambda: servers)
    return {"settings": settings, "servers": servers}


def test_write_file_json(tmp_path: Path) -> None:
    path = tmp_path / "data" / "file.json"
    helpers.write_file_json(path, {"foo": "bar"})
    assert json.loads(path.read_text(encoding="utf-8")) == {"foo": "bar"}


def test_get_settings_uses_defaults(tmp_settings_dir: Dict[str, Path]) -> None:
    assert helpers.get_settings() == helpers.DEFAULT_SETTINGS


def test_get_settings_merges_values(tmp_settings_dir: Dict[str, Path]) -> None:
    tmp_settings_dir["settings"].write_text(json.dumps({"ssh_user": "alice"}), encoding="utf-8")
    assert helpers.get_settings()["ssh_user"] == "alice"


def test_update_settings(tmp_settings_dir: Dict[str, Path]) -> None:
    helpers.update_settings({"ssh_user": "bob"})
    stored = json.loads(tmp_settings_dir["settings"].read_text(encoding="utf-8"))
    assert stored == {"ssh_user": "bob"}


def test_get_servers_returns_empty(tmp_settings_dir: Dict[str, Path]) -> None:
    assert list(helpers.get_servers()) == []


def test_get_servers_reads_file(tmp_settings_dir: Dict[str, Path]) -> None:
    tmp_settings_dir["servers"].write_text(json.dumps([{"slug": "srv"}]), encoding="utf-8")
    assert list(helpers.get_servers()) == [{"slug": "srv"}]


def test_update_servers_runs_command(
    tmp_settings_dir: Dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    commands = []

    def fake_run(cmd, check, shell, text, capture_output):
        commands.append(cmd)
        return None

    monkeypatch.setattr("helpers.subprocess.run", fake_run)
    helpers.update_settings({"fetch_command": "scp remote.json {server_path}"})
    helpers.update_servers()
    assert commands == [f"scp remote.json {tmp_settings_dir['servers']}"]


def test_decode_messages_param(app) -> None:
    with app.test_request_context("/?messages={\"main\": \"hi\"}"):
        assert helpers.decode_messages_param() == {"main": "hi"}


def test_decode_messages_param_invalid(app) -> None:
    with app.test_request_context("/?messages=not-json"):
        assert helpers.decode_messages_param() is None
