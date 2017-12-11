#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 10
#
from functools import reduce
from operator import xor

INPUTFILE = 'input.txt'

# Utility functions

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

# Solution

class IntKnot():
    def __init__(self, size=256, lengths=None, enhanced=False):
        self.size = size
        self.vals = list(range(size))
        self.pos = 0
        self.skip = 0
        if isinstance(lengths, list):
            self.lengths = lengths
        else:
            self.lengths = {}
        if enhanced:
            self.lengths = self.lengths + [17, 31, 73, 47, 23]

    def cycle(self, repeat=1, lengths=[]):
        if lengths:
            sizes = lengths
        else:
            sizes = self.lengths
        for _ in range(repeat):
            for size in sizes:
                self.make_knot(size)
        return self

    def make_knot(self, knot_size):
        if self.pos + knot_size <= self.size:
            oldvals = list(reversed(self.vals[self.pos:self.pos+knot_size]))
            self.vals[self.pos:self.pos+knot_size] = oldvals
        else:
            size1 = self.size - self.pos
            size2 = knot_size - size1
            oldvals = list(reversed(self.vals[self.pos:] + self.vals[:size2]))
            self.vals[self.pos:] = oldvals[:size1]
            self.vals[:size2] = oldvals[-size2:]
        self.pos = (self.pos + knot_size + self.skip) % self.size
        self.skip += 1
        return self

    def prod(self):
        return self.vals[0] * self.vals[1]

    def dense_hash(self):
        return dense_hash(self.vals)

def dense_hash(vals):
    assert len(vals) == 256
    assert all([v < 256 and v >= 0 for v in vals])
    result = [0] * 16
    for i in range(16):
        result[i] = reduce(xor, vals[i*16:(i+1)*16])
    return "".join(["{:02x}".format(v) for v in result])


# PART 1

def example():
    text = "3,4,1,5"
    sizes = [int(v) for v in text.split(',')]
    expected = 12

    result = IntKnot(5, lengths=sizes).cycle().prod()
    print("'{}' -> {} (expected {})".format(str(sizes), result, expected))
    assert result == expected
    print('= ' * 32)

def part1(line):
    sizes = [int(v) for v in line.split(',')]
    result = IntKnot(lengths=sizes).cycle().prod()
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    cases = [("", 'a2582a3a0e66e6e86e3812dcb672a272'),
             ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
             ('1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
             ('1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e')]

    for text, expected in cases:
        sizes = [ord(ch) for ch in text]
        result = IntKnot(lengths=sizes, enhanced=True).cycle(repeat=64).dense_hash()
        print("'{}' -> {} (expected {})".format(text, result, expected))
        assert result == expected
    print('= ' * 32)

def part2(text):
    sizes = [ord(ch) for ch in text]
    result = IntKnot(lengths=sizes, enhanced=True).cycle(repeat=64).dense_hash()
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines[0])
    example2()
    part2(lines[0])
