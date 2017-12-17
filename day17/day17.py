#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 17
#

INPUT = 304

# Solution

class Buffer():
    def __init__(self, step):
        self.buffer = ['0']
        self.size = 1
        self.step = step
        self.pos = 0

    def __str__(self):
        return " ".join([' '+v+' ' if i != self.pos else '('+v+')'
                         for i, v in enumerate(self.buffer)])

    def __repr__(self):
        return str(self)

    def insert(self, value):
        nextpos = (self.pos + self.step) % self.size + 1
        self.buffer = self.buffer[:nextpos] + [str(value)] + self.buffer[nextpos:]
        self.pos = nextpos
        self.size += 1
        return self

    def fake_insert(self, value):
        nextpos = (self.pos + self.step) % self.size + 1
        self.pos = nextpos
        self.size += 1
        return self

def solve(arg):
    """Solve the problem."""
    b = Buffer(arg)
    for i in range(2017):
        b.insert(i+1)
    return b.buffer[b.pos + 1]

def solve2(arg):
    """Solve the problem."""
    result = None
    b = Buffer(arg)
    for i in range(50000000):
        b.fake_insert(i+1)
        if b.pos == 1:
            result = i + 1
    return result

# PART 1

def example():
    step = 3
    expected = '638'
    result = solve(step)
    print("'{}' -> {} (expected {})".format(step, result, expected))
    assert result == expected
    print('= ' * 32)

def part1(value):
    result = solve(value)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def part2(value):
    result = solve2(value)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT)
    part2(INPUT)
