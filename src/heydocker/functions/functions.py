import json
import logging
import os
import re
import subprocess

import docker

logger = logging.getLogger(__name__)


def check_network():
    """
    Check network speed, download speed and upload speed.

    :return: Network speed test result.
    :rtype: string
    """
    try:
        response = subprocess.check_output(["speedtest-cli", "--share"]).decode("utf-8")
        return f"Speedtest response: {response}"
    except subprocess.CalledProcessError as e:
        return "Network speed test failed."


def check_ip():
    """
    Check IP address.

    :return: IP address.
    :rtype: string
    """
    ip_address = subprocess.check_output(["curl", "ipinfo.io/ip"]).decode("utf-8")
    return f"IP Address: {ip_address}"


def list_images():
    """
    List docker images.

    :return: Docker images.
    :rtype: string
    """
    client = client = docker.from_env()
    images = client.images.list()

    response = json.dumps(
        [
            {
                "id": image.id,
                "labels": image.labels,
                "tags": image.tags,
                "short_id": image.short_id,
            }
            for image in images
        ]
    )

    return f"List Docker images: {response}"


def list_containers():
    """
    List docker containers.

    :return: Docker containers.
    :rtype: string
    """
    client = client = docker.from_env()
    containers = client.containers.list(all=True)

    json_message = {
        "containers": [
            {
                "container_id": container.short_id,
                "image": container.image.tags[0] if container.image.tags else None,
                "command": container.attrs["Config"]["Cmd"],
                "created": container.attrs["Created"],
                "status": container.status,
                "ports": container.attrs["NetworkSettings"]["Ports"],
                "name": container.name,
            }
            for container in containers
        ]
    }
    response = json.dumps(json_message)

    return f"List Docker containers: {response}"


def run_container(image_name: str):
    """
    Run docker container by image name.

    :param image_name: Docker image name.
    :type image_name: str
    :return: Docker container run result.
    :rtype: string
    """
    client = client = docker.from_env()
    image = client.images.get(image_name)

    if image == None:
        return f"{image_name} not found."

    container = client.containers.run(image, detach=True)
    return f"Image {image_name} has been run as container {container.name}."


def start_container(container_name: str):
    """
    Start docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container start result.
    :rtype: string
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"{container_name} not found."

    container.start()
    return f"Container {container_name} has been started."


def restart_container(container_name: str):
    """
    Restart docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container restart result.
    :rtype: string
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"{container_name} not found."

    container.restart()
    return f"Cotainer {container_name} has been restarted."


def remove_container(container_name: str):
    """
    Remove docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container remove result.
    :rtype: string
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    container.remove()
    return f"Container {container_name} has been removed."


def stop_container(container_name: str):
    """
    Stop docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container stop result.
    :rtype: string
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    container.stop()
    return f"Container {container_name} has been stopped."


def stats_container(container_name: str):
    """
    Get docker container stats by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container stats.
    :rtype: string
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    message = json.dumps(container.stats(stream=False))

    return "Container stats: {message}"
