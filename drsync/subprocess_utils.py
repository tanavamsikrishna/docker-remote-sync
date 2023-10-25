import subprocess
import sys
from colorama import Fore


def check_subprocess_errors(error_lines) -> list[str] | None:
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return None
    error_msg = "\n".join(error_lines)
    error_msg = f"{Fore.RED}{error_msg}{Fore.RESET}"
    print(error_msg, file=sys.stderr)
    return error_lines


def start_subprocess(*args):
    return subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
