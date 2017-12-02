#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 1
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

def sum_repeats(text):
    m = len(text)
    return sum([int(text[i]) for i in range(len(text)) if text[i] == text[(i+1)%m]])

def sum_repeats2(text):
    m = len(text)
    step = m // 2
    return sum([int(text[i]) for i in range(len(text)) if text[i] == text[(i+step)%m]])

# Example

def example():
    cases = [('1122', 3),
             ('1111', 4),
             ('1234', 0),
             ('91212129', 9)]
    for text, expected in cases:
        result = sum_repeats(text)
        print("{} -> {} (expected {})".format(text, result, expected))
        assert result == expected

    print('= ' * 32)

# PART 1

def part1(lines):
    print("part 1 result -> ", sum_repeats(lines[0]))
    print('= ' * 32)

# Example 2

def example2():
    cases = [('1212', 6),
             ('1221', 0),
             ('123425', 4),
             ('123123', 12),
             ('12131415', 4)]
    for text, expected in cases:
        result = sum_repeats2(text)
        print("{} -> {} (expected {})".format(text, result, expected))
        assert result == expected

    print('= ' * 32)


# PART 2

def part2(lines):
    print("part 2 result -> ", sum_repeats2(lines[0]))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
