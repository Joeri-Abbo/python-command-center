"""Module helpers"""
import paramiko

import helpers
from pssh.clients import SSHClient


def get_ssh_command(host):
    """Get the ssh command"""
    return "ssh {ssh_user}@{host}".format(
        ssh_user=helpers.get_setting("ssh_user"),
        host=host
    )


def get_ssh_client(host):
    """Get the ssh client"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=helpers.get_setting("ssh_user"))
    # TODO fix or change ssh client in build script
    return ssh_client


def run_remote_command(host, command, error_message):
    try:
        ssh_client = get_ssh_client(host)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.readlines()
        ssh_client.close()
        return output
    except Exception as e:
        return [
            error_message,
            "Error: {error}".format(error=e)
        ]


def get_disk_space(host):
    """Get the disk space"""
    return run_remote_command(host, "df -h", "Unable to get disk space information.")


def get_docker_services(host):
    """Get docker services"""
    return run_remote_command(host, "docker service ls", "Unable to get services from docker information.")


def run_docker_system_prune(host):
    """Run docker system prune"""
    command = "docker system prune -a -f"
    return run_remote_command(host, command, f"Unable to run command {command} information.")


def run_docker_scale(host, service, replicas):
    """Run docker service scale"""
    command = "docker service scale {service}={replicas}".format(
        service=service,
        replicas=replicas
    )
    return run_remote_command(host, command, f"Unable to run command {command} information.")


def run_reboot(host):
    """Run docker system prune"""
    command = "sudo reboot"

    return run_remote_command(host, command, f"Unable to run command {command} information.")


def get_server(slug):
    servers = helpers.get_servers()
    for server_item in servers:
        if slug == server_item['slug']:
            return server_item
    return None
