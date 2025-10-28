"""Utility helpers for configuration and server metadata."""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from flask import request

LOGGER = logging.getLogger(__name__)

DEFAULT_SETTINGS: Dict[str, Any] = {"ssh_user": "", "fetch_command": ""}


def write_file_json(path: Path, content: Dict[str, Any]) -> None:
    """Write ``content`` to ``path`` as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2), encoding="utf-8")


def load_json(path: Path, default: Any) -> Any:
    """Load JSON data from ``path`` or return ``default`` when missing."""
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:  # pragma: no cover - rare corruption
        raise ValueError(f"Invalid JSON in {path}") from exc


def get_pcc_base() -> Path:
    """Return the PCC base directory."""
    return Path.home() / ".pcc"


def get_setting_path() -> Path:
    """Return the path to the settings file."""
    return get_pcc_base() / "settings.json"


def get_server_path() -> Path:
    """Return the path to the servers file."""
    return get_pcc_base() / "servers.json"


def get_settings(path: Path | None = None) -> Dict[str, Any]:
    """Return merged settings from disk and defaults."""
    settings_path = path or get_setting_path()
    loaded = load_json(settings_path, {})
    merged = DEFAULT_SETTINGS.copy()
    merged.update(loaded)
    return merged


def get_setting(key: str, default: Optional[str] = "") -> str:
    """Return a single setting value."""
    return str(get_settings().get(key, default or ""))


def update_settings(settings: Dict[str, Any], path: Path | None = None) -> None:
    """Persist settings to disk."""
    write_file_json(path or get_setting_path(), settings)


def get_servers(path: Path | None = None) -> Iterable[Dict[str, Any]]:
    """Return stored server definitions."""
    return load_json(path or get_server_path(), [])


def build_fetch_command(server_path: Path, template: Optional[str] = None) -> str:
    """Create the fetch command string using configuration."""
    command_template = template or get_setting("fetch_command")
    if not command_template:
        raise RuntimeError("Fetch command not configured")
    return command_template.format(server_path=server_path)


def update_servers(
    command_template: Optional[str] = None, *, server_path: Optional[Path] = None
) -> None:
    """Fetch the latest servers file using the configured command."""
    target_path = server_path or get_server_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    command = build_fetch_command(target_path, template=command_template)
    try:
        subprocess.run(command, check=True, shell=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - network dependent
        LOGGER.error("Fetching servers failed: %s", exc)
        raise RuntimeError("Failed to fetch servers") from exc


def decode_messages_param() -> Optional[Dict[str, Any]]:
    """Decode the optional ``messages`` query parameter."""
    raw_value = request.args.get("messages")
    if not raw_value:
        return None
    try:
        payload = json.loads(raw_value)
    except json.JSONDecodeError:
        LOGGER.debug("Ignoring malformed messages payload: %s", raw_value)
        return None
    if isinstance(payload, dict):
        return payload
    return None
