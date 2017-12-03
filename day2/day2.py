#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 2
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

def checksum(sheet):
    result = 0
    for row in sheet.splitlines():
        vals = [int(item.strip()) for item in row.strip().split()]
        result += max(vals) - min(vals)
    return result

def checksum2(sheet):
    result = 0
    def row_value(items):
        for i, a in enumerate(items[:-1]):
            for b in items[i+1:]:
                if a % b == 0:
                    return a // b
        raise ValueError("No divisible pair found in {}".format(items))                 
    for row in sheet.splitlines():
        vals = sorted([int(item.strip()) for item in row.strip().split()],
                reverse=True)
        result += row_value(vals)
    return result

# PART 1

def example():
    sheet = """ 5 1 9 5
7 5 3
2 4 6 8
"""
    expected = 18
    result = checksum(sheet)
    print("result = {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result = checksum("\n".join(lines))
    print("checksum = {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    sheet = """5 9 2 8
9 4 7 3
3 8 6 5
"""
    expected = 9
    result = checksum2(sheet)
    print("result = {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    result = checksum2("\n".join(lines))
    print("checksum2 = {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
