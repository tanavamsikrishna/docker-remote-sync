import re
import sys
import tarfile
from collections.abc import Callable
from pathlib import Path

from drsync.config import RemotePath
from drsync.io_util import print_error, print_header
from drsync.subprocess_utils import check_subprocess_errors, start_subprocess


def sync_folders(
    source_folder: Path,
    remote: str,
    port: int | None,
    remote_folder: str,
    additional_ssh_args: str | None = None,
):
    print_header("Syncing local changes with remote")
    rsync_executable = "rsync"
    ssh_args: list[str] = []
    if additional_ssh_args:
        ssh_args.append(additional_ssh_args)
    if port is not None:
        ssh_args.append(f"-p {port}")

    rsync_ssh_args = ()
    if ssh_args:
        rsync_ssh_args = ("-e", f"ssh {' '.join(ssh_args)}")
    try:
        process = start_subprocess(
            rsync_executable,
            "--delete",
            "--archive",
            "--ignore-times",
            "--recursive",
            "--verbose",
            *rsync_ssh_args,
            f"{source_folder}/",
            f"{remote}:{remote_folder}",
            output="print",
            text=True,
        )
        _ = process.wait()
        if process.stderr is not None:
            check_subprocess_errors(process.stderr.readlines())
        if process.returncode != 0:
            sys.exit(process.returncode)
    except FileNotFoundError as e:
        if e.filename == rsync_executable:
            print(f"Could not find {rsync_executable} executable", file=sys.stderr)
            sys.exit(1)
        else:
            raise


def extract_tar_file(file: Path, output_folder: Path):
    print_header("Extracting the layers of image")
    with tarfile.open(name=file, mode="r:") as tf:
        tf.extractall(path=output_folder)


def build_remote_tar(rce: Callable[[str], str], folder: str):
    print_header("Building remote tar file")
    tar_file_loc = f"{folder}/image.tar"
    print(f"Remote image file is: {tar_file_loc}")
    output = rce(f"cd {folder} && tar cf {tar_file_loc} *")
    print(output)
    return tar_file_loc


def get_build_remote_tar_cmd(folder: RemotePath) -> str:
    print_header("Building remote tar file")
    tar_file_loc = f"{folder}/image.tar"
    print(f"Remote image file is: {tar_file_loc}")
    return f"cd {folder} && tar cf {tar_file_loc} *"


def load_image_on_remote(rce: Callable[[str], str], image_file: str, image_name: str):
    """
    rce: Remote command executor
    """
    print_header("Loading docker image on remote")
    output = rce(f"docker load -i {image_file} && rm {image_file}")

    output_id_leading_str = "Loaded image ID: sha256:"
    if output.startswith(output_id_leading_str):
        image_sha256 = output.replace(output_id_leading_str, "").strip()
        output = rce(f"docker tag {image_sha256} {image_name}")
        print(output)
    elif len(matches := re.findall(".*Loaded image: (.*)", output)) > 0:
        output = rce(f"docker tag {matches[0]} {image_name}")
        print(output)
    else:
        print_error(f"Unexpected output from docker load command execution\n{output}")
        sys.exit(1)
