import argparse
import time


def read_file(fname):
    rocks = set()
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


def sort_key_N(c):
    # sort top to bottom
    return c.imag


def sort_key_W(c):
    # sort left to right
    return c.real


def sort_key_S(c):
    # sort bottom to top
    return -c.imag


def sort_key_E(c):
    # sort right to left
    return -c.real


sort_keys = {"N": sort_key_N, "W": sort_key_W, "S": sort_key_S, "E": sort_key_E}

directions = {"N": -1j, "W": -1, "S": 1j, "E": 1}


def make_boundary_checks(max_x, max_y):
    # N, W, S, E
    out = {
        "N": lambda x: x.imag < 0,
        "W": lambda x: x.real < 0,
        "S": lambda x: x.imag > max_y,
        "E": lambda x: x.real > max_x,
    }
    return out


def print_map(rocks, walls):
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


def roll_rocks(rocks, walls, sort_key, direction, boundary):
    rocks = list(rocks)
    rocks.sort(key=sort_key)
    new_rocks = set()
    for rock in rocks:
        new_rock = rock 
        while not boundary(new_rock) and (
            new_rock not in new_rocks and new_rock not in walls
        ):
            rock = new_rock
            new_rock += direction
        new_rocks.add(rock)
    return frozenset(new_rocks)


def part_1(data):
    rocks, walls, max_y, max_x = data
    boundaries = make_boundary_checks(max_x, max_y)
    new_rocks = roll_rocks(
        rocks, walls, sort_keys["N"], directions["N"], boundaries["N"]
    )
    out = sum(max_y + 1 - rock.imag for rock in new_rocks)
    return round(out)


def part_2(data):
    rocks, walls, max_y, max_x = data
    rocks = frozenset(rocks)
    boundaries = make_boundary_checks(max_x, max_y)
    known = {}
    for i in range(1_000_000_000):
        if rocks in known:
            cycle_start = known[rocks]
            cycle_length = i - cycle_start
            offset = (1_000_000_000 - cycle_start) % cycle_length
            inverted_map = {val: key for key, val in known.items()}
            rocks = inverted_map[cycle_start + offset]
            out = sum(max_y + 1 - rock.imag for rock in rocks)
            return round(out)
        else:
            known[rocks] = i
        for direction in "NWSE":
            rocks = roll_rocks(
                rocks,
                walls,
                sort_keys[direction],
                directions[direction],
                boundaries[direction],
            )


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
