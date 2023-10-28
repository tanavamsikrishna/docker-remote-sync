import argparse
import functools
import io
from tempfile import TemporaryDirectory

from drsync.docker_interface import save_docker_image
from drsync.remote import create_remote_folder, get_remote_conn, run_cmd_on_remote
from drsync.sync import (
    build_remote_tar,
    extract_tar_file,
    load_image_on_remote,
    sync_folders,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="docker-remote-sync",
        description="Utility to sync updated docker layers between 2 docker host machines",
        epilog="""
○ Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync
○ Example usage: `docker-remote-sync myalpine:latest remotehost "~/myalpine_cache"`
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "image_name", help="Docker image (along with tag) on local machine"
    )
    parser.add_argument("remote", help="Address of remote with")
    parser.add_argument("--port", help="Alternate ssh port on remote", required=False)
    parser.add_argument("remote_cache_folder", help="Cache folder on remote")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with TemporaryDirectory() as temp_extraction_folder, io.BytesIO() as temp_tar_file:
        remote = args.remote
        port = args.port
        image_name = args.image_name
        remote_cache_folder = args.remote_cache_folder
        save_docker_image(image_name, temp_tar_file)
        temp_tar_file.seek(0)
        extract_tar_file(temp_tar_file, temp_extraction_folder)
        rce = functools.partial(run_cmd_on_remote, conn=get_remote_conn(remote, port))

        create_remote_folder(remote_cache_folder, rce)
        sync_folders(temp_extraction_folder, remote, port, remote_cache_folder)
        remote_image_file = build_remote_tar(rce, remote_cache_folder)
        load_image_on_remote(rce, remote_image_file, image_name)


if __name__ == "__main__":
    main()
