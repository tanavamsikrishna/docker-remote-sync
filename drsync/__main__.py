import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory

from drsync.docker import save_docker_image
from drsync.sync import extract_tar_file, sync_folders


if __name__ == "__main__":
    image_name = sys.argv[1]
    dest_folder = sys.argv[2]
    with NamedTemporaryFile() as temp_tar_file, TemporaryDirectory() as temp_extraction_folder:
        save_docker_image(image_name, temp_tar_file.name)
        extract_tar_file(temp_tar_file.name, temp_extraction_folder)
        sync_folders(temp_extraction_folder, dest_folder)
