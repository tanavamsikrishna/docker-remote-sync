import sys

from colorama import Fore, Style


def print_header(msg: str):
    print(f" > {Fore.BLUE}{Style.BRIGHT}{msg}{Fore.RESET}{Style.RESET_ALL}")


def print_error(msg: str):
    print(f"{Fore.RED}{msg}{Fore.RESET}", file=sys.stderr)
