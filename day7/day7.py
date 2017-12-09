#!/usr/bin/env python3
#
#  Advent of Code 2017 - Day 7
#
import re

INPUTFILE = 'input.txt'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

LINE_RE = re.compile(r"([a-z]+) \((\d+)\)(?: -> ([a-z].*[a-z]))?")


class Tree():
    def __init__(self, name, weight, child_names):
        self.name = name
        self.weight = weight
        self._total_weight = 0
        self.child_names = child_names
        self.children = []

    def add_children(self, nodes):
        for name in self.child_names:
            child = nodes.pop(name)
            child.add_children(nodes)
            self.children.append(child)

    @property
    def total_weight(self):
        if self._total_weight == 0:
            self._total_weight = self.weight
            for child in self.children:
                self._total_weight += child.total_weight
        return self._total_weight

    def rebalance(self, expected_weight=0):
        if not self.children:
            if expected_weight:
                return self.name, expected_weight
        odd_weight, common_weight = odd_value([c.total_weight for c in self.children])
        if not odd_weight:
            if expected_weight:
                return self.name, expected_weight - self.total_weight + self.weight
        odd_child = [c for c in self.children if c.total_weight == odd_weight][0]
        return odd_child.rebalance(common_weight)


def odd_value(vals):
    if len(vals) < 3:
        return None
    v1, v2 = min(vals), max(vals)
    if v1 == v2:
        return None, v1
    c1, c2 = vals.count(v1), vals.count(v2)
    if c1 == 1:
        return v1, v2
    else:
        return v2, v1

def parse_input(text):
    lines = [line.strip() for line in text.splitlines() if line]
    table = dict()
    for line in lines:
        m = LINE_RE.match(line)
        if m:
            disc, weight, supp = m.groups()
            if supp:
                children = supp.split(', ')
            else:
                children = list()
            table[disc] = (int(weight), children)
    return table

def construct_tree(text):
    """Construct the tree of discs.
    A tuple (top, nodes) is returned, where top is the name of the top
    disc, and nodes is a dict mapping disc names to their Tree objects.
    """
    table = parse_input(text)
    nodes = dict()
    child_nodes = set()
    parent_nodes = set()
    top = set()
    for disc, v in table.items():
        weight, children = v
        assert not disc in nodes
        nodes[disc] = Tree(disc, weight, children)
        if children:
            parent_nodes.add(disc)
            for child in children:
                child_nodes.add(child)
    top_nodes = parent_nodes.difference(child_nodes)
    assert len(top_nodes) == 1
    top = list(top_nodes)[0]
    tree = nodes[top]
    tree.add_children(nodes)
    return tree


# PART 1

def example():
    sample = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""
    expected = "tknk"
    tree = construct_tree(sample)
    print("top node is {} (expected {})".format(tree.name, expected))
    assert tree.name == expected
    print('= ' * 32)

def part1(lines):
    text = "\n".join(lines)
    tree = construct_tree(text)
    print("top node is {}".format(tree.name))
    print('= ' * 32)


# PART 2

def example2():
    sample = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""
    expected = 60
    tree = construct_tree(sample)
    node, weight = tree.rebalance()
    print("To balance tree, node {} weight should be {} (expected {})".format(
        node, weight, expected))
    assert weight == expected
    print('= ' * 32)

def part2(lines):
    text = "\n".join(lines)
    tree = construct_tree(text)
    node, weight = tree.rebalance()
    print("To balance tree, node {} weight should be {}".format(node, weight))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)
