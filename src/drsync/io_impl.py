import subprocess
import sys
from pathlib import Path
from typing import cast, final, override

from fabric import Connection, Result

from drsync.config import get_io_service
from drsync.io_interfaces import (
    CmdLineArgsService,
    ContainerService,
    LocalProcessExecService,
    RemoteCmdExecService,
)


@final
class AppleContainers(ContainerService):
    @override
    def save_docker_image(self, image: str, output_file: Path):
        command = ["container", "image", "save", image, "--output", str(output_file)]
        get_io_service(LocalProcessExecService).run_cmd(command)


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
        output: Result = cast(Result, self.connection.run(command))
        return output.stdout


@final
class PySubprocessService(LocalProcessExecService):
    @override
    def run_cmd(self, command: list[str]):
        _ = subprocess.check_call(args=command)
