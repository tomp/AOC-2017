#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day N
#
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    return """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
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

class Component():
    """A bridge unit, characterized its two port sizes.
    This class is conceptually immutable.
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.strength = a + b
        self.tuple = (a, b)

    def __repr__(self):
        return "{}/{}".format(self.a, self.b)

    def __hash__(self):
        return hash(self.tuple)

    def has_port(self, port):
        return self.a == port or self.b == port

class Bridge():
    """A Bridge represents an immutable sequence of connected components.
    bridge ... a list of port numbers, starting with zero, and ending with
               the final, unattached port.
    avail .... the list of unused components
    """
    def __init__(self, bridge=None, comps=[]):
        if bridge:
            self.bridge = bridge
        else:
            self.bridge = [0]
        self.avail = comps
        self.strength = sum(self.bridge)
        self.length = len(self.bridge)

    def __repr__(self):
        return "<Bridge [{}] {}:{}>".format(self.strength, self.length,
                   "-".join([str(v) for v in self.bridge]))

    @property
    def port(self):
        return self.bridge[-1]

    def add_component(self, comp, rest):
        """Returns a new Bridge represented the current bridge after adding
        given component. The 'rest' is the list a remaining available
        components.
        """
        if comp.a == self.port:
            return Bridge(self.bridge + [comp.a, comp.b], rest)
        else:
            return Bridge(self.bridge + [comp.b, comp.a], rest)

    def extensions(self):
        for i, c in enumerate(self.avail):
            if c.has_port(self.port):
                yield self.add_component(c, self.avail[:i]+self.avail[i+1:])

def load_components(lines):
    result = []
    for line in lines:
        result.append(Component(*[int(v) for v in line.split('/')]))
    assert len(result) == len(set(result))
    return result

def strongest_bridge(comps):
    start = Bridge(comps=comps)
    strongest = start
    q = [start]
    while q:
        b = q.pop(0)
        if b.strength > strongest.strength:
            strongest = b
            logger.debug(b)
        for bn in b.extensions():
            q.append(bn)
    return strongest

def longest_bridge(comps):
    start = Bridge(comps=comps)
    longest = [start]
    length = start.length
    q = [start]
    while q:
        b = q.pop(0)
        if b.length > length:
            longest = [b]
            length = b.length
            logger.debug(b)
        elif b.length == length:
            longest.append(b)
            logger.debug(b)
        for bn in b.extensions():
            q.append(bn)
    strongest = max([b.strength for b in longest])
    return [b for b in longest if b.strength == strongest][0]

def solve(lines):
    """Solve the problem."""
    comp = load_components(lines)
    bridge = strongest_bridge(comp)
    return bridge.strength

def solve2(lines):
    """Solve the problem."""
    comp = load_components(lines)
    bridge = longest_bridge(comp)
    return bridge.strength

# PART 1

def example():
    lines = split_nonblank_lines(sample_input())
    expected = 31
    result = solve(lines)
    logger.info("result is {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    lines = split_nonblank_lines(sample_input())
    expected = 19
    result = solve2(lines)
    logger.info("result is {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
