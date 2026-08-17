import sys
from pathlib import Path
from typing import final, override

from fabric import Connection, Result

from drsync.io_interfaces import CmdLineArgsService, ContainerService, RemoteCmdExecService


@final
class AppleContainers(ContainerService):
    @override
    def save_docker_image(self, image: str, output_file: Path):
        pass


@final
class SysModuleArgv(CmdLineArgsService):
    @override
    def get_argv(self) -> list[str]:
        return sys.argv


@final
class FabricRemoteExec(RemoteCmdExecService):
    def __init__(self, host: str, port: int | None):
        self.connection = Connection(host=host, port=port)

    @override
    def run_cmd(self, command: str) -> str:
        output: Result = self.connection.run(command)
        return output.stdout

    @override
    def mkdir(self, path: str):
        self.connection.run(f"mkdir -p {path.absolute()}")
