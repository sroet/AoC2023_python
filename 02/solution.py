import argparse
import time


# structure = {game_id: [(r, g, b), (r,g,b)...]}
def read_file(fname):
    data = {}
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip == "":
                continue
            game, parts = strip.split(":")
            parts = parts.split(";")
            out = []
            for hand in parts:
                r, g, b = 0, 0, 0
                hand = hand.split(",")
                for color in hand:
                    i, c = color.split()
                    if "red" in c:
                        r = int(i)
                    elif "green" in c:
                        g = int(i)
                    elif "blue" in c:
                        b = int(i)
                    else:
                        raise ValueError("found no color")
                out.append((r, g, b))
            key = int(game.split()[-1])
            data[key] = out
    return data


def part_1(data):
    # (r,g,b)
    limit = (12, 13, 14)
    out = 0
    for key, val in data.items():
        valid = True
        for hand in val:
            if any(c > lim for c, lim in zip(hand, limit)):
                valid = False
                break
        if valid:
            out += key
    return out


def part_2(data):
    out = 0
    for key, val in data.items():
        r, g, b = (max(i) for i in zip(*val))
        power = r * g * b
        out += power
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
