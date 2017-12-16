#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 15
#
import time

GENA_START = 516
GENA_FACTOR = 16807
GENA_MASK = 0x3

GENB_START = 190
GENB_FACTOR = 48271
GENB_MASK = 0x7

# Solution

def generator(factor, start, mask=0x0):
    modulus = 2147483647
    value = start
    while True:
        value = (value * factor) % modulus
        if value & mask == 0:
            yield value

def solve(va, vb, n):
    """Solve the problem."""
    gena = generator(GENA_FACTOR, va)
    genb = generator(GENB_FACTOR, vb)
    count = 0
    i = 0
    for va, vb in zip(gena, genb):
        if va & 0xffff == vb & 0xffff:
            count += 1
            # print("[{:6d}]  {:10d}  {:10d}  : {:04x} {:04x}  - {}".format(
            #     i, va, vb, va & 0xffff, vb & 0xffff, count))
        i += 1
        if i == n:
            break
    return count

def solve2(va, vb, n):
    """Solve the problem."""
    gena = generator(GENA_FACTOR, va, GENA_MASK)
    genb = generator(GENB_FACTOR, vb, GENB_MASK)
    count = 0
    i = 0
    for va, vb in zip(gena, genb):
        if va & 0xffff == vb & 0xffff:
            count += 1
            # print("[{:6d}]  {:10d}  {:10d}  : {:04x} {:04x}  - {}".format(
            #     i, va, vb, va & 0xffff, vb & 0xffff, count))
        i += 1
        if i == n:
            break
    return count


# PART 1

def example(): 
    n = 40000000
    start_time = time.time()
    result = solve(65, 8921, n)
    elapsed = time.time() - start_time
    expected = 588
    print("{} pairs -> {} (expected {})".format(n, result, expected))
    print("elapsed time: {} sec".format(elapsed))
    assert result == expected
    print('= ' * 32)

def part1(lines):
    n = 40000000
    result = solve(GENA_START, GENB_START, n)
    print("result is {}".format(result))
    print('= ' * 32)


# PART 2

def example2():
    n = 5000000
    start_time = time.time()
    result = solve2(65, 8921, n)
    elapsed = time.time() - start_time
    expected = 309
    print("{} pairs -> {} (expected {})".format(n, result, expected))
    print("elapsed time: {} sec".format(elapsed))
    assert result == expected
    print('= ' * 32)

def part2(lines):
    n = 5000000
    result = solve2(GENA_START, GENB_START, n)
    print("result is {}".format(result))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(input)
    example2()
    part2(input)
