#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 13
#

INPUTFILE = 'input.txt'

def sample_input():
    return ""

# Utility functions

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def split_nonblank_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines

# Solution

def scanner_position(n, t):
    """Return positin of scanner of range n at time t."""
    n1 = n - 1
    return n1 - abs(t % (2*n1) - n1)

def severity(scanners, delay=0):
    """Return the total severity of a passage through a firewall with the
    given set of security scanners, each described by a tuple (depth, range).
    """
    result = 0
    for depth, size in scanners:
        if scanner_position(size, depth + delay) == 0:
            result += depth * size
    return result

def caught(scanners, delay=0):
    """Return True if the packet delayed by the given interval would
    be caught by a firewall with the given set of security scanners,
    each described by a tuple (depth, range).
    """
    result = 0
    for depth, size in scanners:
        if scanner_position(size, depth + delay) == 0:
            return True
    return False

def solve(lines):
    scanners = []
    for line in lines:
        depth, size = [int(v.strip()) for v in line.split(':')]
        scanners.append((depth, size))
    return severity(scanners)

def solve2(lines):
    scanners = []
    for line in lines:
        depth, size = [int(v.strip()) for v in line.split(':')]
        scanners.append((depth, size))
    delay = 0
    while caught(scanners, delay):
        delay += 1
    return delay

# PART 1

def example():
    text = """
0: 3
1: 2
4: 4
6: 4
"""
    lines = split_nonblank_lines(text)
    expected = 24
    result = solve(lines)
    print("result is {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result = solve(lines)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    text = """
0: 3
1: 2
4: 4
6: 4
"""
    lines = split_nonblank_lines(text)
    expected = 10
    result = solve2(lines)
    print("result is {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    result = solve2(lines)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
