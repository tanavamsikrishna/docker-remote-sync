import argparse
import io
from tempfile import TemporaryDirectory

from drsync.docker_interface import save_docker_image
from drsync.sync import build_remote_tar, extract_tar_file, sync_folders


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="docker-remote-sync",
        description="Utility to sync updated docker layers between 2 docker host machines",
        epilog="""
○ Do not delete the cache folder on remote machine to be able to take advantage of incremental file sync
○ The tar file on remote which is the snapshot of local docker image with be at location <<destination_folder>>.tar
○ This tar file can be "loaded" into docker using `docker load -i <<destination_folder>>.tar`
○ Example usage: `docker-remote-sync myalpine:latest remotehost /tmp/myalpine_remotefolder`
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "image_name", help="Docker image (along with tag) on local machine"
    )
    parser.add_argument("remote", help="Address of remote with")
    parser.add_argument("--port", help="Alternate ssh port on remote", required=False)
    parser.add_argument("destination_folder", help="Cache folder on destination")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with TemporaryDirectory() as temp_extraction_folder, io.BytesIO() as temp_tar_file:
        save_docker_image(args.image_name, temp_tar_file)
        temp_tar_file.seek(0)
        extract_tar_file(temp_tar_file, temp_extraction_folder)
        sync_folders(
            temp_extraction_folder, args.remote, args.port, args.destination_folder
        )
        build_remote_tar(args.remote, args.port, args.destination_folder)


if __name__ == "__main__":
    main()
