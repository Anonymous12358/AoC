def part_a(inp):
    # Split lines by default
    return inp


def part_b(inp):
    """raw"""
    # Disable splitting lines
    return inp


def part_c(inp):
    r"""
    /(\w+) (\w+)/
    """
    # Match regex and extract groups
    return inp


def part_d(inp):
    r"""
    /(\w+): (\d+)-(\d+)/
    str int int
    """
    # Cast groups to types
    return inp


def part_e(inp):
    """
    split " "
    int
    """
    # Split on any substring; types to cast are cycled so you can cast any number of components
    return inp


def part_f(inp):
    r"""
    /(\w) (\w)/
    int int
    ABC XYZ
    """
    # Palettes for casting to integer types: A means 0, B means 1, etc
    # Palettes can be defined per-component and are cycled
    return inp


def part_g(inp):
    """array
    split
    bool
    .#
    """
    # Cast whole input to numpy array
    return inp


def part_h(inp):
    """quick array"""
    # Equivalent to part g, for the default way AoC does grids
    return inp
