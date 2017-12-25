#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 19
#
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    return """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""


# Utility functions

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip("\n")
            if line:
                lines.append(line)
        return lines

def split_nonblank_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip("\n")
        if line:
            lines.append(line)
    return lines

# Solution

VERT = "|"
HORZ = "-"
ECKE = "+"
BLANK = " "
UP, DOWN, RIGHT, LEFT = "up", "down", "right", "left"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def trace_route(rows):
    """Trace the diagrammed route, starting from the entry port on the
    first line.  Return a list of the labelled nodes encountered.
    """
    nrow = len(rows)
    ncols= [len(row) for row in rows]
    assert min(ncols) == max(ncols)
    ncol = min(ncols)

    r = 0
    c = rows[r].index(VERT)
    d = DOWN
    logger.debug("[{},{}] {} heading {}".format(r, c, rows[r][c], d))

    steps = 1
    found = []
    while True:
        steps += 1
        if d == UP:
            r -= 1
        elif d == DOWN:
            r += 1
        elif d == RIGHT:
            c += 1
        elif d == LEFT:
            c -= 1
        sym = rows[r][c]
        logger.debug("[{},{}] {} heading {}".format(r, c, sym, d))
        if sym == ECKE:
            lastd = d
            if d == UP or d == DOWN:
                if c >= 0:
                    if rows[r][c-1] == HORZ or rows[r][c-1] in LETTERS:
                        d = LEFT
                if c < ncol-1:
                    if rows[r][c+1] == HORZ or rows[r][c+1] in LETTERS:
                        d = RIGHT
            elif d == RIGHT or d == LEFT:
                if r >= 0:
                    if rows[r-1][c] == VERT or rows[r-1][c] in LETTERS:
                        d = UP
                if r < nrow-1:
                    if rows[r+1][c] == VERT or rows[r+1][c] in LETTERS:
                        d = DOWN
            if d == lastd:
                raise ValueError("Stuck at [{},{}] heading {}".format(r, c, d))
        elif sym in LETTERS:
            found.append(sym)
            if d == UP and (r == 0 or rows[r-1][c] == BLANK):
                break
            elif d == DOWN and (r == nrow-1 or rows[r+1][c] == BLANK):
                break
            elif d == RIGHT and (c == ncol-1 or rows[r][c+1] == BLANK):
                break
            elif d == LEFT and (c == 0 or rows[r][c-1] == BLANK):
                break
    return steps, found


def solve(lines):
    """Solve the problem."""
    steps, found = trace_route(lines)
    return "".join(found)

def solve2(lines):
    """Solve the problem."""
    steps, found = trace_route(lines)
    return steps

# PART 1

def example():
    lines = split_nonblank_lines(sample_input())
    expected = "ABCDEF"
    result = solve(lines)
    logger.info("found {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    lines = split_nonblank_lines(sample_input())
    expected = 38
    result = solve2(lines)
    logger.info("{} steps (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines)
    logger.info("{} steps".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
