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

def solve(text):
    offsets = [int(line.strip()) for line in text.splitlines() if len(line)]
    pc = 0
    count = 0
    while pc >=0 and pc < len(offsets):
        count += 1
        dst = pc + offsets[pc]
        offsets[pc] += 1
        pc = dst
    return count

def solve2(text):
    offsets = [int(line.strip()) for line in text.splitlines() if len(line)]
    pc = 0
    count = 0
    while pc >=0 and pc < len(offsets):
        count += 1
        dst = pc + offsets[pc]
        if offsets[pc] >= 3:
            offsets[pc] -= 1
        else:
            offsets[pc] += 1
        pc = dst
    return count


# PART 1

def example():
    text = """0
3
0
1
-3"""
    expected = 5
    result = solve(text)
    print("{} steps (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result = solve("\n".join(lines))
    print("{} steps".format(result))
    print('= ' * 32)


# PART 2

def example2():
    text = """0
3
0
1
-3"""
    expected = 10
    result = solve2(text)
    print("{} steps (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    result = solve2("\n".join(lines))
    print("{} steps".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
