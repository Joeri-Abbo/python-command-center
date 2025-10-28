from __future__ import annotations

from unittest import mock

import helpers
from main import create_app


def test_home_route(monkeypatch):
    app = create_app()
    app.config.update({"TESTING": True})
    monkeypatch.setattr(helpers, "decode_messages_param", lambda: {"main": "hi"})
    monkeypatch.setattr(helpers, "get_servers", lambda: [])
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_install_post(monkeypatch):
    app = create_app()
    app.config.update({"TESTING": True})

    stored = {}

    def fake_update(settings):
        stored.update(settings)

    monkeypatch.setattr(helpers, "update_settings", fake_update)
    client = app.test_client()
    response = client.post(
        "/install",
        data={"ssh_user": "alice", "fetch_command": "scp"},
        follow_redirects=False,
    )
    assert stored == {"ssh_user": "alice", "fetch_command": "scp"}
    assert response.status_code == 302


def test_fetch_triggers_update(monkeypatch):
    app = create_app()
    app.config.update({"TESTING": True})

    monkeypatch.setattr(helpers, "update_servers", lambda: None)
    client = app.test_client()
    with mock.patch("threading.Thread") as thread_mock:
        client.get("/fetch")
        kwargs = thread_mock.call_args.kwargs
        assert kwargs["target"] is helpers.update_servers
        assert kwargs["daemon"] is True
