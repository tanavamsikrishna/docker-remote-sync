from drsync.logging_util import print_error


def check_subprocess_errors(error_lines: list[str]):
    error_lines = [el for e in error_lines if len(el := e.rstrip()) > 0]
    if len(error_lines) == 0:
        return
    error_msg = "\n".join(error_lines)
    print_error(error_msg)
