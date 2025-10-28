from __future__ import annotations

from unittest import mock

import pytest

import server_helper


def test_get_ssh_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("helpers.get_setting", lambda key, default="": "user")
    assert server_helper.get_ssh_command("example.com") == "ssh user@example.com"


def test_get_server(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("helpers.get_servers", lambda: [{"slug": "srv", "title": "Srv"}])
    assert server_helper.get_server("srv") == {"slug": "srv", "title": "Srv"}
    assert server_helper.get_server("missing") is None


def test_run_remote_command_handles_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        server_helper, "get_ssh_client", mock.Mock(side_effect=RuntimeError("boom"))
    )
    output = server_helper.run_remote_command("example.com", "ls", "error")
    assert output[0] == "error"
    assert "boom" in output[1]
