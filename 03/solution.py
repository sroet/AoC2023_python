import argparse
import time
from math import prod


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def make_maps(data):
    symbol_set = {}  # needs to be a dict for part 2
    number_dict = {}
    for y, line in enumerate(data):
        temp = ""
        for x, c in enumerate(line):
            if c.isnumeric():
                temp += c
                continue
            elif temp:
                number_start = x - len(temp)
                number_dict[complex(number_start, y)] = int(temp)
                temp = ""
            if c != ".":
                symbol_set[complex(x, y)] = c
        if temp:
            number_start = x + 1 - len(temp)
            # needed this way around due to double numbers
            number_dict[complex(number_start, y)] = int(temp)
            temp = ""
    return number_dict, symbol_set


def part_1(data):
    result = 0
    number_dict, symbol_set = make_maps(data)
    for coord, number in number_dict.items():
        x_start = round(coord.real)
        y_start = round(coord.imag)
        x_end = x_start + len(str(number))
        search = (
            complex(x, y)
            for x in range(x_start - 1, x_end + 1)
            for y in range(y_start - 1, y_start + 2)
        )
        if any(s in symbol_set for s in search):
            result += number
    return result


def part_2(data):
    number_dict, symbol_set = make_maps(data)
    gears = {key: list() for key, val in symbol_set.items() if val == "*"}
    for coord, number in number_dict.items():
        x_start = round(coord.real)
        y_start = round(coord.imag)
        x_end = x_start + len(str(number))
        search = (
            complex(x, y)
            for x in range(x_start - 1, x_end + 1)
            for y in range(y_start - 1, y_start + 2)
        )
        for s in search:
            if s in gears:
                gears[s].append(number)
    result = sum(prod(val) for val in gears.values() if len(val) == 2)
    return result

    pass


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
