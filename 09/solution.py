import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append([int(i) for i in strip.split()])
    return data


def parts(data):
    out1, out2 = 0, 0
    for line in data:
        final_numbers = []
        first_numbers = []
        current_line = line
        while not all(i == 0 for i in current_line):
            final_numbers.append(current_line[-1])
            first_numbers.append(current_line[0])
            next_line = [i - j for j, i in zip(current_line, current_line[1:])]
            current_line = next_line

        # Part 1
        current_diff = 0
        while final_numbers:
            current_diff += final_numbers.pop()
        out1 += current_diff

        # Part 2
        current_diff = 0
        while first_numbers:
            current_diff = first_numbers.pop() - current_diff
        out2 += current_diff

    return out1, out2


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1, total_2 = parts(data)
    print(f"Part 1: {total_1}")
    print(f"Part 2: {total_2}")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
