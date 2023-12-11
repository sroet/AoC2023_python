import argparse
import time
from itertools import combinations


def read_file(fname):
    data = set()
    filled_x = set()
    filled_y = set()
    empty_x = set()
    empty_y = set()
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            empty_y.add(y)
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    empty_x.add(x)
                    if c == "#":
                        data.add((x, y))
                        filled_x.add(x)
                        filled_y.add(y)
    # use empty instead of filled as len(empty)=6 and len(filled)=134
    # and we loop over this set for every combination
    empty_y -= filled_y
    empty_x -= filled_x
    return data, empty_x, empty_y


def parts(data, time=2):
    galaxies, empty_x, empty_y = data
    out = 0
    for gal1, gal2 in combinations(galaxies, 2):
        x1, y1 = gal1
        x2, y2 = gal2
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        y_dist = max_y - min_y
        for y in empty_y:
            if min_y < y < max_y:
                y_dist += time - 1
        x_dist = max_x - min_x
        for x in empty_x:
            if min_x < x < max_x:
                x_dist += time - 1
        out += y_dist + x_dist
    return round(out)


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = parts(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = parts(data, 1_000_000)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
