import argparse
import time
from collections import defaultdict


def read_file(fname):
    # {card_id: (winning_numbers, your_numbers)}
    data = {}
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                card, numbers = strip.split(":")
                key = int(card.split()[-1])
                winning, your = numbers.split("|")
                winning = set(int(i) for i in winning.split())
                your = set(int(i) for i in your.split())
                data[key] = (winning, your)

    return data


def part_1(data):
    out = 0
    for winning, your in data.values():
        out += int(2 ** (len(winning & your) - 1))
    return out


def part_2(data):
    counts = defaultdict(lambda: 1)
    out = 0
    for key, (winning, your) in data.items():
        count = counts[key]
        out += count
        wins = len(winning & your)
        for i in range(key + 1, key + wins + 1):
            counts[i] += count
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
