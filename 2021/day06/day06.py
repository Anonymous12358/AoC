from functools import partial


def simulate(raw_inp, gens):
    fish = {i: raw_inp.count(str(i)) for i in range(7)}
    for _ in range(gens):
        fish = {k-1: v for k, v in fish.items()}
        fish[8] = fish[-1]
        fish[6] = (fish[6] if 6 in fish.keys() else 0) + fish[-1]
        fish.pop(-1)
    return sum(fish.values())


part_a = partial(simulate, gens=80)
part_b = partial(simulate, gens=256)
