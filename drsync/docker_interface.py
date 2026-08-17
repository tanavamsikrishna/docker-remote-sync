from typing import BinaryIO

from drsync.io_util import print_header
from drsync.subprocess_utils import start_subprocess


def save_docker_image(docker_executable: str, image_name: str, file: BinaryIO):
    print_header(f"Saving a snapshot of the docker image: {image_name} to {file}")
    process = start_subprocess(*docker_executable.split(), "save", image_name, text=False)
    stdout_data, _ = process.communicate()
    _ = file.write(stdout_data)
