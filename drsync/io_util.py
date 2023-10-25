import sys

from colorama import Fore, Style


def print_header(msg):
    print(f" > {Fore.BLUE}{Style.BRIGHT}{msg}{Fore.RESET}{Style.RESET_ALL}")


def print_error(msg):
    print(f"{Fore.RED}{msg}{Fore.RESET}", file=sys.stderr)
