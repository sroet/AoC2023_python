import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def part_1(data):
    out = 0
    for line in data:
        temp = [int(c) for c in line if c.isnumeric()]
        out += temp[0] * 10
        out += temp[-1]
    return out


convert_dict = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_2(data):
    out = 0
    for line in data:
        min_idx, min_val = len(line) + 1, 0
        max_idx, max_val = -1, 0
        for key, val in convert_dict.items():
            idx = line.find(str(key))
            if idx != -1 and idx < min_idx:
                min_idx = idx
                min_val = val
            idx = line.rfind(str(key))
            if idx != -1 and idx > max_idx:
                max_idx = idx
                max_val = val
        out += 10 * min_val + max_val
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
