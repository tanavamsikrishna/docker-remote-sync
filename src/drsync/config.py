from typing import Literal, NewType, cast

from drsync.io_interfaces import Service

RemotePath = NewType("RemotePath", str)
type ContainerServiceName = Literal["apple_containers", "docker", "colima"]

default_remote_conn_timeout = 10
default_remote_workspace_folder = RemotePath("~/.drsync")
default_container_service_name: ContainerServiceName = "docker"


_io_service_store = {}


def set_io_service[T: Service](t: type[T], o: T):
    _io_service_store[t] = o


def get_io_service[T: Service](t: type[T]) -> T:
    return cast(T, _io_service_store[t])
