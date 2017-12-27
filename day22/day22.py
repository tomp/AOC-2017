#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 22
#
from collections import defaultdict
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    return """
..#
#..
...
"""

# Constants
UP, DOWN, RIGHT, LEFT = 'up', 'down', 'right', 'left'
CLEAN, INFECTED, FLAGGED, WEAKENED = '', '#', 'F', 'W'

TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
TURN_LEFT  = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
REVERSE  = {UP: DOWN, RIGHT: LEFT, LEFT: RIGHT, DOWN: UP}


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

class Grid():
    def __init__(self, lines):
        self.state = defaultdict(int) # maps (row, col) to 0 (clean) or 1 (infected)
        self.dir = UP
        self.x = 0
        self.y = 0
        self.new_infections = 0
        self._load_lines(lines)

    def __str__(self):
        return "<Grid x,y={},{} dir={} state={}>".format(
                self.x, self.y, self.dir, self.state[self.pos])

    def _load_lines(self, lines):
        size = len(lines)
        assert size % 2 == 1  # initial size must be odd, so there's a center
        lim = (size - 1)//2
        for i, row in enumerate(lines):
            for j, sym in enumerate(row):
                x, y = j - lim, lim - i
                if sym == INFECTED:
                    self.state[(x,y)] = INFECTED
                else:
                    self.state[(x,y)] = CLEAN
                logger.debug("({},{}) {}".format(x, y, self.state[(x,y)]))

    @property
    def pos(self):
        return (self.x, self.y)

    def step(self):
        start = str(self)
        if self.state[self.pos] == INFECTED:
            self.state[self.pos] = CLEAN
            self.dir = TURN_RIGHT[self.dir]
        else:
            self.state[self.pos] = INFECTED
            self.dir = TURN_LEFT[self.dir]
            self.new_infections += 1
        if self.dir == UP:
            self.y += 1
        elif self.dir == LEFT:
            self.x -= 1
        elif self.dir == DOWN:
            self.y -= 1
        elif self.dir == RIGHT:
            self.x += 1
        end = str(self)
        logger.debug("{} --> {}".format(start, end))


class Grid2():
    def __init__(self, lines):
        self.state = defaultdict(str) # maps (row, col) to 0 (clean) or 1 (infected)
        self.dir = UP
        self.x = 0
        self.y = 0
        self.new_infections = 0
        self._load_lines(lines)

    def __str__(self):
        return "<Grid x,y={},{} dir={} state={}>".format(
                self.x, self.y, self.dir, self.state[self.pos])

    def _load_lines(self, lines):
        size = len(lines)
        assert size % 2 == 1  # initial size must be odd, so there's a center
        lim = (size - 1)//2
        for i, row in enumerate(lines):
            for j, sym in enumerate(row):
                x, y = j - lim, lim - i
                if sym == INFECTED:
                    self.state[(x,y)] = INFECTED
                else:
                    self.state[(x,y)] = CLEAN
                logger.debug("({},{}) {}".format(x, y, self.state[(x,y)]))

    @property
    def pos(self):
        return (self.x, self.y)

    def step(self):
        start = str(self)
        if self.state[self.pos] == INFECTED:
            self.state[self.pos] = FLAGGED
            self.dir = TURN_RIGHT[self.dir]
        elif self.state[self.pos] == WEAKENED:
            self.state[self.pos] = INFECTED
            self.new_infections += 1
        elif self.state[self.pos] == CLEAN:
            self.state[self.pos] = WEAKENED
            self.dir = TURN_LEFT[self.dir]
        elif self.state[self.pos] == FLAGGED:
            self.state[self.pos] = CLEAN
            self.dir = REVERSE[self.dir]
        else:
            raise RuntimeError("Unrecognized state: ({},{}) {}".format(
                self.x, self.y, self.state[self.pos]))
        end = str(self)
        logger.debug("{} --> {}".format(start, end))

        if self.dir == UP:
            self.y += 1
        elif self.dir == LEFT:
            self.x -= 1
        elif self.dir == DOWN:
            self.y -= 1
        elif self.dir == RIGHT:
            self.x += 1


def solve(lines, n):
    """Solve the problem."""
    grid = Grid(lines)
    for _ in range(n):
        grid.step()
    return grid.new_infections

def solve2(lines, n):
    """Solve the problem."""
    grid = Grid2(lines)
    for _ in range(n):
        grid.step()
    return grid.new_infections

# PART 1

def example():
    lines = split_nonblank_lines(sample_input())
    cases = [(7, 5), (70, 41), (10000, 5587)]
    for nstep, expected in cases:
        result = solve(lines, nstep)
        logger.info("{} bursts -> {} infections (expected {})".format(nstep, result, expected))
        assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines, 10000)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    lines = split_nonblank_lines(sample_input())
    cases = [(100, 26), (10000000, 2511944)]
    for nstep, expected in cases:
        result = solve2(lines, nstep)
        logger.info("{} bursts -> {} infections (expected {})".format(nstep, result, expected))
        assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines, 10000000)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
