import sys

import docker

from drsync.io_util import print_error, print_header


def save_docker_image(image_name, file):
    print_header("Reading a snapshot of the docker image")
    client = docker.from_env()
    try:
        image = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print_error(f"Image with identifier `{image_name}` not found")
        sys.exit(1)
    except docker.errors.APIError as e:
        print_error(e)
        sys.exit(1)

    for chunk in image.save():
        file.write(chunk)
