from functools import reduce
from copy import deepcopy


def multi_getitem(iterable, index):
    for i in index:
        iterable = iterable[i]
    return iterable


def multi_setitem(iterable, index, value):
    multi_getitem(iterable, index[:-1])[index[-1]] = value


def multiindex_iadd(iterable, index, value):
    multi_getitem(iterable, index[:-1])[index[-1]] += value


def try_explode(snail):
    stack = []
    last_scalar_index = None
    while True:
        # Look through from left to right
        curr = multi_getitem(snail, stack)
        if hasattr(curr, "__getitem__"):  # Found a pair
            # Explode
            if len(stack) == 4:
                # Explode left
                if last_scalar_index:
                    multiindex_iadd(snail, last_scalar_index, curr[0])
                # Replace pair
                right = curr[1]
                multi_setitem(snail, stack, 0)
                # Explode right
                while stack.pop() == 1:
                    if not stack:  # Reached the end of the snail - don't add to the right
                        return True
                stack.append(1)
                while hasattr(multi_getitem(snail, stack), "__getitem__"):
                    stack.append(0)
                multiindex_iadd(snail, stack, right)
                return True

            stack.append(0)  # Look at the left of the pair first

        else:  # Found a scalar
            last_scalar_index = tuple(stack)  # Found a scalar, so remember it in case we explode
            while stack.pop() == 1:  # Keep going up the number until you find a pair where you previously went left
                if not stack:
                    return False  # End of the snail - explosions to do
            stack.append(1)  # And then go right


def try_split(snail):
    stack = []
    while True:
        curr = multi_getitem(snail, stack)
        if hasattr(curr, "__getitem__"):  # Found a pair
            stack.append(0)  # Go left
        else:
            # Split
            if curr >= 10:
                multi_setitem(snail, stack, [curr//2, curr-curr//2])
                return True

            while stack.pop() == 1:  # Go up until you can go right
                if not stack:
                    return False  # End of the snail - no splits to do
            stack.append(1)  # Go right


def simplify(snail):
    while try_explode(snail) or try_split(snail):
        pass
    return snail


def snail_add(a, b):
    return simplify([a, b])


def magnitude(snail):
    if hasattr(snail, "__getitem__"):
        return magnitude(snail[0]) * 3 + magnitude(snail[1]) * 2
    else:
        return snail


def part_a(inp):
    return magnitude(reduce(snail_add, map(eval, inp)))


def part_b(inp):
    return max(magnitude(snail_add(deepcopy(a), deepcopy(b))) for a in map(eval, inp) for b in map(eval, inp))
