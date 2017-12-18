#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 18
#
from collections import defaultdict, namedtuple

INPUTFILE = 'input.txt'

def sample_input():
    text = """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""
    return split_nonblank_lines(text)

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

ABC = 'abcdefghijklmnopqrstuvwxyz'

Value = namedtuple('Value', ['reg', 'val'])

def parse_value(token):
    if token in ABC:
        return Value(reg=token, val=0)
    else:
        return Value(reg="", val=int(token))

class Program():
    def __init__(self, lines=None):
        self.ins = []
        self.size = 0
        self.pc = 0
        self.reg = defaultdict(int)
        self.sound = 0
        if lines:
            self.load_program(lines)

    def load_program(self, lines):
        for line in lines:
            tok = line.strip().split()
            assert len(tok) <= 3
            if tok[0] == 'snd':
                self.ins.append((tok[0], parse_value(tok[1])))
            elif tok[0] == 'rcv':
                self.ins.append((tok[0], parse_value(tok[1])))
            elif tok[0] == 'set':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'add':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'mul':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'mod':
                self.ins.append((tok[0], tok[1], parse_value(tok[2])))
            elif tok[0] == 'jgz':
                self.ins.append((tok[0], parse_value(tok[1]), parse_value(tok[2])))
        self.size = len(self.ins)
        return self


    def _value(self, obj):
        """Return the integer value represented by the given Value object."""
        if obj.reg:
            return self.reg[obj.reg]
        else:
            return obj.val

    def run(self, recover=False):
        while self.pc >= 0 and self.pc < self.size:
            self.step(recover)

    def step(self, recover=False):
        try:
            ins = self.ins[self.pc]
            if ins[0] == 'snd':
                self.sound = self._value(ins[1])
                self.pc += 1
            elif ins[0] == 'rcv':
                if self._value(ins[1]) and recover:
                    return self.sound
                self.pc += 1
            elif ins[0] == 'set':
                self.reg[ins[1]] = self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'add':
                self.reg[ins[1]] += self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'mul':
                self.reg[ins[1]] *= self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'mod':
                self.reg[ins[1]] = self.reg[ins[1]] % self._value(ins[2])
                self.pc += 1
            elif ins[0] == 'jgz':
                if self._value(ins[1]):
                    self.pc += self._value(ins[2])
        except IndexError:
            return None

def solve(arg):
    """Solve the problem."""
    pass

# PART 1

def example():
    lines = sample_input()
    expected = 4
    prog = Program(lines=lines)
    result = prog.run(True)
    print("recovered sound = {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result = solve(lines)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    print('= ' * 32)

def part2(lines):
    print('= ' * 32)

if __name__ == '__main__':
    example()
    # input = load_input(INPUTFILE)
    # part1(input)
    # example2()
    # part2(input)
