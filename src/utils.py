"""
Defines small utilities for the module
"""
# pyright: basic
from argparse import Namespace, ArgumentParser
from os import makedirs
from os.path import dirname, exists, abspath
from shutil import rmtree

def liner() -> Namespace:
    """
    Parses the command line input
    ----------
    Returns:
        cmd: Namespace, A namespace object with all possible commands
    """
    prs: ArgumentParser = ArgumentParser(
        prog = '',
        description = '',
        epilog = 'Work in progress'
    )
    py: str = abspath(dirname(__file__)) + '/'
    source: str = abspath(dirname(dirname(__file__))) + '/'
    general = prs.add_argument_group('General', 'Usual script functionalities')
    _ = general.add_argument(
        "-v",
        "--verbose",
        help = "Prints more while running",
        dest='verbose',
        type = str,
    )
    _ = general.add_argument(
        "--version",
        help = """Prints the program version""",
        dest="ver",
        action="version",
        version="%(prog)s 0.1.3",
    )
    _ = general.add_argument(
        "-d",
        "--defaults",
        help = "Prints argument defaults",
        action = 'store_true',
        default=False,
        dest='default',
    )
    _ = general.add_argument(
        "-o",
        "--output",
        help = "Define the folder you want the output in",
        default= source + 'output/',
        dest='output',
        type = str,
    )
    _ = general.add_argument(
        "-clear",
        "--clearFirst",
        help = """Clears the output folders before executing (Note this is deprecated and will remove the output directory multiple times in a run thus it won't work. It was only for testing the building of the project no more than that)""",
        action="store_true",
        default=False,
        dest="clear",
    )
    funcs = prs.add_argument_group('Funcitons', 'Options from this particular script')
    _ = funcs.add_argument(
        "-x",
        help = """The amount of money to populate box 1 (revealed box) with""",
        type = int,
        default = 1000,
        dest="x",
    )
    _ = funcs.add_argument(
        "-y",
        help = """The amount of money to populate box 2 (mystery box) with when box 2 is the only picked box alone""",
        type = int,
        default = 1000000,
        dest="y",
    )
    _ = funcs.add_argument(
        "-z",
        help = """The amount of money to populate box 2 (mystery box) with when box 2 and 1 (revealed box) are picked""",
        type = int,
        default = 0,
        dest="z",
    )
    _ = funcs.add_argument(
        "-p",
        "-people",
        help = """How many unique people to simulate""",
        type = int,
        default = 1,
        dest="people",
    )
    _ = funcs.add_argument(
        "-s",
        "-steps",
        help = """How many simulation steps to take for each person""",
        type = int,
        default = 1000,
        dest="steps",
    )
    cmd: Namespace = prs.parse_args()
    if cmd.default:
        for args, value in vars(cmd).items():
            print(f'{args}: {value}')
        exit('Defaults printed, exiting')
    makedirs(cmd.output, exist_ok=True)
    if cmd.clear:
        if exists(cmd.output):
            confirm: str = input(f'Are you sure you want to remove {cmd.output}? [y/N]')
            if confirm.lower() == 'y':
                rmtree(cmd.output)  # Surely nothing bad will come of this
            else:
                exit('Broke before clearing output for safety')
    return cmd

if __name__ == "__main__":
    cmd: Namespace = liner()
