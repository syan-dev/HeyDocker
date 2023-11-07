from datetime import datetime

from dateutil.parser import isoparse


def format_time_difference(created_str):
    created_date = isoparse(created_str).replace(tzinfo=None)
    current_date = datetime.now()
    time_difference = current_date - created_date

    if time_difference.days > 365:
        # If the time difference is greater than a year, show the number of years ago
        years = time_difference.days // 365
        return f"{years} years ago"
    elif time_difference.days > 0:
        # If the time difference is greater than a day, show the number of days ago
        return f"{time_difference.days} days ago"
    elif time_difference.seconds < 60:
        # If the time difference is less than a minute, show the number of seconds ago
        return f"{time_difference.seconds} seconds ago"
    elif time_difference.seconds < 3600:
        # If the time difference is less than an hour, show the number of minutes ago
        minutes = time_difference.seconds // 60
        return f"{minutes} minutes ago"
    else:
        # Otherwise, show the number of hours ago
        hours = time_difference.seconds // 3600
        return f"{hours} hours ago"


def format_byte(byte):
    """
    Convert B to kB, MB, GB

    :param byte: number of bytes
    :type byte: int
    """
    if byte < 1024:
        return f"{byte}B"
    elif byte < 1024 * 1024:
        return f"{byte / 1024:.2f}kB"
    elif byte < 1024 * 1024 * 1024:
        return f"{byte / 1024 / 1024:.2f}MB"
    else:
        return f"{byte / 1024 / 1024 / 1024:.2f}GB"


def convert_container_to_json(container):
    """
    Convert docker container to json.

    :param container: Docker container.
    :type container: docker.models.containers.Container

    :return: Docker container json.
    :rtype: dict
    """
    return {
        "short_id": container.short_id,
        "name": container.name,
        "image": container.image.tags[0],
        "status": container.status,
        "created": format_time_difference(container.attrs["Created"]),
        "ports": container.attrs["NetworkSettings"]["Ports"],
        "labels": container.attrs["Config"]["Labels"],
    }


def convert_image_to_json(image):
    """
    Convert docker image to json.

    :param image: Docker image.
    :type image: docker.models.images.Image

    :return: Docker image json.
    :rtype: dict
    """
    return {
        "short_id": image.short_id,
        "tags": image.tags,
        "created": format_time_difference(image.attrs["Created"]),
        "size": image.attrs["Size"],
    }


def convert_volume_to_json(volume):
    """
    Convert docker volume to json.

    :param volume: Docker volume.
    :type volume: docker.models.volumes.Volume

    :return: Docker volume json.
    :rtype: dict
    """
    return {
        "short_id": volume.short_id,
        "name": volume.name,
        "created": format_time_difference(volume.attrs["CreatedAt"]),
    }


def convert_stats(stats):
    """
    Convert container stats easier to understand.

    :param container_stats: _description_
    :type container_stats: _type_
    """
    # cpu %
    total_usage = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_cpu_usage = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )
    cpu_count = stats["cpu_stats"]["online_cpus"]
    cpu_percentage = (total_usage / system_cpu_usage) * 100 * cpu_count
    # convert float with 2 decimal
    cpu_percentage = "{:.2f}%".format(cpu_percentage)

    # mem usage / limit
    mem_usage = stats["memory_stats"]["usage"]
    mem_limit = stats["memory_stats"]["limit"]
    # mem %
    mem_percentage = (mem_usage / mem_limit) * 100
    # convert float with 2 decimal
    mem_percentage = "{:.2f}%".format(mem_percentage)

    # net i/o
    net_rx = stats["networks"]["eth0"]["rx_bytes"]
    net_tx = stats["networks"]["eth0"]["tx_bytes"]

    # block i/o
    block_read = stats["blkio_stats"]["io_service_bytes_recursive"][0]["value"]
    block_write = stats["blkio_stats"]["io_service_bytes_recursive"][1]["value"]

    # pids
    pids = stats["pids_stats"]["current"]

    return {
        "cpu_percentage": cpu_percentage,
        "mem_usage": format_byte(mem_usage),
        "mem_limit": format_byte(mem_limit),
        "mem_percentage": mem_percentage,
        "net_rx": net_rx,
        "net_tx": net_tx,
        "block_read": format_byte(block_read),
        "block_write": format_byte(block_write),
        "pids": pids,
    }
