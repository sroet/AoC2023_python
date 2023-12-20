import argparse
import time
from collections import deque, Counter
from math import lcm


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


class Modules:
    def __init__(self, name, count, destinations=None):
        self._destinations = destinations
        self.inp_queue = deque()
        self.name = name
        self.count = count

    def override_destinations(self, destinations):
        self._destinations = destinations

    def process(self):
        pass

    def inp(self, signal):
        self.inp_queue.append(signal)


class FlipFlop(Modules):
    def __init__(self, name, count, destinations):
        self.state = 0
        super().__init__(name, count, destinations)

    def process(self):
        _, signal = self.inp_queue.popleft()
        if signal:
            return
        self.state = int(not self.state)
        _ = [dest.inp((self.name, self.state)) for dest in self._destinations]
        self.count[self.state] += len(self._destinations)
        return self._destinations

    def reset(self):
        self.state = 0


class Conjunction(Modules):
    def __init__(self, name, count, destinations):
        super().__init__(name, count, destinations)
        self.state = {}
        self.out = 1

    def register_input(self, input_name):
        self.state[input_name] = 0

    def process(self):
        name, signal = self.inp_queue.popleft()
        self.state[name] = signal
        out = int(not all(self.state.values()))
        _ = [dest.inp((self.name, out)) for dest in self._destinations]
        self.count[out] += len(self._destinations)
        self.out = out
        return self._destinations

    def reset(self):
        for key in self.state.keys():
            self.state[key] = 0


class Broadcast(Modules):
    def button(self):
        out = 0
        _ = [dest.inp((self.name, out)) for dest in self._destinations]
        self.count[out] += len(self._destinations) + 1
        return self._destinations

    def reset(self):
        pass


class Output(Modules):
    def process(self):
        return

    def inp(self, inp):
        return


module_types = {"b": Broadcast, "%": FlipFlop, "&": Conjunction}


def part_1(data):
    # generate all classes
    modules = {}
    count = Counter()
    for line in data:
        name, destinations = line.split("->")
        name = name.strip()
        destinations = [i.strip() for i in destinations.split(",")]
        cls = module_types[name[0]]
        if name[0] == "b":
            name = name
        else:
            name = name[1:]
        modules[name] = cls(name, count, destinations)
    # update destinations to instances and register conjunction inputs
    for module in modules.values():
        new_dest = []
        for dest in module._destinations:
            dest_module = modules.get(dest, Output(dest, count, None))
            new_dest.append(dest_module)
            if isinstance(dest_module, Conjunction):
                dest_module.register_input(module.name)
        module._destinations = new_dest

    broadcaster = modules["broadcaster"]
    for _ in range(1000):
        queue = deque(broadcaster.button())
        while queue:
            next_module = queue.popleft()
            out = next_module.process()
            if out is not None:
                queue.extend(out)
    return count[0] * count[1], modules


def part_2(modules):
    # This part requires manual input reading/parsing
    # notes for my input:
    #  rx
    #  ^
    #  |
    # &gf
    #  ^
    #  |
    # ( &qs, &sv, &pg, &sp) (need all have one low)
    #  ^    ^    ^    ^
    #  |    |    |    |
    #  &mh, &jt, &pz, &rn
    # all of these need to output low and cycle in a sane amount of button presses

    for module in modules.values():
        module.reset()
    broadcaster = modules["broadcaster"]
    cycle_modules = ["mh", "jt", "pz", "rn"]
    out_search = 0
    cycles = {key: 0 for key in cycle_modules}
    for i in range(10000):
        queue = deque(broadcaster.button())
        while queue:
            next_module = queue.popleft()
            out = next_module.process()
            if out is not None:
                queue.extend(out)
            if next_module.name in cycle_modules and next_module.out == out_search:
                # decide to check the low output
                if cycles[next_module.name] == 0:
                    cycles[next_module.name] = i + 1
        if all(val != 0 for val in cycles.values()):
            break
    return lcm(*[val for val in cycles.values()])


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1, modules = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(modules)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
