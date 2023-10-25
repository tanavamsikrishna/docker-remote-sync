from colorama import Fore, Style


def print_header(msg):
    print(f" > {Fore.BLUE}{Style.BRIGHT}{msg}{Fore.RESET}{Style.RESET_ALL}")
