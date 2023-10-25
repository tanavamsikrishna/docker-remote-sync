import sys
import tarfile

from fabric import Connection

from drsync.io_util import print_header
from drsync.subprocess_utils import check_subprocess_errors, start_subprocess


def sync_folders(
    source_folder: str, remote: str, port: int | None, destination_folder: str
):
    print_header("Syncing local changes with remote")
    rsync_executable = "rsync"
    ssh_cmd_with_port = ()
    if port is not None:
        ssh_cmd_with_port = ("-e", f"'ssh -p {port}'")
    try:
        process = start_subprocess(
            rsync_executable,
            "--times",
            "--delete",
            "--recursive",
            "--verbose",
            *ssh_cmd_with_port,
            f"{source_folder}/",
            f"{remote}:{destination_folder}",
        )
        while line := process.stdout.readline():
            print(line.rstrip())
        check_subprocess_errors(process.stderr.readlines())
    except FileNotFoundError as e:
        if e.filename == rsync_executable:
            print(f"Could not find {rsync_executable} executable", file=sys.stderr)
            sys.exit(1)
        else:
            raise e


def extract_tar_file(file, output_folder):
    print_header("Extracting the layers of image")
    with tarfile.open(fileobj=file, mode="r:") as tf:
        tf.extractall(path=output_folder)


def build_remote_tar(remote: str, port: int | None, folder: str):
    print_header("Building remote tar file")
    tar_file_loc = f"{folder}.tar"
    conn = Connection(host=remote, port=port)
    output = conn.run(f"tar cf {tar_file_loc} {folder}/*")
    print(output)
