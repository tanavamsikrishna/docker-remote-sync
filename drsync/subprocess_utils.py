import subprocess
import sys


def check_subprocess_errors(error_lines):
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return
    print("\n".join(error_lines), file=sys.stderr)
    sys.exit(1)


def start_subprocess(*args):
    return subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
