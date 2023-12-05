import argparse
import time


def read_file(fname):
    seeds, maps = [], []
    current_map = []
    with open(fname, "r") as file:
        for i, line in enumerate(file):
            strip = line.strip()
            if i == 0:
                # seeds line:
                seeds = [int(i) for i in strip.split()[1:]]
                continue
            if strip != "":
                if not strip[0].isnumeric():
                    continue
                # (s_dest, s_source, range)
                current_map.append(tuple(int(i) for i in strip.split()))
            elif current_map:
                maps.append(current_map)
                current_map = []
        if current_map:
            maps.append(current_map)
    return seeds, maps


def run_through_map(seed, maps):
    for current_map in maps:
        # this loop does not replace if seed is not found, as intended
        for start_d, start_s, rang in current_map:
            if start_s <= seed < start_s + rang:
                seed = seed - start_s + start_d
                break
    return seed


def section_inputs(seed_range, maps):
    # assumes sorted maps in (start_s, start_d, rang) order
    # seed range in [(start, range), ...]
    for current_map in maps:
        next_seed_range = []
        for seed_start, seed_r in seed_range:
            for start_s, start_d, rang in current_map:
                assert seed_r > 0  # debug check
                if start_s >= seed_start + seed_r:
                    # complete seed range is left of map
                    continue
                if start_s + rang <= seed_start:
                    # complete seed range is right of map
                    continue
                if start_s <= seed_start and start_s + rang >= seed_start + seed_r:
                    # complete seed range is converted
                    next_seed_range.append((seed_start - start_s + start_d, seed_r))
                    break
                if start_s <= seed_start and start_s + rang < seed_start + seed_r:
                    # left side is converted
                    covered = rang - (seed_start - start_s)
                    next_seed_range.append((seed_start - start_s + start_d, covered))
                    seed_start = start_s + rang
                    seed_r -= covered
                    continue
                if start_s > seed_start and start_s + rang >= seed_start + seed_r:
                    # right side is converted (and left is unaltered assuming ordered maps)
                    # append unconverted left range
                    next_seed_range.append((seed_start, start_s - seed_start))
                    if start_s + rang >= seed_start + seed_r:
                        # full right side is converted
                        covered = seed_r - (start_s - seed_start)
                        # append converted right range
                        next_seed_range.append((start_d, covered))
                        break
                    else:
                        # only part is converted
                        next_seed_range.append(start_d, rang)
                        seed_r = (seed_start + seed_r) - (start_s + rang)
                        seed_start = start_s + rang
                        continue
                # This should never be hit
                raise ValueError("uncaught case")
            else:
                # if we reached end of maps and still have a seed_r left
                next_seed_range.append((seed_start, seed_r))
        seed_range = next_seed_range
    seed_range.sort()
    return seed_range[0][0]


def part_1(data):
    seeds, maps = data
    out = min(run_through_map(seed, maps) for seed in seeds)
    return out


def part_2(data):
    seeds, maps = data
    # convert map order and sort them to make sectioning easier
    maps = [[(j, i, k) for i, j, k in m] for m in maps]
    for m in maps:
        m.sort()
    out = None
    for seed_range in zip(seeds[::2], seeds[1::2]):
        temp = section_inputs([seed_range], maps)
        if out is None:
            out = temp
        else:
            out = min(out, temp)
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
