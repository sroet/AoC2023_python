import argparse
import time


def read_file(fname):
    data = []
    temp_data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                temp_data.append(strip)
            elif temp_data:
                data.append(temp_data)
                temp_data = []
    if temp_data:
        data.append(temp_data)
    return data


def part_1(data):
    out = 0
    for mirror in data:
        length = len(mirror)
        # check horizontal split
        for i in range(length - 1):
            if all(x == y for x, y in zip(mirror[i::-1], mirror[i + 1 :])):
                out += 100 * (i + 1)
                break
        else:
            # vertical split
            mirror = list(zip(*mirror))
            length = len(mirror)
            for i in range(length - 1):
                if all(x == y for x, y in zip(mirror[i::-1], mirror[i + 1 :])):
                    out += i + 1
                    break
    return out


def part_2(data):
    out = 0
    for mirror in data:
        length = len(mirror)
        # check horizontal split
        for i in range(length - 1):
            current_diff = 0
            for x, y in zip(mirror[i::-1], mirror[i + 1 : :]):
                if x != y:
                    current_diff += sum(int(a != b) for a, b in zip(x, y))
                if current_diff > 1:
                    break
            else:
                if current_diff == 0:
                    # part 1 result
                    continue
                out += 100 * (i + 1)
                break
        else:
            # vertical split
            mirror = list(zip(*mirror))
            length = len(mirror)
            for i in range(length - 1):
                current_diff = 0
                for x, y in zip(mirror[i::-1], mirror[i + 1 : :]):
                    if x != y:
                        current_diff += sum(int(a != b) for a, b in zip(x, y))
                    if current_diff > 1:
                        break
                else:
                    if current_diff == 0:
                        # part 1 result
                        continue
                    out += i + 1
                    break
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
