#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 18
#
from collections import defaultdict, namedtuple
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'


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

class SoundProgram():
    def __init__(self, lines=None):
        self.ins = []
        self.size = 0
        self.recover = 0
        self.pc = 0
        self.reg = defaultdict(int)
        self.sound = 0
        if lines:
            self.load_program(lines)

    def __repr__(self):
        return "<Program pc={}/{} sound={}>".format(self.pc, self.size,
                self.sound)

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
            if self.recover:
                return self.recover
        return ""


    def step(self, recover=False):
        try:
            ins = self.ins[self.pc]
            if ins[0] == 'snd':
                self.sound = self._value(ins[1])
                self.pc += 1
            elif ins[0] == 'rcv':
                if self._value(ins[1]) and recover:
                    self.recover = self.sound
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
                else:
                    self.pc += 1
        except IndexError:
            pass
        return self

class DuetProgram():
    def __init__(self, id, sendq, recvq, lines=None):
        self.id = id
        self.reg = defaultdict(int)
        self.reg['p'] = id
        self.sendq = sendq
        self.recvq = recvq
        self.blocked = False
        self.sent = 0
        self.done = False
        self.ins = []
        self.size = 0
        self.pc = 0
        if lines:
            self.load_program(lines)

    def __repr__(self):
        return "prog{} @{} done={} block={} sent={} q={} reg={}>".format(self.id,
                self.pc, self.size, int(self.done), int(self.blocked),
                self.sent, len(self.recvq), str(dict(self.reg.items())))

    def load_program(self, lines):
        for line in lines:
            tok = line.strip().split()
            assert len(tok) <= 3
            if tok[0] == 'snd':
                self.ins.append((tok[0], parse_value(tok[1])))
            elif tok[0] == 'rcv':
                self.ins.append((tok[0], tok[1]))
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

    def run(self):
        while not self.done:
            self.step()

    def step(self):
        try:
            ins = self.ins[self.pc]
            if ins[0] == 'snd':
                self.sendq.append(self._value(ins[1]))
                self.sent += 1
                self.pc += 1
                logger.debug("prog{} @{} --> {}".format(self.id,
                    self.pc, self._value(ins[1])))
            elif ins[0] == 'rcv':
                if self.recvq:
                    self.reg[ins[1]] = self.recvq.pop(0)
                    logger.debug("prog{} @{} <-- {}".format(self.id,
                        self.pc, self.reg[ins[1]]))
                    self.pc += 1
                    self.blocked = False
                else:
                    self.blocked = True
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
                logger.debug(str(self))
                if self._value(ins[1]) > 0:
                    self.pc += self._value(ins[2])
                else:
                    self.pc += 1
        except IndexError:
            self.done = True
        return self

def run_duet(lines):
    q1 = list()
    q2 = list()
    prog0 = DuetProgram(0, q2, q1, lines=lines)
    prog1 = DuetProgram(1, q1, q2, lines=lines)

    while not ((prog0.done or prog0.blocked) and
               (prog1.done or prog1.blocked)):
        prog0.step()
        prog1.step()

    return prog1.sent

# PART 1

def example():
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
    lines = split_nonblank_lines(text)
    expected = 4
    prog = SoundProgram(lines=lines)
    result = prog.run(True)
    logger.info("recovered sound = {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    prog = SoundProgram(lines=lines)
    result = prog.run(True)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def example2():
    text = """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""
    lines = split_nonblank_lines(text)
    expected = 3
    result = run_duet(lines)
    logger.info("prog1 sent {} msgs (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = run_duet(lines)
    logger.info("prog1 sent {} msgs".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    example2()
    part2(lines)
