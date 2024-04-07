from typing import BinaryIO

from drsync.io_util import print_header
from drsync.subprocess_utils import start_subprocess


def save_docker_image(docker_executable: str, image_name, file: BinaryIO):
    print_header("Reading a snapshot of the docker image")
    process = start_subprocess(
        *docker_executable.split(), "save", image_name, text=False
    )
    stdout_data, _ = process.communicate()
    file.write(stdout_data)
