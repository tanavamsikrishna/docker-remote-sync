import subprocess

from drsync.io_util import print_error


def check_subprocess_errors(error_lines) -> list[str] | None:
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return None
    error_msg = "\n".join(error_lines)
    print_error(error_msg)
    return error_lines


def start_subprocess(*args):
    return subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
