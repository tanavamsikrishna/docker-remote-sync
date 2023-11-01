from typing import BinaryIO

from drsync.io_util import print_header
from drsync.subprocess_utils import start_subprocess


def save_docker_image(image_name, file: BinaryIO):
    print_header("Reading a snapshot of the docker image")
    docker_executable = "docker"
    process = start_subprocess(docker_executable, "save", image_name, text=False)
    stdout_data, _ = process.communicate()
    file.write(stdout_data)
