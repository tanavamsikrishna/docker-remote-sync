import argparse
import functools
import io
from tempfile import TemporaryDirectory

from drsync.config import (
    default_docker_command,
    default_remote_workspace_folder,
    default_ssh_port,
    get_sys_argv,
)
from drsync.docker_interface import save_docker_image
from drsync.remote import create_remote_folder, get_remote_conn, run_cmd_on_remote
from drsync.sync import (
    build_remote_tar,
    extract_tar_file,
    load_image_on_remote,
    sync_folders,
)


class CmdLineArgs:
    def __init__(self) -> None:
        self.image_name: str
        self.remote: str
        self.port: int
        self.remote_workspace_folder: str
        self.docker_cmd: str
        self.additional_ssh_args: str


def parse_arguments() -> CmdLineArgs:
    parser = argparse.ArgumentParser(
        prog="docker-remote-sync",
        description="Utility to sync updated docker layers between two docker host machines",
        epilog="""
○ Do not delete the cache folder on the remote machine to be able to take advantage of incremental file sync
○ Example usage: `docker-remote-sync alpine:latest remotehost`
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _ = parser.add_argument("image_name", help="Docker image on local machine")
    _ = parser.add_argument("remote", help="Address of remote")
    _ = parser.add_argument(
        "--port", help="Alternate ssh port on remote", required=False, default=default_ssh_port
    )
    _ = parser.add_argument(
        "remote_workspace_folder",
        default=default_remote_workspace_folder,
        help="The folder on remote server used as a workspace by the utility",
    )
    _ = parser.add_argument(
        "--docker-cmd",
        help="Alternate docker command. Defaults to `docker`. Eg. `colima x - docker` or `podman`",
        default=default_docker_command,
    )
    _ = parser.add_argument(
        "--additional-ssh-args",
        default="",
        help="Additional ssh arguments enclosed in quotes",
    )
    return parser.parse_args(get_sys_argv(), namespace=CmdLineArgs())


def main():
    args = parse_arguments()
    with TemporaryDirectory() as temp_extraction_folder, io.BytesIO() as temp_tar_file:
        remote = args.remote
        port = args.port
        image_name = args.image_name
        docker_cmd = args.docker_cmd
        additional_ssh_args = args.additional_ssh_args

        save_docker_image(docker_cmd, image_name, temp_tar_file)
        _ = temp_tar_file.seek(0)
        extract_tar_file(temp_tar_file, temp_extraction_folder)
        rce = functools.partial(run_cmd_on_remote, conn=get_remote_conn(remote, port))

        _ = create_remote_folder(args.remote_workspace_folder, rce)
        sync_folders(
            temp_extraction_folder,
            remote,
            port,
            args.remote_workspace_folder,
            additional_ssh_args,
        )
        remote_image_file = build_remote_tar(rce, args.remote_workspace_folder)
        load_image_on_remote(rce, remote_image_file, image_name)


if __name__ == "__main__":
    main()
