import argparse
import functools
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from drsync.config import (
    default_docker_command,
    default_remote_workspace_folder,
    default_ssh_port,
    get_io_service,
    set_io_service,
)
from drsync.io_impl import AppleContainers, SysModuleArgv
from drsync.io_interfaces import CmdLineArgsService, ContainerService, RemoteCmdExecService
from drsync.remote import get_remote_conn, run_cmd_on_remote
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
    return parser.parse_args(get_io_service(CmdLineArgsService).get_argv(), namespace=CmdLineArgs())


def main():
    set_io_service(CmdLineArgsService, SysModuleArgv())
    args = parse_arguments()
    set_io_service(ContainerService, AppleContainers())
    with TemporaryDirectory() as temp_extraction_folder, NamedTemporaryFile("+bw") as temp_tar_file:
        temp_tar_file_path = Path(temp_tar_file.name)
        temp_extraction_folder_path  = Path(temp_extraction_folder)
        get_io_service(ContainerService).save_docker_image(args.image_name, temp_tar_file_path)
        _ = temp_tar_file.seek(0)
        extract_tar_file(temp_extraction_folder_path, temp_extraction_folder_path)
        get_io_service(RemoteCmdExecService).mkdir(f"{args.remote_workspace_folder}/{args.image_name}")
        sync_folders(
            temp_extraction_folder_path,
            args.remote,
            args.port,
            args.remote_workspace_folder,
            args.additional_ssh_args,
        )
        rce = functools.partial(run_cmd_on_remote, conn=get_remote_conn(args.remote, args.port))
        remote_image_file = build_remote_tar(rce, args.remote_workspace_folder)
        load_image_on_remote(rce, remote_image_file, args.image_name)


if __name__ == "__main__":
    main()
