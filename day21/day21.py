#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 21
#
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

START = ['.#.', '..#', '###']

def sample_input():
    return """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""

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

def load_rule(input0, output):
    """Load a single enhancement rule.
    A dict mapping all matching input patterns to the given output
    pattern is returned.
    """
    result = {input0: output}
    pix = input0.split('/')
    if len(pix) == 2:
        for _ in range(3):
            pix = [pix[0][1] + pix[1][1], pix[0][0] + pix[1][0]]
            result["/".join(pix)] = output
            vflip = [pix[1][0] + pix[1][1], pix[0][0] + pix[0][1]]
            result["/".join(vflip)] = output
            hflip = [pix[0][1] + pix[0][0], pix[1][1] + pix[1][0]]
            result["/".join(hflip)] = output
    elif len(pix) == 3:
        for _ in range(3):
            pix = [pix[0][2] + pix[1][2] + pix[2][2],
                   pix[0][1] + pix[1][1] + pix[2][1],
                   pix[0][0] + pix[1][0] + pix[2][0]]
            result["/".join(pix)] = output
            vflip = [pix[2][0] + pix[2][1] + pix[2][2],
                     pix[1][0] + pix[1][1] + pix[1][2],
                     pix[0][0] + pix[0][1] + pix[0][2]]
            result["/".join(vflip)] = output
            hflip = [pix[0][2] + pix[0][1] + pix[0][0],
                     pix[1][2] + pix[1][1] + pix[1][0],
                     pix[2][2] + pix[2][1] + pix[2][0]]
            result["/".join(hflip)] = output
    return result

def load_rulebook(lines):
    """Load a table of enhancement rules.
    A dict mapping the input and output patterns is returned.
    """
    result = dict()
    for line in lines:
        input_pattern, output_pattern = line.split(' => ')
        result.update(load_rule(input_pattern, output_pattern))
    return result

def enhance(pattern, rules):
    """Apply the given rules to the input pattern (a list of strings.)
    The output pattern is returned.
    """
    assert len(pattern) == max([len(row) for row in pattern])
    assert len(pattern) == min([len(row) for row in pattern])
    if len(pattern) % 2 == 0:
        unit = 2
        nunit = len(pattern) // 2
    else:
        unit = 3
        nunit = len(pattern) // 3
    result = []
    for iunit in range(nunit):
        inputs = ["/".join(rows) for rows in zip(
                     *[[pattern[i][junit*unit:(junit+1)*unit]
                         for junit in range(nunit)]
                             for i in range(iunit*unit, (iunit+1)*unit)])]
        outputs = ["".join(segs) for segs in zip(
                      *[rules[pat].split('/') for pat in inputs])]
        result.extend(outputs)
    return result


def solve(lines, n):
    """Apply the rules specified in the input lines to the starting
    pattern for n iterations.
    The number of lit pixels in the final pattern is returned.
    """
    rules = load_rulebook(lines)
    pattern = START
    for _ in range(n):
        pattern = enhance(pattern, rules)
    return sum([row.count('#') for row in pattern])

# PART 1

def example():
    lines = split_nonblank_lines(sample_input())
    expected = 12
    result = solve(lines, 2)
    logger.info("result is {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines, 5)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def part2(lines):
    result = solve(lines, 18)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    part2(input)
