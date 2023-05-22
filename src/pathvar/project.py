import os
import argparse
from argparse import ArgumentParser, Namespace

# TODO: Delete the following constants if there is no need to them
HOME_PATH: str = os.path.normpath(os.path.expanduser('~'))
TEMP_PATH: str = os.path.join(HOME_PATH, "__TEMP_current_path_var__.txt")


def main() -> None:
    # Place holder for the current path
    current_path: str = os.environ["PATH"]

    # Create argument parser
    parser: ArgumentParser = ArgumentParser(
        description="Interacting with the system's 'PATH' environment variable."
    )
    # Add arguments to the ArgumentParser object
    add_args(parser)
    # Parse the arguments
    parse_args(parser)

    # Print the current state
    """ print(format_message("Eliminating duplicates...")) """
    # Filter the path variable
    new_path: str = path_duplicates_eliminator(current_path)

    # Print the current state
    """ print(format_message(f"Old: {current_path}",
                         f"New: {new_path}",
                         f"IsAnyDuplicateElimination: {current_path != new_path}")) """

    # TODO: Modify os.environ["PATH"] to hold the new clean value


def add_args(parser_obj: ArgumentParser) -> None:
    parser_obj.add_argument(
        "-s", "--show",
        action="store_true",
        help="shows the current value of the 'PATH' (default)"
    )
    parser_obj.add_argument(
        "-e", "--eliminate-duplicates",
        action="store_true",
        help="eliminates any duplicates in the value of the 'PATH'"
    )
    parser_obj.add_argument(
        "-a", "--append",
        metavar='',
        help="appends any number of paths \
            to the current value of the 'PATH' \
                (which are must be given as a single string separated with ':' \
                    between every two paths and without any spaces)"
    )
    parser_obj.add_argument(
        "-p", "--push",
        metavar='',
        help="pushes any number of paths at the beginning \
            of the current value of 'PATH' \
                (which are must be given as a single string separated with ':' \
                    between every two paths and without any spaces)"
    )
    parser_obj.add_argument(
        "-d", "--delete",
        metavar='',
        help="deletes from 'PATH' any number of paths \
            (which are must be given as a single string separated with ':' \
                between every two paths and without any spaces)"
    )
    parser_obj.add_argument(
        "-q", "--query",
        metavar='',
        help="checks whether the given path is in the current 'PATH'"
    )
    parser_obj.add_argument(
        "--remove-all-paths",
        action="store_true",
        help="removes all paths in the current 'PATH' (NOT RECOMMENDED)"
    )
    parser_obj.add_argument(
        "-v", "--version",
        action="version",
        version="1.0.0"
    )


def parse_args(parser_obj: ArgumentParser) -> None:
    """Parsing the command line arguments

    Using 'argparse' library this function will consume an 'ArgumentParser' object
    in order to parse the arguments and handle the chosen option/s.

    :param parser_obj: parser object for parsing the command line arguments
    :type parser_obj: argparse.ArgumentParser
    :return: None
    :rtype: None
    """
    args: Namespace = parser_obj.parse_args()
    if args.show:
        print(format_message("Command Line Argument => " + str(args.show)))
    if args.eliminate_duplicates:
        print(format_message("Command Line Argument => " +
              str(args.eliminate_duplicates)))
    if args.append:
        print(format_message("Command Line Argument => " +
              str(args.append.split(':'))))
    if args.push:
        print(format_message("Command Line Argument => " + str(args.push.split(':'))))
    if args.delete:
        # TODO: split the string value on ':'
        print(format_message("Command Line Argument => " +
              str(args.delete.split(':'))))
    if args.query:
        print(format_message("Command Line Argument => " + str(args.query)))
    if args.remove_all:
        print(format_message("Command Line Argument => " + str(args.remove_all)))


def path_duplicates_eliminator(s: str) -> str:
    """Remove any duplicates in a PATH variable

    This function removes any duplicated paths from a PATH variable.
    It looks for duplicates in the paths based on the ':' colon separator.

    :param s: The value of the PATH environment variable
    :type s: str
    :return: The same input of the PATH value without any duplicates
    :rtype: str
    """

    # Split on ':'
    ss: list[str] = s.split(':')
    if len(ss) < 2:
        return s

    # Store only the unique paths
    temp_ss: list[str] = []
    for p in ss:
        if p not in temp_ss:
            temp_ss.append(p)

    # Concatenate the string result
    result: str = ""
    for part in temp_ss:
        result += part + ':' if part != temp_ss[-1] else part
    # Return the final result string without duplicates
    return result


def format_message(*strings: str) -> str:
    """Format any number of string objects


    This function format the inputted strings as paragraphs,
    separated by empty lines, ready to be printed.

    :param strings: Any number of string objects
    :type strings: tuple[str]
    :return: A single object has all string inputs
    :rtype: str
    """
    result: str = ""
    for s in strings:
        result += '\n' + s.strip() + '\n'
    return '\n' + result.strip() + '\n'


if __name__ == "__main__":
    main()
