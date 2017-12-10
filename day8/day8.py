#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 8
#
import re
import operator
from collections import defaultdict

INSTRUCTION_RE = re.compile(r"^([a-z]+) (inc|dec) (-?[0-9]+) if ([a-z]+) (\S+) (-?[0-9]+)")

INPUTFILE = 'input.txt'

COMP = {'==': operator.eq,
        '!=': operator.ne,
        '>':  operator.gt,
        '>=': operator.ge,
        '<':  operator.lt,
        '<=': operator.le}

INC = 'inc'
DEC = 'dec'

def sample_input():
    return split_nonblank_lines("""
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""")

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

def run_program(lines):
    """Parse  and execute the given program.
    A tuple is returned, of the maximum value in any register at the
    end of the computation, and the maximum value found at any point
    during the calculation.
    """
    reg = defaultdict(int)
    max_reg = 0
    for line in lines:
        m = INSTRUCTION_RE.match(line)
        if not m:
            raise ValueError("Unparseable instruction: '{}'".format(line))
        op_reg, op, v1, cond_reg, comp, v2 = m.groups()
        if COMP[comp](reg[cond_reg], int(v2)):
            if op == INC:
                reg[op_reg] += int(v1)
            elif op == DEC:
                reg[op_reg] -= int(v1)
            if reg[op_reg] > max_reg:
                max_reg = reg[op_reg]
    return max(reg.values()), max_reg
        

# PART 1

def example():
    lines = sample_input()
    expected = 1
    result, _ = run_program(lines)
    print("max reg value at end is {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    result, _ = run_program(lines)
    print("max reg value at end is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    lines = sample_input()
    expected = 10
    _, result = run_program(lines)
    print("max reg value at any time is {} (expected {})".format(result, expected))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    _, result = run_program(lines)
    print("max reg value at any time is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
