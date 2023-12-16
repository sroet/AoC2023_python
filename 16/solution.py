import argparse
import time
from collections import deque


def read_file(fname):
    data = {}
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    if c != ".":
                        data[complex(x, y)] = c
    return data, x, y


# Needed to fix matching with complex numbers in python 3.12
class complex(complex):
    __match_args__ = ("real", "imag")


def part_1(data, start=(complex(-1, 0), complex(1, 0))):
    objects, max_x, max_y = data
    known = set()
    energized = set()
    todo = deque()
    todo.append(start)
    while todo:
        coord, direction = todo.popleft()
        new_coord = coord + direction
        # Out of bounds
        if not (0 <= new_coord.real <= max_x and 0 <= new_coord.imag <= max_y):
            continue
        # Already processed
        if (new_coord, direction) in known:
            continue
        else:
            known.add((new_coord, direction))
            energized.add(new_coord)
        match objects.get(new_coord, None), direction:
            case (None, _):
                # Nothing happens
                pass
            case ("/", complex(1, 0)) | ("\\", complex(-1, 0)):
                # Mirror to going up
                direction = complex(0, -1)
            case ("/", complex(-1, 0)) | ("\\", complex(1, 0)):
                # Mirror to going down
                direction = complex(0, 1)
            case ("/", complex(0, 1)) | ("\\", complex(0, -1)):
                # Mirror to going left
                direction = complex(-1, 0)
            case ("/", complex(0, -1)) | ("\\", complex(0, 1)):
                # Mirror to going right
                direction = complex(1, 0)
            case ("|", (complex(0, 1) | complex(0, -1))):
                pass
            case ("|", (complex(1, 0) | complex(-1, 0))):
                todo.append((new_coord, complex(0, 1)))
                direction = complex(0, -1)
            case ("-", (complex(0, 1) | complex(0, -1))):
                todo.append((new_coord, complex(-1, 0)))
                direction = complex(1, 0)
            case ("-", (complex(1, 0) | complex(-1, 0))):
                pass
            case _:
                raise ValueError("missed case")
        todo.append((new_coord, direction))
    return len(energized)


def part_2(data):
    _, max_x, max_y = data
    out = -1
    for x in range(max_x + 1):
        out = max(
            out,
            part_1(data, (complex(x, -1), complex(0, 1))),
            part_1(data, (complex(x, max_y + 1), complex(0, -1))),
        )
    for y in range(max_y + 1):
        out = max(
            out,
            part_1(data, (complex(-1, y), complex(1, 0))),
            part_1(data, (complex(max_x + 1, y), complex(1, 0))),
        )
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
