"""SSH helper utilities for remote administration."""

from __future__ import annotations

from typing import Iterable, Optional

import paramiko

import helpers


def get_ssh_command(host: str) -> str:
    """Return the configured SSH command for ``host``."""
    return f"ssh {helpers.get_setting('ssh_user')}@{host}"


def get_ssh_client(host: str) -> paramiko.SSHClient:
    """Create and return a connected SSH client."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=helpers.get_setting("ssh_user"))
    return client


def run_remote_command(host: str, command: str, error_message: str) -> Iterable[str]:
    """Run ``command`` on ``host`` returning output lines."""
    try:
        client = get_ssh_client(host)
        _, stdout, _ = client.exec_command(command)
        output = stdout.readlines()
        client.close()
        return output
    except Exception as exc:  # pragma: no cover - network dependent
        return [error_message, f"Error: {exc}"]


def get_disk_space(host: str) -> Iterable[str]:
    return run_remote_command(host, "df -h", "Unable to get disk space information.")


def get_docker_services(host: str) -> Iterable[str]:
    return run_remote_command(
        host,
        "docker service ls",
        "Unable to get services from docker information.",
    )


def run_docker_system_prune(host: str) -> Iterable[str]:
    command = "docker system prune -a -f"
    return run_remote_command(host, command, f"Unable to run command {command} information.")


def run_docker_scale(host: str, service: str, replicas: int) -> Iterable[str]:
    command = f"docker service scale {service}={replicas}"
    return run_remote_command(host, command, f"Unable to run command {command} information.")


def run_reboot(host: str) -> Iterable[str]:
    command = "sudo reboot"
    return run_remote_command(host, command, f"Unable to run command {command} information.")


def get_server(slug: str) -> Optional[dict]:
    for server in helpers.get_servers():
        if isinstance(server, dict) and server.get("slug") == slug:
            return server
    return None
