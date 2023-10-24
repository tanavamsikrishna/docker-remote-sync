import sys
import tarfile
from drsync.io_util import print_header

from drsync.subprocess_utils import check_subprocess_errors, start_subprocess


def sync_folders(source_folder, destination_folder):
    print_header("Syncing local changes with remote")
    rsync_executable = "rsync"
    try:
        process = start_subprocess(
            rsync_executable,
            "-t",
            "--recursive",
            "--verbose",
            f"{source_folder}/",
            destination_folder,
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
    with tarfile.open(file, mode="r:") as tf:
        tf.extractall(path=output_folder)
