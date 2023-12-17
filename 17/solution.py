import argparse
import time
import heapq
import itertools


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append([int(i) for i in strip])
    return data


class PriorityQ:
    # Inspired by: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = "<removed-task>"
        self.counter = itertools.count()

    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            if self.entry_finder[task][0] < priority:
                # Only update if the current found priority is lower
                return
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        # debug
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task, priority
        raise KeyError("Empty pq")


directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

oposites = {"<": ">", ">": "<", "v": "^", "^": "v", ".": ""}


def part_1(data):
    # task = (current_weight, coord, last_move, repeat)
    queue = PriorityQ()
    weight, start = 0, ((0, 0), ".", 0)
    queue.add_task(start, weight)
    moves = "<>^v"
    max_x = len(data[0])
    max_y = len(data)
    seen = {}
    while True:
        try:
            ((x, y), last_move, repeat), weight = queue.pop_task()
        except KeyError as err:
            print(err)
            break
        if (x, y, last_move, repeat) in seen:
            continue
        else:
            seen[(x, y, last_move, repeat)] = weight
        oposite = oposites[last_move]
        for move in moves:
            if move == last_move and repeat == 3:
                continue
            elif move == last_move:
                n_repeat = repeat + 1
            else:
                n_repeat = 1
            if move == oposite:
                continue
            dx, dy = directions[move]
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < max_x and 0 <= ny < max_y):
                continue
            if (nx, ny, move, n_repeat) in seen:
                continue
            n_weight = weight + data[ny][nx]
            if nx == max_x - 1 and ny == max_y - 1:
                return n_weight
            queue.add_task(((nx, ny), move, n_repeat), n_weight)


def part_2(data):
    # task = (current_weight, coord, last_move, repeat)
    queue = PriorityQ()
    weight, start = 0, ((0, 0), ".", 0)
    queue.add_task(start, weight)
    max_x = len(data[0])
    max_y = len(data)
    seen = {}
    while True:
        try:
            ((x, y), last_move, repeat), weight = queue.pop_task()
        except KeyError as err:
            print(err)
            break
        if (x, y, last_move, repeat) in seen:
            continue
        else:
            seen[(x, y, last_move, repeat)] = weight

        moves = "<>^v"
        if repeat < 4 and last_move != ".":
            moves = last_move
        oposite = oposites[last_move]
        for move in moves:
            if move == last_move and repeat == 10:
                continue
            elif move == last_move:
                n_repeat = repeat + 1
            else:
                n_repeat = 1
            if move == oposite:
                continue
            dx, dy = directions[move]
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < max_x and 0 <= ny < max_y):
                continue
            if (nx, ny, move, n_repeat) in seen:
                continue
            n_weight = weight + data[ny][nx]
            if nx == max_x - 1 and ny == max_y - 1:
                if 4 <= n_repeat:
                    return n_weight
                continue
            queue.add_task(((nx, ny), move, n_repeat), n_weight)

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
