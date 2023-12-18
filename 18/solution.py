import argparse
import time
from collections import deque

def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                split = strip.split()
                data.append((split[0], int(split[1]), split[2].strip('(#)')))
    return data

directions = {'U': complex(0, -1),
        'D': complex(0, 1),
        'L': complex(-1, 0),
        'R': complex(1, 0)}

def print_map(trench, min_x, max_x, min_y, max_y):
    for line in range(min_y, max_y+1):
        out = ''
        for c in range(min_x, max_x+1):
            if complex(c, line) in trench:
                out += '#'
            else:
                out += '.'
        print(out)
    print('')

def flood_fill(trench, min_x, max_x, min_y, max_y):
    # flood fill outside
    dirs = [val for val in directions.values()]
    start = complex(min_x, min_y)
    queue = deque([start])
    seen = set([start])
    while queue:
        current = queue.popleft()
        for direction in dirs:
            next_coord = current + direction
            if not (min_x <= next_coord.real <= max_x and min_y <= next_coord.imag <= max_y):
                continue
            if next_coord in seen or next_coord in trench:
                continue
            seen.add(next_coord)
            queue.append(next_coord)
    return seen 

def part_1(data):
    current = complex(0,0)
    out = 0
    for direction, length, _ in data:
        direction = directions[direction]
        # leverage shoelace formula
        next_coord = current + direction*length
        out += (current.real * next_coord.imag) - (next_coord.real * current.imag) + length
        current = next_coord
    return round(out)//2 + 1

part_2_directions = {0: complex(1, 0),
        1: complex(0, 1),
        2: complex(-1, 0),
        3: complex(0, -1)}

def part_2(data):
    current = complex(0,0)
    out = 0
    for _, _, instruction in data:
        direction = part_2_directions[int(instruction[-1])]
        length = int(instruction[:-1], 16)
        # leverage shoelace formula
        next_coord = current + direction*length
        out += (current.real * next_coord.imag) - (next_coord.real * current.imag) + length
        current = next_coord
    return round(out)//2 + 1

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
