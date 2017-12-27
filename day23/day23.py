#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 23
#
from collections import namedtuple, defaultdict
from math import sqrt
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

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

ABC = 'abcdefgh'

Value = namedtuple('Value', ['reg', 'val'])

def parse_value(token):
    if token in ABC:
        return Value(reg=token, val=0)
    else:
        return Value(reg="", val=int(token))

class Coprocessor():
    def __init__(self, lines=None, debug=True):
        self.ins = [('nop',)]
        self.size = 0
        self.pc = 1
        self.reg = defaultdict(int)
        if not debug:
            self.reg['a'] = 1
        self.count_mul = 0
        self.trace = set()
        self.trace_count = defaultdict(int)
        if lines:
            self.load_program(lines)

    def set_trace(self, lineno):
        self.trace.add(lineno)

    def __repr__(self):
        return "<Program pc={} reg={}>".format(self.pc, dict(self.reg))

    def load_program(self, lines):
        for line in lines:
            tok = line.strip().split()
            assert len(tok) <= 3
            if tok[0] == 'set':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'sub':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'mul':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'jnz':
                self.ins.append((tok[0], parse_value(tok[1]), parse_value(tok[2])))
        self.size = len(self.ins)
        return self


    def _value(self, obj):
        """Return the integer value represented by the given Value object."""
        if obj.reg:
            return self.reg[obj.reg]
        else:
            return obj.val

    def run(self):
        while self.pc >= 0 and self.pc < self.size:
            if self.pc in self.trace:
                self.trace_count[self.pc] += 1
                logger.info("[{}] ({}): {}".format(self.pc,
                    self.trace_count[self.pc], str(self)))
            self.step()
        return ""

    def step(self):
        try:
            ins = self.ins[self.pc]
            if ins[0] == 'set':
                self.reg[ins[1]] = self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'sub':
                self.reg[ins[1]] -= self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'mul':
                self.count_mul += 1
                self.reg[ins[1]] *= self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'jnz':
                if self._value(ins[1]):
                    self.pc += self._value(ins[2])
                else:
                    self.pc += 1
        except IndexError:
            pass
        return self

# Identify primes

primes = [2, 3, 5, 7, 11, 13]
MAX_PRIME = 150000

def is_prime(n):
    pmax = sqrt(n)
    for p in primes:
        if n % p == 0:
            return False
        elif p > pmax:
            return True

for n in range(17, MAX_PRIME, 2):
    if is_prime(n):
        primes.append(n)

def solve(lines):
    """Solve the problem."""
    prog = Coprocessor(lines)
    prog.run()
    return prog.count_mul

def solve2(lines):
    """Solve the problem."""
    prog = Coprocessor(lines, debug=False)
    prog.set_trace(32)
    prog.set_trace(16)
    prog.set_trace(26)
    prog.run()
    return prog.reg['h']

def solve3(lines):
    """Solve part 2 by counting the number of composite numbers in
    the sequence [108100, 108117, 108134, ..., 125100]

    The 'h' register is incremented every time the value of register 'b'
    (in the main loop) is a not a prime number.  In my input, 'b' assumes
    values [108100, 108117, 108134, ..., 125100]
    """
    h = 0
    for b in range(108100, 125117, 17):
        if not is_prime(b):
            h += 1
    return h
    

# PART 1

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

# PART 2

def part2(lines):
    result = solve3(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    input = load_input(INPUTFILE)
    part1(input)
    part2(input)
