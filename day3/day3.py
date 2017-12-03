#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 3
#
from math import sqrt

INPUT = 368078

def distance_to_access_port(pos):
    return ring(pos) + axis_offset(pos)

def ring(pos):
    if pos == 1:
        return 0
    return int((sqrt(pos-1) - 1) / 2) + 1

def ring_end(ring):
    return ((2 * ring) + 1) * ((2 * ring) + 1)

def axis_offset(pos):
    r = ring(pos)
    if r == 0:
        return 0
    lastpos = ring_end(r)
    sidelen = 2 * r
    return abs((lastpos - pos) % sidelen - r)

def distance_to_access_port2(start):
    for pos, ring, x, y in coords():
        if pos == start:
            return abs(x) + abs(y)

def values(n):
    prev = dict()
    i = 0
    for pos, ring, x, y in coords():
        if i >= n:
            raise StopIteration
        value = 0
        for xv in (x-1, x, x+1):
            if abs(xv) <= ring:
                for yv in (y-1, y, y+1):
                    if abs(yv) <= ring and (xv, yv) != (x, y):
                        xyval = prev.get((xv, yv), 0)
                        value += xyval

        prev[(x, y)] = value if value else 1
        i += 1
        yield prev[(x, y)]

def coords():
    """A generator that yields the index and xy coords of successive squares in the
    spiral memory store. Tuples (pos, ring, x, y) are yielded.
    """
    pos, x, y = 1, 0, 0
    ring = 0
    end = ring_end(ring)
    while True:
        yield (pos, ring, x, y)
        pos += 1
        if pos > end:
            ring += 1
            end = ring_end(ring)
            x += 1
            dx, dy = 0, 1
        else:
            if abs(x*dx) == ring or abs(y*dy) == ring:
                if (dx, dy) == (0, 1):
                    dx, dy = -1, 0
                elif (dx, dy) == (-1, 0):
                    dx, dy = 0, -1
                elif (dx, dy) == (0, -1):
                    dx, dy = 1, 0
            x, y = x + dx, y + dy

# PART 1

def example():
    cases = [(12, 3),
              (1, 0),
              (23, 2),
              (1024, 31)]
    for start, expected in cases:
        result = distance_to_access_port(start)
        print("Start: {}  distance = {} (expected {})".format(start, result, expected))
        assert result == expected
    print('= ' * 32)

def part1(start):
    dist = distance_to_access_port(start)
    print("Starting at {}, distance to access port is {}".format(start, dist))
    print('= ' * 32)


# PART 2

def example2():
    actual = [1, 1, 2, 4, 5]
    results = [v for v in values(5)]
    for result, expected in zip(results, actual):
        print("value {} (expected {})".format(result, expected))
        assert result == expected
    print('= ' * 32)

def part2(lines):
    for v in values(INPUT):
        if v > INPUT:
            result = v
            break
    print(result)
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT)
    example2()
    part2(INPUT)
