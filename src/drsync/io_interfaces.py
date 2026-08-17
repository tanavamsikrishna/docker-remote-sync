from abc import ABC, abstractmethod
from pathlib import Path


class Service(ABC):
    pass


class ContainerService(Service, ABC):
    @abstractmethod
    def save_docker_image(self, image: str, output_file: Path): ...


class CmdLineArgsService(Service, ABC):
    @abstractmethod
    def get_argv(self) -> list[str]: ...


class RemoteCmdExecService(Service, ABC):
    @abstractmethod
    def run_cmd(self, command: str) -> str: ...

    @abstractmethod
    def mkdir(self, path: str):...
