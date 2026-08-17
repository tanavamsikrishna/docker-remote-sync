import subprocess
import sys
from collections.abc import Callable

default_remote_conn_timeout = 10
default_remote_workspace_folder = "~/.drsync"
default_docker_command = "docker"
default_ssh_port = 22


def get_sys_argv() -> list[str]:
    return sys.argv


def get_process_creator() -> Callable[..., subprocess.Popen[str]]:
    return lambda *args, **kwargs: subprocess.Popen(*args, **kwargs)
