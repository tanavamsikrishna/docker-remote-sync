import subprocess
from typing import Literal

from drsync.io_util import print_error


def check_subprocess_errors(error_lines: list[str]):
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return
    error_msg = "\n".join(error_lines)
    print_error(error_msg)


def start_subprocess(*args: str, output: Literal["print", "read"] = "read", text: bool):
    completed_process = subprocess.run(
        args=args,
        stdout=subprocess.PIPE if output == "read" else None,
        stderr=subprocess.PIPE,
        text=text,
    )
