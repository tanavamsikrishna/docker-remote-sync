import subprocess
from typing import Literal

from drsync.io_util import print_error


def check_subprocess_errors(error_lines) -> list[str] | None:
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return None
    error_msg = "\n".join(error_lines)
    print_error(error_msg)
    return error_lines


def start_subprocess(
    *args, output: Literal["print", "read"] = "read", text=True
) -> subprocess.Popen:
    return subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE if output == "read" else None,
        stderr=subprocess.PIPE,
        text=text,
    )
