import os

# TODO: Delete the following constants if there is no need to them
HOME_PATH: str = os.path.normpath(os.path.expanduser('~'))
TEMP_PATH: str = os.path.join(HOME_PATH, "__TEMP_current_path_var__.txt")


def main() -> None:

    # Place holder for the current path
    current_path: str = os.environ["PATH"]

    # Print the current state
    print(format_message("echo Eliminating duplicates..."))
    # Filter the path variable
    new_path: str = str_duplicates_elimination(current_path)

    # Print the current state
    print(format_message(f"Old: {current_path}",
                         f"New: {new_path}",
                         f"IsAnyDuplicateElimination: {current_path != new_path}"))

    # TODO: Modify os.environ["PATH"] to hold the new clean value


def str_duplicates_elimination(s: str) -> str:

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


def format_message(*args: str) -> str:
    result: str = ""
    for s in args:
        result += '\n' + s.strip() + '\n'
    return '\n' + result.strip()


if __name__ == "__main__":
    main()
