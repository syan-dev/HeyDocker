import json
import logging
import os
import re
import subprocess

import docker

from heydocker.functions.utils import (
    convert_container_to_json,
    convert_image_to_json,
    convert_stats,
    convert_volume_to_json,
)

logger = logging.getLogger(__name__)

# ==================== #
#     Machine Info     #
# ==================== #


def check_network() -> str:
    """
    Check network speed, download speed and upload speed.

    :return: Network speed test result.
    :rtype: str
    """
    try:
        response = subprocess.check_output(["speedtest-cli", "--share"]).decode("utf-8")
        return f"Speedtest response: {response}"
    except subprocess.CalledProcessError as e:
        return "Network speed test failed."


def check_ip() -> str:
    """
    Check IP address.

    :return: IP address.
    :rtype: str
    """
    ip_address = subprocess.check_output(["curl", "ipinfo.io/ip"]).decode("utf-8")
    return f"IP Address: {ip_address}"


def check_disk_usage() -> str:
    """
    Check disk usage.

    :return: Disk usage.
    :rtype: str
    """
    usage = subprocess.check_output(["df", "-h"]).decode("utf-8")
    return f"Disk usage: {usage}"


# ==================== #
#     Docker Image     #
# ==================== #


def list_images() -> str:
    """
    List all docker images.

    :return: Docker images.
    :rtype: str
    """
    client = client = docker.from_env()
    images = client.images.list()

    json_message = {"docker_images": [convert_image_to_json(image) for image in images]}
    response = json.dumps(json_message)

    return response


def get_image(image_name: str) -> str:
    """
    Get raw data of docker image by name.

    :param image_name: Docker image name.
    :type image_name: str

    :return: Docker image.
    :rtype: str
    """
    client = client = docker.from_env()
    image = client.images.get(image_name)

    if image == None:
        return f"Docker image {image_name} not found."

    json_message = {"docker_image": image.attrs}
    response = json.dumps(json_message)

    return response


def remove_image(image_name: str) -> str:
    """
    Remove docker image by name.

    :param image_name: Docker image name.
    :type image_name: str
    """
    client = client = docker.from_env()
    image = client.images.get(image_name)

    if image == None:
        return f"Docker image {image_name} not found."

    image.remove()
    return f"Docker image {image_name} has been removed."


def pull_image(repository: str, tag: str) -> str:
    """
    Pull docker image by repository and tag.

    :param repository: Docker image repository.
    :type repository: str
    :param tag: Docker image tag.
    :type tag: str

    :return: Docker image pull result.
    :rtype: str
    """
    client = client = docker.from_env()
    image = client.images.pull(repository, tag)

    if image == None:
        return f"Docker image {repository}:{tag} not found."

    return f"Docker image {repository}:{tag} has been pulled."


def prune_images() -> str:
    """
    Delete all unused docker images.

    :return: Docker images prune result.
    :rtype: str
    """
    client = client = docker.from_env()
    images = client.images.prune()

    response = json.dumps(images)

    return f"Prune Docker images: {response}"


# ==================== #
#   Docker Container   #
# ==================== #


def list_containers() -> str:
    """
    List all docker containers.

    :return: Docker containers.
    :rtype: str
    """
    client = client = docker.from_env()
    containers = client.containers.list(all=True)

    json_message = {
        "docker_containers": [
            convert_container_to_json(container) for container in containers
        ]
    }
    response = json.dumps(json_message)

    return response


def get_container(container_name: str) -> str:
    """
    Get raw data of docker container by name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Docker container {container_name} not found."

    json_message = {"docker_container": container.attrs}
    response = json.dumps(json_message)

    return response


def run_container(image_name: str) -> str:
    """
    Run docker container by image name.

    :param image_name: Docker image name.
    :type image_name: str
    :return: Docker container run result.
    :rtype: str
    """
    client = client = docker.from_env()
    image = client.images.get(image_name)

    if image == None:
        return f"{image_name} not found."

    container = client.containers.run(image, detach=True)
    return f"Image {image_name} has been run as container {container.name}."


def create_container(image_name: str) -> str:
    """
    Create docker container by image name.

    :param image_name: Docker image name.
    :type image_name: str

    :return: Docker container create result.
    :rtype: str
    """
    client = client = docker.from_env()
    image = client.images.get(image_name)

    if image == None:
        return f"{image_name} not found."

    container = client.containers.create(image)
    return f"Image {image_name} has been created as container {container.name}."


def start_container(container_name: str) -> str:
    """
    Start docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container start result.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"{container_name} not found."

    container.start()
    return f"Container {container_name} has been started."


def restart_container(container_name: str) -> str:
    """
    Restart docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container restart result.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"{container_name} not found."

    container.restart()
    return f"Cotainer {container_name} has been restarted."


def remove_container(container_name: str) -> str:
    """
    Remove docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container remove result.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    container.remove()
    return f"Container {container_name} has been removed."


def stop_container(container_name: str) -> str:
    """
    Stop docker container by container name.

    :param container_name: Docker container name.
    :type container_name: str
    :return: Docker container stop result.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    container.stop()
    return f"Container {container_name} has been stopped."


def stats_container(container_name: str) -> str:
    """
    Get docker container stats by container name.

    :param container_name: Docker container name.
    :type container_name: str

    :return: Docker container stats.
    :rtype: str
    """
    client = client = docker.from_env()
    container = client.containers.get(container_name)

    if container == None:
        return f"Container {container_name} not found."

    # message = json.dumps(container.stats(stream=False))
    stats = container.stats(stream=False)
    logger.info(f"Stats: {stats}")
    message = convert_stats(stats)

    return f"Container stats: {message}"


def prune_containers() -> str:
    """
    Delete all stopped docker containers.

    :return: Docker containers prune result.
    :rtype: str
    """
    client = client = docker.from_env()
    containers = client.containers.prune()

    response = json.dumps(containers)

    return f"Prune Docker containers: {response}"


# ==================== #
#    Docker Volume     #
# ==================== #


def list_volumes() -> str:
    """
    List all docker volumes.

    :return: Docker volumes.
    :rtype: str
    """
    client = client = docker.from_env()
    volumes = client.volumes.list()

    json_message = {
        "docker_volumes": [convert_volume_to_json(volume) for volume in volumes]
    }
    response = json.dumps(json_message)

    return response


def get_volume(volume_name: str) -> str:
    """
    Get raw data of docker volume by name.

    :param volume_name: Docker volume name.
    :type volume_name: str

    :return: Docker volume.
    :rtype: str
    """
    client = client = docker.from_env()
    volume = client.volumes.get(volume_name)

    if volume == None:
        return f"Docker volume {volume_name} not found."

    json_message = {"docker_volume": volume.attrs}
    response = json.dumps(json_message)

    return response


def create_volume():
    """
    Create docker volume.

    :return: Docker volume create result.
    :rtype: str
    """
    client = client = docker.from_env()
    volume = client.volumes.create()

    return f"Volume {volume.name} has been created."


def remove_volume(volume_name: str) -> str:
    """
    Remove docker volume by volume name.

    :param volume_name: Docker volume name.
    :type volume_name: str

    :return: Docker volume remove result.
    :rtype: str
    """
    client = client = docker.from_env()
    volume = client.volumes.get(volume_name)

    if volume == None:
        return f"Volume {volume_name} not found."

    volume.remove()
    return f"Volume {volume_name} has been removed."


def prune_volume() -> str:
    """
    Delete all unused docker volumes.

    :return: Docker volumes prune result.
    :rtype: str
    """
    client = client = docker.from_env()
    volumes = client.volumes.prune()

    response = json.dumps(volumes)

    return f"Prune Docker volumes: {response}"
