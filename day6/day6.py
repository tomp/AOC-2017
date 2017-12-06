#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 6
#

INPUTFILE = 'input.txt'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def redistribute(banks):
    """Redistribute the blocks from the memory bank with the most blocks,
    as described in the spec.

    The input list is modified in-place.
    """
    nblock, ifrom = max(sorted([(nblock, -i) for i, nblock in enumerate(banks)]))
    ifrom = -ifrom
    # print("Distribute the {} blocks from bank {}".format(nblock, ifrom))
    banks[ifrom] = 0
    nbank = len(banks)
    ndist = nblock // nbank
    if nblock % nbank:
        ndist += 1
    # print("...move {} blocks to each other bank".format(ndist))
    for i in range(nbank):
        ito = (ifrom + i + 1) % nbank
        if ndist > nblock:
            ndist = nblock
        banks[ito] += ndist
        nblock -= ndist

def recurrence_count(text):
    banks = [int(v) for v in text.strip().split()]
    seen = dict()
    count = 0
    while not tuple(banks) in seen:
        # print("{}: [{}]".format(count, " ".join([str(v) for v in banks])))
        seen[tuple(banks)] = count
        redistribute(banks)
        count += 1
    return count, count - seen[tuple(banks)]

# PART 1

def example():
    text = "0 2 7 0"
    expected = 5
    result, _ = recurrence_count(text)
    print("Found previously visited state after {} cycles. (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    count, cycle = recurrence_count(lines[0])
    print("Found previously visited state after {} cycles.".format(count))
    print('= ' * 32)


# PART 2

def example2():
    text = "0 2 7 0"
    expected = 4
    _, result = recurrence_count(text)
    print("Found previously visited state after {} cycles. (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    count, cycle = recurrence_count(lines[0])
    print("Cycle length is {}.".format(cycle))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
