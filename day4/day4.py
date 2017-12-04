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

def normalize_word(word):
    return ''.join(sorted(word))

def is_valid(phrase):
    words = phrase.strip().split()
    uniq = set(words)
    return len(words) == len(uniq)

def is_valid2(phrase):
    words = phrase.strip().split()
    uniq = set([normalize_word(word) for word in words])
    return len(words) == len(uniq)

# PART 1

def example():
    cases = [('aa bb cc dd ee', True),
             ('aa bb cc dd aa', False),
             ('aa bb cc dd aaa', True)]
    for phrase, expected in cases:
        result = is_valid(phrase)
        print("'{}' -> {} (expected {})".format(phrase, result, expected))
        assert result == expected
    print('= ' * 32)

def part1(lines):
    nvalid = 0
    for phrase in lines:
        if is_valid(phrase):
            nvalid += 1
    print("{} input phrases were valid".format(nvalid))
    print('= ' * 32)


# PART 2

def example2():
    cases = [('abcde fghij', True),
             ('abcde xyz ecdab', False),
             ('a ab abc abd abf abj', True),
             ('iiii oiii ooii oooi oooo', True),
             ('oiii ioii iioi iiio', False)]
    for phrase, expected in cases:
        result = is_valid2(phrase)
        print("'{}' -> {} (expected {})".format(phrase, result, expected))
        assert result == expected
    print('= ' * 32)

def part2(lines):
    nvalid = 0
    for phrase in lines:
        if is_valid2(phrase):
            nvalid += 1
    print("{} input phrases were valid".format(nvalid))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
