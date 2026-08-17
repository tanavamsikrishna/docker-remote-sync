from typing import cast

from drsync.io_interfaces import Service

default_remote_conn_timeout = 10
default_remote_workspace_folder = "~/.drsync"


_io_service_store = {}


def set_io_service[T: Service](t: type[T], o: T):
    _io_service_store[t] = o


def get_io_service[T: Service](t: type[T]) -> T:
    return cast(T, _io_service_store[t])
