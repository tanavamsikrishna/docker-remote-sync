import argparse
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import get_args

from drsync.config import (
    ContainerServiceName,
    RemotePath,
    default_container_service_name,
    default_remote_workspace_folder,
    get_io_service,
    set_io_service,
)
from drsync.io_impl import AppleContainers, SysModuleArgv
from drsync.io_interfaces import CmdLineArgsService, ContainerService, RemoteCmdExecService
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
        self.port: int | None = None
        self.remote_workspace_folder: RemotePath = default_remote_workspace_folder
        self.container_service_name: ContainerServiceName = default_container_service_name
        self.additional_ssh_args: str = ""


def parse_arguments() -> CmdLineArgs:
    all_container_service_names = ",".join(get_args(ContainerServiceName))
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
    _ = parser.add_argument("--port", help="Alternate ssh port on remote", required=False)
    _ = parser.add_argument(
        "--remote-workspace-folder",
        help="The folder on remote server used as a workspace by the utility",
        required=False,
    )
    _ = parser.add_argument(
        "--container-service",
        help=f"Alternate container service. Defaults to `docker`. Available: {all_container_service_names}",
        required=False,
    )
    _ = parser.add_argument(
        "--additional-ssh-args",
        help="Additional ssh arguments enclosed in quotes",
    )
    return parser.parse_args(get_io_service(CmdLineArgsService).get_argv(), namespace=CmdLineArgs())


def main():
    set_io_service(CmdLineArgsService, SysModuleArgv())
    args = parse_arguments()
    match args.container_service_name:
        case "apple_containers":
            set_io_service(ContainerService, AppleContainers())
        case _:
            raise NotImplementedError

    with TemporaryDirectory() as temp_extraction_folder, NamedTemporaryFile("+bw") as temp_tar_file:
        temp_tar_file_path = Path(temp_tar_file.name)
        temp_extraction_folder_path = Path(temp_extraction_folder)
        # TODO: extract the following block into a function
        get_io_service(ContainerService).save_docker_image(args.image_name, temp_tar_file_path)
        _ = temp_tar_file.seek(0)
        extract_tar_file(temp_extraction_folder_path, temp_extraction_folder_path)
        _ = get_io_service(RemoteCmdExecService).run_cmd(
            f"mkdir -p {args.remote_workspace_folder}/{args.image_name}"
        )
        sync_folders(
            temp_extraction_folder_path,
            args.remote,
            args.port,
            args.remote_workspace_folder,
            args.additional_ssh_args,
        )
        remote_tar_file = RemotePath(f"{args.remote_workspace_folder}/image.tar")
        build_remote_tar(args.remote_workspace_folder, remote_tar_file)
        load_image_on_remote(remote_tar_file, args.image_name)


if __name__ == "__main__":
    main()
