#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 11
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

class HexPos():
    delta = {'n': (-1, 1, 0),
             'ne': (0, 1, 1),
             'se': (1, 0, 1),
             's': (1, -1, 0),
             'sw': (0, -1, -1),
             'nw': (-1, 0, -1)}

    def __init__(self, a=0, b=0, c=0):
        self.pos = (a, b, c)
        self.furthest = self.dist

    def move(self, *moves):
        for dir in moves:
            self._move(dir)
            if self.dist > self.furthest:
                self.furthest = self.dist
        return self

    def _move(self, dir):
        self.pos = (self.pos[0]+self.delta[dir][0],
                    self.pos[1]+self.delta[dir][1],
                    self.pos[2]+self.delta[dir][2])
        return self

    @property
    def dist(self):
        """Return the number of moves req'd to get to the origin."""
        dx = list(sorted([abs(x) for x in self.pos]))
        return dx[0] + dx[1]



def solve(arg):
    """Solve the problem."""
    pass

# PART 1

def example():
    cases = [('ne,ne,ne', 3),
             ('ne,ne,sw,sw', 0),
             ('ne,ne,s,s', 2),
             ('se,sw,se,sw,sw', 3)]
    for path, expected in cases:
        moves = path.split(',')
        result = HexPos().move(*moves).dist
        print("'{}' -> {} (expected {})".format(path, result, expected))
        assert result == expected
    print('= ' * 32)

def part1(path):
    moves = path.split(',')
    result = HexPos().move(*moves).dist
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    cases = [('ne,ne,ne', 3),
             ('ne,ne,sw,sw', 2),
             ('ne,ne,s,s', 2),
             ('se,sw,se,sw,sw', 3)]
    for path, expected in cases:
        moves = path.split(',')
        result = HexPos().move(*moves).furthest
        print("'{}' -> {} (expected {})".format(path, result, expected))
        assert result == expected
    print('= ' * 32)

def part2(path):
    moves = path.split(',')
    result = HexPos().move(*moves).furthest
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines[0])
    example2()
    part2(lines[0])
