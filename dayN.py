#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day N
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

def solve(arg):
    """Solve the problem."""
    pass

# PART 1

def example():
    cases = [('arg1', 'expected1'),
             ('arg2', 'expected2')]
    for arg, expected in cases:
        result = solve(arg)
        print("'{}' -> {} (expected {})".format(arg, result, expected))
        assert result == expected
    print('= ' * 32)

def part1(lines):
    print('= ' * 32)


# PART 2

def example2():
    print('= ' * 32)

def part2(lines):
    print('= ' * 32)

if __name__ == '__main__':
    example()
    # input = load_input(INPUTFILE)
    # part1(input)
    # example2()
    # part2(input)
