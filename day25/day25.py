#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 25
#
from collections import namedtuple, defaultdict
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'

def sample_input():
    return """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

# Solution

LEFT, RIGHT = -1, 1
ZERO, ONE = 0, 1

Move = namedtuple('Move', ['write', 'dir', 'next'])
State = namedtuple('State', ['zero', 'one'])

SAMPLE_MACHINE = {
        'A': State(zero=Move(1, RIGHT, 'B'),
                    one=Move(0, LEFT, 'B')),
        'B': State(zero=Move(1, LEFT, 'A'),
                    one=Move(1, RIGHT, 'A'))}

MACHINE = {
        'A': State(zero=Move(1, RIGHT, 'B'),
                    one=Move(0, LEFT,  'D')),
        'B': State(zero=Move(1, RIGHT, 'C'),
                    one=Move(0, RIGHT, 'F')),
        'C': State(zero=Move(1, LEFT,  'C'),
                    one=Move(1, LEFT,  'A')),
        'D': State(zero=Move(0, LEFT,  'E'),
                    one=Move(1, RIGHT, 'A')),
        'E': State(zero=Move(1, LEFT,  'A'),
                    one=Move(0, RIGHT, 'B')),
        'F': State(zero=Move(0, RIGHT, 'C'),
                    one=Move(0, RIGHT, 'E')),
        }

NSTEP = 12302209

class Tape():
    """A Tape is the state of a Turing machine's data store."""
    def __init__(self):
        self.val = defaultdict(int)
        self.cursor = 0

    def squares(self):
        ilow = min(self.val.keys())
        imax = max(self.val.keys())
        return [(i, self.val[i]) for i in range(ilow, imax+1)]

    @property
    def checksum(self):
        return sum(self.val.values())

    def __repr__(self):
        return "".join([" {} ".format(v) if i != self.cursor else "[{}]".format(v)
            for i, v in self.squares()])

    def step(self, state):
        if self.val[self.cursor] == 0:
            return self.execute(state.zero)
        else:
            return self.execute(state.one)

    def execute(self, move):
        self.val[self.cursor] = move.write
        self.cursor += move.dir
        return move.next

    def run(self, machine, init='A', nstep=1):
        assert init in machine
        steps = 0
        state = init
        logger.debug(self)
        while steps < nstep:
            steps += 1
            state = self.step(machine[state])
            # logger.debug("{}: '{}' @{} {}".format(steps, state, self.cursor, self))
        

def solve(machine, nstep):
    """Solve the problem."""
    t = Tape()
    t.run(machine, 'A', nstep)
    return t.checksum

# PART 1

def example():
    machine = SAMPLE_MACHINE
    nstep = 6
    expected = 3
    result = solve(machine, nstep)
    logger.info("After {} steps, checksum -> {} (expected {})".format(
        nstep, result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1():
    result = solve(MACHINE, NSTEP)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


if __name__ == '__main__':
    example()
    part1()
