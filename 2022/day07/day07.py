import re
from typing import Any, Callable

REPORT_LIMIT = 100_000
CAN_UPDATE_LIMIT = 40_000_000


def scan_dir(log: list[str]) -> dict:
    """
    Look through a list of cd and ls commands and infer the structure of the directories visited.
    :param log: The cd and ls commands and responses thereto.
    :return: Nested dictionaries. Each key is the name of a file or directory. Each directory is represented by a
    dictionary and each file is represented by its size.
    """
    curr_path = ["/"]
    directories = {}
    for line in log:
        if line.startswith("$ cd "):
            next_path = line[5:]
            if next_path == "..":
                curr_path.pop()
            elif next_path == "/":
                curr_path = ["/"]
            else:
                curr_path.append(next_path)
        else:
            m = re.match(r'(\d+) ([\w.]+)', line)
            if not m:
                continue
            # Add the file to the directories
            directory = directories
            for element in curr_path:
                if element not in directory:
                    directory[element] = {}
                directory = directory[element]
            directory[m.group(2)] = int(m.group(1))

    return directories


def get_sizes(root: dict, size_callback: Callable[[int], Any] | None = None) -> int:
    """
    Search through a directory and find the total size of it and of each directory within.
    :param root: The top-level directory for the search.
    :param size_callback: A function to call each time a size is found. Takes the size as its argument.
    :return: The total size of the root directory.
    """

    while True:
        # Get a directory containing no directories
        directory = root
        # Keep track of where we came from so we can replace the current directory later
        last_dir, key_in_last_dir = None, None
        while True:
            for key, value in directory.items():
                if isinstance(value, dict):
                    # Delve deeper
                    last_dir, key_in_last_dir = directory, key
                    directory = value
                    break
            else:
                # This directory contains no directories
                # Replace it with the sum of its component sizes
                size = sum(directory.values())
                if size_callback is not None:
                    size_callback(size)
                if last_dir is not None:
                    last_dir[key_in_last_dir] = size

                break

        if last_dir is None:
            # We have reached the root directory
            break

    return root["/"]


def part_a(inp):
    total = 0

    def size_callback(size):
        nonlocal total
        if size <= REPORT_LIMIT:
            total += size

    get_sizes(scan_dir(inp), size_callback)
    return total


def part_b(inp):
    root = scan_dir(inp)
    # Find the amount we need to delete, based on the total size
    can_delete_threshold = get_sizes(root) - CAN_UPDATE_LIMIT
    min_size = 7e7

    def size_callback(size):
        nonlocal min_size
        if can_delete_threshold <= size < min_size:
            min_size = size

    get_sizes(root, size_callback)
    return min_size
