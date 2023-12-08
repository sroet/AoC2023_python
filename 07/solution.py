import argparse
import time
from collections import Counter

order = "AKQJT98765432"
order_map = {e: f"{i+1:02d}" for i, e in enumerate(order)}
order2 = "AKQT98765432J"
order2_map = {e: f"{i+1:02d}" for i, e in enumerate(order2)}


def get_hand_type(hand):
    count = Counter(hand)
    val = count.most_common()
    counts = tuple([i[1] for i in val[:2]])
    match counts:
        case (5,):
            hand_type = 0
        case (4, _):
            hand_type = 1
        case (3, 2):
            hand_type = 2
        case (3, _):
            hand_type = 3
        case (2, 2):
            hand_type = 4
        case (2, _):
            hand_type = 5
        case _:
            hand_type = 6
    return hand_type


def make_order_tuple_part1(hand):
    hand_type = get_hand_type(hand)
    card_val = int("".join(order_map[i] for i in hand))
    return (hand_type, card_val, hand)


def make_order_tuple_part2(hand):
    vals = set(hand)
    hand_type = min(get_hand_type(hand.replace("J", card)) for card in vals)
    card_val = int("".join(order2_map[i] for i in hand))
    return (hand_type, card_val, hand)


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                split = strip.split()
                data.append((split[0], int(split[1])))
    return data


def part_1(data):
    temp = [(make_order_tuple_part1(hand), bid) for hand, bid in data]
    temp.sort()
    out = 0
    for i, e in enumerate(temp[::-1], 1):
        out += e[1] * i
    return out


def part_2(data):
    temp = [(make_order_tuple_part2(hand), bid) for hand, bid in data]
    temp.sort()
    out = 0
    for i, e in enumerate(temp[::-1], 1):
        out += e[1] * i
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
