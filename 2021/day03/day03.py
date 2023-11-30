def most_common_bit(nums, index):
    return int(sum(num & 1 << index for num in nums) << 1 >= len(nums) << index)


def part_a(inp):
    row_length = len(inp[0])
    gamma = sum((sum(int(row[i]) for row in inp) << 1 >= len(inp)) << (row_length-i-1) for i in range(row_length))
    epsilon = gamma ^ ((1 << row_length) - 1)
    return gamma * epsilon


def part_b(inp):
    row_length = len(inp[0])
    nums = set(map(lambda x: int(x, 2), inp))
    for index in range(row_length-1, -1, -1):
        bit = most_common_bit(nums, index)
        nums = set(filter(lambda num: num & 1 << index == bit << index, nums))
        if len(nums) == 1:
            oxygen ,= nums

    nums = set(map(lambda x: int(x, 2), inp))
    for index in range(row_length - 1, -1, -1):
        bit = most_common_bit(nums, index)
        nums = set(filter(lambda num: num & 1 << index != bit << index, nums))
        if len(nums) == 1:
            scrubber, = nums
    return oxygen * scrubber
