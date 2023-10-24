from drsync.io_util import print_header
from drsync.subprocess_utils import check_subprocess_errors, start_subprocess


def save_docker_image(image, file):
    print_header("Saving the docker image to a file")
    docker_executable = "docker"
    process = start_subprocess(docker_executable, "save", "--output", file, image)
    output = process.stdout.readlines()
    check_subprocess_errors(process.stderr.readlines())
    return output
