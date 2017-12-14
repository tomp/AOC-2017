#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 14
#
from functools import reduce
from operator import xor

INPUT = 'wenycdww'

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
    result = solve(lines)
    print("result is {}".format(result))
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
