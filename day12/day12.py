#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 12
#
import re

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

# LINE_RE = re.compile(r"

def parse_network(lines):
    """Return a dict mapping each ID to a list of the IDs it can
    communicate with directly.
    """
    neighbors = dict()
    for line in lines:
        node, conn, others = line.split(maxsplit=2)
        assert conn == '<->'
        neighbors[int(node)] = [int(v.strip()) for v in others.split(',')]
    return neighbors

def count_connected_nodes(neighbors, start):
    """Return the number of nodes in the group to which the
    given node belongs.
    """
    group = find_group(neighbors, start)
    return len(group)

def find_group(neighbors, start):
    """Return a set containing the members of the group to which the
    given node belongs.
    """
    found = set([start])
    queue = [start]
    while queue:
        node = queue.pop(0)
        found.add(node)
        for other in neighbors[node]:
            if not other in found:
                queue.append(other)
    return found

def count_groups(neighbors):
    """Return the number of connected groups found in the network."""
    groups = []
    found = set()
    for node in neighbors:
        if not node in found:
            group = find_group(neighbors, node)
            groups.append(group)
            found.update(group)
    return len(groups)

def solve(lines):
    """Solve the problem."""
    neighbors = parse_network(lines)
    return count_connected_nodes(neighbors, 0)

def solve2(lines):
    """Solve the problem."""
    neighbors = parse_network(lines)
    return count_groups(neighbors)

# PART 1

def example():
    text = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    lines = split_nonblank_lines(text)
    expected = 6
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
    text = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    lines = split_nonblank_lines(text)
    expected = 2
    result = solve2(lines)
    print("found {} groups (expected {})".format(result, expected))
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
