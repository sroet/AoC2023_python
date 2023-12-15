import argparse
import time
from collections import Counter


def read_file(fname):
    rocks = set()
    # needed to print the map if needed
    # global walls
    walls = set()
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    match c:
                        case "#":
                            walls.add(complex(x, y))
                        case "O":
                            rocks.add(complex(x, y))

    return rocks, walls, y, x


directions = {"N": -1j, "W": -1, "S": 1j, "E": 1}


def make_wall_maps(max_x, max_y, walls):
    current_holes = []
    N_map, S_map, E_map, W_map = {}, {}, {}, {}
    # NS first, so per column
    for x in range(max_x + 1):
        current_wall = complex(x, -1)
        for y in range(max_y + 1):
            current_coord = complex(x, y)
            if current_coord in walls:
                next_wall = current_coord
                for i in current_holes:
                    N_map[i] = current_wall
                    S_map[i] = next_wall
                current_holes = []
                current_wall = next_wall
            else:
                current_holes.append(current_coord)
        # deal with final boundary
        if current_holes:
            next_wall = current_coord + 1j
            for i in current_holes:
                N_map[i] = current_wall
                S_map[i] = next_wall
                current_holes = []

    # EW next, so per row
    for y in range(max_y + 1):
        current_wall = complex(-1, y)
        for x in range(max_x + 1):
            current_coord = complex(x, y)
            if current_coord in walls:
                next_wall = current_coord
                for i in current_holes:
                    W_map[i] = current_wall
                    E_map[i] = next_wall
                current_holes = []
                current_wall = next_wall
            else:
                current_holes.append(current_coord)
        # deal with final boundary
        if current_holes:
            next_wall = current_coord + 1
            for i in current_holes:
                W_map[i] = current_wall
                E_map[i] = next_wall
                current_holes = []
    return {"N": N_map, "S": S_map, "E": E_map, "W": W_map}


def print_map(rocks):
    global walls
    for line in range(10):
        out = ""
        for c in range(10):
            if complex(c, line) in walls:
                out += "#"
            elif complex(c, line) in rocks:
                out += "O"
            else:
                out += "."
        print(out)
    print("")


def gen_rocks_iter_from_wall_counter(wall_counter, last_direction="N"):
    complex_dir = -directions[last_direction]
    return (
        key + complex_dir * n
        for key, val in wall_counter.items()
        for n in range(1, val + 1)
    )


def cycle_roll_rocks(rocks, wall_maps, wall_counter=None, part1=False):
    order = "NWSE"
    last_dir = "E"
    if wall_counter is None:
        # Assume first cycle
        wall_map = wall_maps["N"]
        wall_counter = Counter(wall_map[i] for i in rocks)
        if part1:
            return wall_counter
        order = "WSE"
        last_dir = "N"

    for direction in order:
        wall_map = wall_maps[direction]
        itt = gen_rocks_iter_from_wall_counter(wall_counter, last_dir)
        wall_counter = Counter(wall_map[i] for i in itt)
        last_dir = direction

    return wall_counter


def part_1(data):
    rocks, walls, max_y, max_x = data
    wall_maps = make_wall_maps(max_x, max_y, walls)
    wall_counter = cycle_roll_rocks(rocks, wall_maps, part1=True)
    new_rocks = gen_rocks_iter_from_wall_counter(wall_counter, "N")
    out = sum(max_y + 1 - rock.imag for rock in new_rocks)
    return round(out), (rocks, wall_maps, max_y)


def part_2(data):
    rocks, wall_maps, max_y = data
    rocks = frozenset(rocks)
    wall_counter = None
    known = {}
    for i in range(1_000_000_000):
        if rocks in known:
            cycle_start = known[rocks]
            cycle_length = i - cycle_start
            offset = (1_000_000_000 - cycle_start) % cycle_length
            inverted_map = {val: key for key, val in known.items()}
            rocks = inverted_map[cycle_start + offset]
            rocks = gen_rocks_iter_from_wall_counter(
                {key: val for key, val in rocks}, "E"
            )
            out = sum(max_y + 1 - rock.imag for rock in rocks)
            return round(out)
        else:
            known[rocks] = i
        wall_counter = cycle_roll_rocks(rocks, wall_maps, wall_counter)
        rocks = frozenset((key, val) for key, val in wall_counter.items())


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1, data = part_1(data)
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
