import sys
from typing import Callable

import invoke
from fabric import Connection, Result


def get_remote_conn(host: str, port: int | None):
    return Connection(host=host, port=port)


def run_cmd_on_remote(cmd: str, conn: Connection):
    try:
        output: Result = conn.run(cmd)
        return output.stdout
    except invoke.exceptions.UnexpectedExit:
        sys.exit(1)


def create_remote_folder(folder: str, rce: Callable[[str], None]):
    return rce(f"mkdir -p {folder}")
