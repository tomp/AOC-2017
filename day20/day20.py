#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 20
#
import re
from math import sqrt
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

LINE_RE = re.compile(r"p=<(-?\d+),(-?\d+),(-?\d+)>, "
                      "v=<(-?\d+),(-?\d+),(-?\d+)>, "
                      "a=<(-?\d+),(-?\d+),(-?\d+)>")

def sample_input():
    return """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""

def sample_input2():
    return """
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
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

class Coord():
    """A Coord represents a body moving along a single linear coordinate
    under constant acceleration, moving at discrete, fixed-length time steps.
    Positions, velocities, accelerations, and time values are all integers.
    """
    def __init__(self, x0, v0, a):
        self.x0 = x0
        self.v0 = v0
        self.a = a

    def __str__(self):
        return "<Coord {},{},{}>".format(self.x0, self.v0, self.a)

    def __call__(self, t):
        return self.xt(t)

    def xt(self, t):
        """Return the position at time t."""
        return self.x0 + (self.v0 * t) + (self.a * t * (t + 1)/2)

    def vt(self, t):
        """Return the velocity at time t."""
        return self.v0 + t * self.a

    def collision(self, other):
        """Return the future time(s) of collision with the other body,
        as a list of zero, one or two integers.
        If no collision will occur, the empty list is returned.
        """
        da = other.a - self.a
        dv = other.v0 - self.v0
        dx = other.x0 - self.x0
        if da == 0 and dv == 0:
            if dx == 0:
                return [0]
            else:
                return []
        elif da == 0:
            t1 = -dx / dv
            t2 = -1
        else:
            z0 = -(dv/da + 0.5)
            z1 = (dv/da)*(dv/da) + 0.25 + dv/da - 2*dx/da
            if z1 < 0:
                return []
            z1 = sqrt(z1)
            if z0 - z1 > 0.0:
                t1 = z0 - z1
                t2 = z0 + z1
            else:
                t1 = z0 + z1
                t2 = -1
        result = []
        t1 = int(round(t1))
        if t1 >= 0 and self(t1) == other(t1):
            result.append(t1)
        t2 = int(round(t2))
        if t1 >= 0 and self(t2) == other(t2):
            result.append(t2)
        return result

class Particle():
    def __init__(self, line):
        m = LINE_RE.match(line.strip())
        x, y, z, vx, vy, vz, ax, ay, az = [int(v) for v in m.groups()]
        self.xyz = [Coord(x, vx, ax), Coord(y, vy, ay), Coord(z, vz, az)]

    def __str__(self):
        return "<Particle x{}, y{}, z{}>".format(
                self.xyz[0], self.xyz[1], self.xyz[2])

    def __call__(self, t):
        return self.t(t)

    def t(self, t):
        return [c(t) for c in self.xyz]

    def dist(self, t, other=None):
        """Manhattan distance from another particle, or from the origin,
        if no other particle is specified.
        """
        if other:
            return sum([abs(c1(t) - c0(t)) for c0, c1 in zip(self.xyz, other.xyz)])
        else:
            return sum([abs(c(t)) for c in self.xyz])

    def collision(self, other):
        """Return the next collision time of the two particles.
        Return -1 if they don't collide.
        """
        t0 = self.xyz[0].collision(other.xyz[0])
        if not t0:
            return -1
        t1 = self.xyz[1].collision(other.xyz[1])
        if not t1:
            return -1
        t2 = self.xyz[2].collision(other.xyz[2])
        if not t2:
            return -1
        times = list(sorted(list(set(t0 + t1 + t2))))
        result = []
        for t in times:
            if self.dist(t, other) == 0:
                return t
        return -1
        

def solve(lines):
    """Return the index of the particle closest to the origin
    after 1000 steps.
    """
    particles = [Particle(line) for line in lines]
    pt = list(sorted([(p.dist(1000), i) for i, p in enumerate(particles)]))
    return pt[0][1]

def solve2(lines):
    """Return the number of particles that remain after all collisions have
    been resolved.  (We assume that all collisions are independent, which may
    not actually be the case.)
    """
    particles = [Particle(line) for line in lines]
    destroyed = set()
    for i, p1 in enumerate(particles[:-1]):
        for j, p2 in enumerate(particles[i+1:]):
            t = p1.collision(p2)
            if t > -1:
                destroyed.add(i)
                destroyed.add(i+j+1)
                logger.debug("t={}  {} x {}".format(t, i, i+j+1))
    return len(particles) - len(destroyed)

# PART 1

def example():
    lines = split_nonblank_lines(sample_input())
    expected = 0
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
    lines = split_nonblank_lines(sample_input2())
    expected = 1
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
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
