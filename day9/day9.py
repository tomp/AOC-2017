#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 9
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

BEG_GROUP = '{'
END_GROUP = '}'
BEG_GARBAGE = '<'
END_GARBAGE = '>'
CANCEL = '!'
COMMA = ','

def score_groups(text):
    """Strip all garbage from the input text.
    A string representing the stripped text is returned.
    """
    level = 0       # group nesting level
    score = 0
    garbage_size = 0
    garbage = False # are we currently inside a garbage segment?
    cancel = False  # was the previous character a '!'?
    for ch in text:
        if cancel:
            cancel = False
        elif garbage:
            if ch == END_GARBAGE:
                garbage = False
            elif ch == CANCEL:
                cancel = True
            else:
                garbage_size += 1
        elif ch == BEG_GARBAGE:
            garbage = True
        elif ch == BEG_GROUP:
            level += 1
            score += level
        elif ch == END_GROUP:
            level -= 1
        else:
            assert ch == COMMA
    return score, garbage_size


# PART 1

def example():
    cases = [('<>', 0),
             ('<random characters>', 0),
             ('<<<<>', 0),
             ('<{!>}>', 0),
             ('<!!>', 0),
             ('<!!!>>', 0),
             ('<{o"i!a,<{i<a>', 0),
             ('{}', 1),
             ('{{{}}}', 6),
             ('{{},{}}', 5),
             ('{{{},{},{{}}}}', 16),
             ('{<a>,<a>,<a>,<a>}', 1),
             ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
             ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
             ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3)]
             
    for text, expected in cases:
        result, _ = score_groups(text)
        print("'{}' -> {} (expected {})".format(text, result, expected))
        assert result == expected
    print('= ' * 32)

def part1(lines):
    result = score_groups(lines[0])
    print("result is {})".format(result))
    print('= ' * 32)


# PART 2

def example2():
    cases = [('<>', 0),
             ('<>', 0),
             ('<random characters>', 17),
             ('<<<<>', 3),
             ('<{!>}>', 2),
             ('<!!>', 0),
             ('<!!!>>', 0),
             ('<{o"i!a,<{i<a>', 10)]
             
    for text, expected in cases:
        _, result = score_groups(text)
        print("'{}' -> {} (expected {})".format(text, result, expected))
        assert result == expected
    print('= ' * 32)

def part2(lines):
    _, result = score_groups(lines[0])
    print("result is {})".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
