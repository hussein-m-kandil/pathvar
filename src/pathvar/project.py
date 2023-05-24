import os
from argparse import ArgumentParser, Namespace

# TODO: Delete the following constants if there is no need to them
HOME_PATH: str = os.path.normpath(os.path.expanduser('~'))
TEMP_PATH: str = os.path.join(HOME_PATH, "__TEMP_current_path_var__.txt")

FOUND_MSG = "The given path is FOUND in PATH environment variable."
NOT_FOUND_MSG = "The given path is NOT FOUND in PATH environment variable."
BOLD_STYLE = "\033[1m"
UNDERLINE_STYLE = "\033[4m"
RED_STYLE = "\033[91m"
GREEN_STYLE = "\033[92m"
END_STYLE = "\033[0m"


def main() -> None:
    # Place holder for the current path
    current_path_value: str = os.environ["PATH"]

    # Create argument parser
    parser: ArgumentParser = ArgumentParser(
        description="This tool meant to facilitate the interaction \
                with the system's PATH environment variable. \
                    To get the work done correctly do the following: \
                        Read the 'help' instruction well, \n\
                        Be careful about the paths you input (with some options), \n\
                        and Separate between multiple paths with a single ':'. \
                        Copyright (c) 2023 Hussein Mahmoud Kandil - MIT."
    )
    # Add arguments to the ArgumentParser object
    add_args(parser)

    # Parse the arguments and modify the current path
    new_path: str = parse_args_and_modify_path_str(parser, current_path_value)

    # Print the current state
    if new_path == FOUND_MSG or new_path == NOT_FOUND_MSG:
        if new_path == FOUND_MSG:
            print('\n' + BOLD_STYLE + GREEN_STYLE + new_path + END_STYLE)
        else:
            print('\n' + BOLD_STYLE + RED_STYLE + new_path + END_STYLE)
        print_msg("Current 'PATH'", current_path_value)
    elif (current_path_value == new_path):
        print_msg("Current 'PATH'", current_path_value)
    else:
        # TODO: Modify os.environ["PATH"] to hold the new clean value
        ...
        print_msg("Old 'PATH'", current_path_value)
        print_msg("New 'PATH'", new_path)


def add_args(parser_obj: ArgumentParser) -> None:
    """Adding CL arguments to and ArgumentParser object

    Manipulate the inputted ArgumentParser object 
    by adding the needed command line arguments to it
    with all the specifications for each of the arguments
    (i.e. argument name, action, help, ...).

    :param parser_obj: parser object for parsing the command line arguments
    :type parser_obj: argparse.ArgumentParser
    :return: None
    :rtype: None
    """

    # Adding all needed arguments
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
        version="pathvar 1.0.0"
    )


def parse_args_and_modify_path_str(
    parser_obj: ArgumentParser,
    current_path: str
) -> str:
    """Parsing the command line arguments

    Using 'argparse' library this function will consume an 'ArgumentParser' object
    in order to parse the arguments and handle the chosen option/s.

    :param parser_obj: parser object for parsing the command line arguments
    :type parser_obj: argparse.ArgumentParser
    :return: None
    :rtype: None
    """

    # Handle all used arguments
    args: Namespace = parser_obj.parse_args()

    if args.eliminate_duplicates:
        # Change the current path after eliminating any duplicates
        current_path = path_duplicates_eliminator(current_path)

    if args.append:
        # Append the given paths to the current path
        current_path += ':' + args.append.strip().strip(':')

    if args.push:
        # Push the given paths at the beginning of the current path
        current_path = args.push.strip().strip(':') + ':' + current_path

    if args.delete:
        new_path = path_remover(current_path, args.delete)
        if current_path == new_path:
            return NOT_FOUND_MSG
        else:
            current_path = new_path

    if args.query:
        # Return a message to inform the user about whether the given path is in PATH.
        if is_there_path(current_path, args.query):
            return FOUND_MSG
        return NOT_FOUND_MSG

    if args.remove_all_paths:
        print("All paths stored in the PATH environment variable WILL BE DELETED!")
        while True:
            ans: str = input(
                "Are you sure you want to continue [y|n]? "
            )
            if ans.lower() in ('y', 'yes'):
                return ''
            elif ans.lower() in ('n', 'no'):
                break

    # return the current_path with or without any modifications
    return current_path


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
    # Store only the unique paths
    temp_ss: list[str] = []

    for p in ss:
        if p not in temp_ss:
            temp_ss.append(p)

    # Return concatenated string on ':' from the final list
    return ':'.join(temp_ss)


def path_remover(current_path: str, given_paths: str) -> str:
    """Delete the given path/s from the current PATH

    return copy of the 'current_path' 
    without and value included in the 'given_paths'

    :param current_path: The value inside the PATH environment variable
    :type current_path: str
    :param given_paths: The paths that the user want it to be deleted
    :type given_paths: str
    :return: A copy from the current path without any given path
    :rtype: str
    """

    paths_to_remove: list[str] = given_paths.strip().strip(':').split(':')
    paths: list[str] = current_path.split(':')

    for path in paths_to_remove:
        try:
            paths.remove(path)
        except ValueError:
            continue

    return ':'.join(paths)


def is_there_path(current_path: str, given_path: str) -> bool:
    """Check whether the 'given_path' is in 'current_path'

    Return True if the 'given_path' is in 'current_path'
    Otherwise, return false.

    :param current_path: The value inside the PATH environment variable
    :type current_path: str
    :param given_paths: The paths that the user want it to be deleted
    :type given_paths: str
    :return: True/False, based on whether the 'given_path' is in 'current_path'
    :rtype: bool
    """

    for path in current_path.split(':'):
        if given_path == path:
            return True
    return False


def print_msg(title: str, msg: str) -> None:
    """Print message to the user

    This function will print a message to the user
    in form of message title and message body

    :param title: The title of the message
    :type title: str
    :param msg: The body of the message
    :type msg: str
    :return: Nothing, just the print side effect
    :rtype: None
    """
    print()
    print(BOLD_STYLE + title + ': ' + END_STYLE)
    print('_' * 28 + '\n')
    print(msg)
    print()


if __name__ == "__main__":
    main()
