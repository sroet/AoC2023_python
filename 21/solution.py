import argparse
import time
from collections import deque, Counter
from functools import lru_cache

def read_file(fname):
    rocks = set()
    start = None
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    if c == '#':
                        rocks.add(complex(x,y))
                    elif c == 'S':
                        start = complex(x,y)
    return rocks, start, x, y

directions= (complex(0,1), complex(0,-1), complex(1,0), complex(-1, 0))

def map_complex(c, max_real, max_imag):
    return complex(c.real % (max_real+1), c.imag % (max_imag + 1))

def map_to_field(c, max_x, max_y):
    return (c.real//(max_x+1), c.imag//(max_y+1))

def part_1(data, steps):
    rocks, start, max_x, max_y = data
    # add boundary of rocks for now
    #rocks |= set(complex(-1, y) for y in range(-1, max_y+1))
    #rocks |= set(complex(max_x+1, y) for y in range(-1, max_y+1))
    #rocks |= set(complex(x, -1) for x in range(-1, max_x+1))
    #rocks |= set(complex(x, max_y+1) for x in range(-1, max_x+1))
 
    current_queue = set([start])
    for i in range(steps):
        next_queue = set()
        while current_queue:
            coord = current_queue.pop()
            next_queue |= set(coord+d for d in directions)
        current_queue = set( i for i in next_queue if map_complex(i, max_x, max_y) not in rocks)

    #ref = Counter([map_to_field(c, max_x, max_y) for c in current_queue])
    return len(current_queue)

def sort_seeds(seeds):
    seen = set()
    temp = [(key, val) for key, val in seeds]
    temp.sort(key=lambda x: x[1])
    return temp

@lru_cache(maxsize=1000)
def fill_field(seeds, rocks, max_x, max_y, odd=False, max_step=None):
    # todo: check if this is sane
    queue = deque([i for i in sort_seeds(seeds)])
    seen = {}
    top_boundary = {}
    bottom_boundary = {}
    left_boundary = {}
    right_boundary = {}
    out = 0
    i_step = 0
    while queue:
        coord, step = queue.pop()
        if coord not in seen and (max_step is None or step <= max_step):
            out += (bool(step) == odd)
        if coord in seen and seen[coord] < step:
            continue
        #print(f"{coord=}, {step=}, {max_step=}")
        next_step = step + 1
        if max_step is not None and next_step > max_step:
            continue
        for d in directions:
            next_coord = coord+d
            if next_coord in rocks:
                continue
            count = True
            if next_coord in seen:
                if next_step >= seen[next_coord]:
                    continue
                if seen[next_coord] % 2 == odd == next_step % 2:
                    count = False
            seen[next_coord] = next_step
            if next_coord.real < 0:
                left_boundary[next_coord] = next_step
                continue
            elif next_coord.real > max_x:
                right_boundary[next_coord] = next_step
                continue
            elif next_coord.imag < 0:
                top_boundary[next_coord] = next_step
                continue
            elif next_coord.imag > max_y:
                bottom_boundary[next_coord] = next_step
                continue
            if bool(next_step % 2) == odd and count:
                out += 1
            queue.append((next_coord, next_step))
            i_step = max(step, i_step)
    return out, i_step, top_boundary, bottom_boundary, left_boundary, right_boundary
        
def convert_to_tuple(boundary, offset):
    out = []
    for key, val in boundary.items():
        out.append((key, val-offset))
    return tuple(out)


def part_2(data, steps):
    rocks, start, max_x, max_y = data
    print(max_x, max_y)
    # Notes:
    # - every point can be reached with some number of steps and then cycling with len(2)
    # - the fill of a plot depends on the state of 3 of surrounding squares
    # - assume for now that every point is first reached by the seed
    out = -1 # offset double count of the start
    rocks = frozenset(rocks)
    current_field = (0, 0)
    max_diff = max_x+max_y
    odd = bool(steps%2)
    queue = deque()
    queue.append(current_field)
    seed_edges = {(0,0): {start : 0}}
    seen = set()
    last_print = 0
    while queue:
        current_field = queue.popleft()
        if current_field in seen:
            continue
        else:
            seen.add(current_field)
        #print(seed_edges)
        #TODO: replace by pop for preventing memory growth
        #possible_seeds = seed_edges.get(current_field, None)
        possible_seeds = seed_edges.pop(current_field, None)

        if not possible_seeds:
            # no furter seeding
            continue
        current_step = min(val for val in possible_seeds.values())
        current_step -= current_step % 2
        seeds = convert_to_tuple(possible_seeds, current_step)
        if current_step > 10**last_print:
            print(f"{current_step=}")
            last_print += 1
        #help caching
        #print(f"{current_step=}, {steps=}")
        if current_step + 2*max_diff > steps:
            #print(f"{current_field=} {seeds=}")
            max_step = steps-current_step
        else:
            max_step = None 
        temp, i_step, top, bottom, left, right = fill_field(seeds, rocks, max_x, max_y, odd, max_step)
        out += temp
        max_diff = max(max_diff, i_step)
        x,y = current_field
        # top
        dct = seed_edges.get((x, y-1), dict())
        dct.update({complex(key.real, max_y): val+current_step for key,val in top.items()})
        seed_edges[(x, y-1)] = dct
        # bottom
        dct = seed_edges.get((x, y+1), dict())
        dct.update({complex(key.real, 0) : val+current_step for key,val in bottom.items()})
        seed_edges[(x, y+1)] = dct
        # left
        dct = seed_edges.get((x-1, y), dict())
        dct.update({complex(max_x, key.imag): val+current_step for key,val in left.items()})
        seed_edges[(x-1, y)] = dct
        # right
        dct = seed_edges.get((x+1, y), dict())
        dct.update({complex(0, key.imag): val+current_step for key,val in right.items()})
        seed_edges[(x+1, y)] = dct
        queue.appendleft((x+1, y))
        queue.appendleft((x-1, y))
        queue.extend([(x, y+1), (x, y-1)])
        #print(f"{current_field=} {temp=}")
    return out


def main(fname, steps=64, steps2=10):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data, steps)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data, steps2)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--steps", type=int, default=64, required=False)
    parser.add_argument("--steps_2", type=int, default=26501365, required=False)
    args = parser.parse_args()
    filename = args.filename
    steps = args.steps
    steps2 = args.steps_2
    main(filename, steps, steps2)
