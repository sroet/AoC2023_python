import argparse
import time
from collections import namedtuple

Part = namedtuple("Part", ["x", "m", "a", "s"])


def gt(a, b):
    return a > b


def lt(a, b):
    return a < b


def read_file(fname):
    rules = {}
    parts = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "" and strip[0] != "{":
                # rules
                key, val = strip.split("{")
                vals = val[:-1].split(",")
                temp = []
                for v in vals:
                    if ":" in v:
                        eq, dest = v.split(":")
                        if "<" in eq:
                            f = lt
                            left, right = eq.split("<")
                            right = int(right)
                        else:
                            # >
                            f = gt
                            left, right = eq.split(">")
                            right = int(right)
                        temp.append((left, right, f, dest))
                    else:
                        temp.append(v)
                rules[key] = temp
            elif strip != "":
                # parts
                part = strip.strip("{}").split(",")
                temp = {}
                for p in part:
                    key, val = p.split("=")
                    val = int(val)
                    temp[key] = val
                parts.append(Part(**temp))
    return rules, parts


def part_1(data):
    rules, parts = data
    out = 0
    for part in parts:
        current_rule = "in"
        while current_rule not in "AR":
            rule = (i for i in rules[current_rule])
            while True:
                temp = next(rule)
                if isinstance(temp, str):
                    current_rule = temp
                    break
                key, b, func, dest = temp
                if func(getattr(part, key), b):
                    current_rule = dest
                    break
        if current_rule == "A":
            out += sum(part)

    return out


def process_rule(part, key, b, func):
    # returns True/false
    left, right = getattr(part, key)
    if func is gt:
        if left > b:
            # all is true
            return part, None
        if right < b:
            # all is false
            return None, part
        else:
            true = part._replace(**{key: (b + 1, right)})
            false = part._replace(**{key: (left, b)})
            return true, false
    if func is lt:
        if right < b:
            # all is true
            return part, None
        if left > b:
            # all is false
            return None, part
        else:
            true = part._replace(**{key: (left, b - 1)})
            false = part._replace(**{key: (b, right)})
            return true, false


def part_2(data):
    rules, _ = data
    parts = Part((1, 4000), (1, 4000), (1, 4000), (1, 4000))
    queue = [(parts, "in")]
    accepted = set()
    while queue:
        # DFS to manage memory
        part, key = queue.pop()
        if key == "A":
            accepted.add(part)
            continue
        if key == "R":
            continue
        rule = (i for i in rules[key])
        while part is not None:
            temp = next(rule)
            if isinstance(temp, str):
                queue.append((part, temp))
                break
            key, b, func, dest = temp
            true, part = process_rule(part, key, b, func)
            if true is not None:
                queue.append((true, dest))
    out = 0
    for part in accepted:
        temp = 1
        for left, right in part:
            temp *= right - left + 1
        out += temp
    return out


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
