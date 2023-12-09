import argparse
import time
from collections import defaultdict
from math import lcm


def read_file(fname):
    instructions = ""
    maps = {}
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                if not instructions:
                    instructions = strip
                    continue
                key, vals = strip.split(" = ")
                vals = vals.strip("()").split(", ")
                maps[key] = vals
    return instructions, maps


def part_1(data):
    steps = 0
    current = "AAA"
    instructions, maps = data
    length = len(instructions)
    if "ZZZ" not in maps:
        # dealing with part 2 example
        return -1
    while current != "ZZZ":
        options = maps[current]
        direction = instructions[steps % length]
        steps += 1
        match direction:
            case "L":
                current = options[0]
            case "R":
                current = options[1]
            case _:
                raise ValueError(f"found {direction=}")
    return steps
    pass


def part_2(data):
    # Assumptions that are true for my input:
    # 1) there is only one end point per start
    # 2) Every endpoint is always reached when the instruction index == 0
    #    (Only true for real input not example)

    instructions, maps = data
    ins_length = len(instructions)
    starts = [i for i in maps.keys() if i[-1] == "A"]
    # {start: (first_occurence, loop_length)}
    loops = {}
    for start in starts:
        steps = 0
        seen = defaultdict(list)
        current = start
        while not ((current, steps % ins_length) in seen and current[-1] == "Z"):
            ins_idx = steps % ins_length
            seen[(current, ins_idx)].append(steps)
            options = maps[current]
            direction = instructions[ins_idx]
            steps += 1
            match direction:
                case "L":
                    current = options[0]
                case "R":
                    current = options[1]
        options = [c for c in seen if c[0][-1] == "Z" and c[1] == (steps % ins_length)]
        assert len(options) == 1
        options = options[0]
        loop_start = seen[options][0]
        loop_length = steps - loop_start
        loops[start] = (loop_start, loop_length)
    current_step = 0
    current_step_size = 1
    for loop_start, loop_length in loops.values():
        while current_step < loop_start:
            current_step += current_step_size
        while (current_step - loop_start) % loop_length != 0:
            # This fails for the example as the loop is nastier than the real input
            # (encounters a Z on alternating instruction indices
            current_step += current_step_size
        current_step_size = lcm(current_step_size, loop_length)
    return current_step
    print(loops)


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
