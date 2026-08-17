import sys
from collections.abc import Callable

import invoke
from fabric import Connection, Result

from drsync.config import default_remote_conn_timeout


def get_remote_conn(host: str, port: int | None):
    return Connection(host=host, port=port, connect_timeout=default_remote_conn_timeout)


def run_cmd_on_remote(cmd: str, conn: Connection):
    try:
        output: Result = conn.run(cmd)
        return output.stdout
    except invoke.exceptions.UnexpectedExit:
        sys.exit(1)


def create_remote_folder(folder: str, rce: Callable[[str], str]):
    return rce(f"mkdir -p {folder}")
