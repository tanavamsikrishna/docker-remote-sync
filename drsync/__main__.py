import io
from tempfile import TemporaryDirectory
import argparse

from drsync.docker_interface import save_docker_image
from drsync.sync import extract_tar_file, sync_folders


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="docker-remote-sync",
        description="Utility to sync updated docker layers between 2 machines",
    )
    parser.add_argument(
        "image_name", help="Docker image (along with tag) on local machine"
    )
    parser.add_argument("destination_folder", help="Destination folder")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with TemporaryDirectory() as temp_extraction_folder, io.BytesIO() as temp_tar_file:
        save_docker_image(args.image_name, temp_tar_file)
        temp_tar_file.seek(0)
        extract_tar_file(temp_tar_file, temp_extraction_folder)
        sync_folders(temp_extraction_folder, args.destination_folder)


if __name__ == "__main__":
    main()
