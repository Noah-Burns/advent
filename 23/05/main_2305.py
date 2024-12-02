#!/usr/bin/python3
from pathlib import Path

# Make a multitree out of the input
# Each seed maps 1:1 to a loc, but the tree grows exponentially at each step
# We're probably not actually supposed to construct an entire tree,
# but instead just every valid path for each seed
# Make a list of lists of mt nodes, when jumping to the next level, find all valid jumps and recursively go from there
# and if our dest isn't mapped, jump to our own number.
# Assuming the maps are always 1:1.


class MTreeNode:
    def __init__(self, mt_node_str):
        mt_node_str_list = mt_node_str.split(" ")
        dest_range_start = int(mt_node_str_list[0])
        source_range_start = int(mt_node_str_list[1])
        range_length = int(mt_node_str_list[2])

        self.source_range = range(source_range_start, source_range_start + range_length)
        self.dest_range = range(dest_range_start, dest_range_start + range_length)

        self.as_ranges = (
            (source_range_start, source_range_start + range_length),
            (dest_range_start, dest_range_start + range_length),
        )

    def __repr__(self) -> str:
        ranges = self.as_ranges
        return f"{ranges[0]} -> {ranges[1]}"


P = Path(__file__).parent.resolve() / "input_2305.txt"
almanac_list = P.read_text().split("\n")

seeds = almanac_list[1]
seeds = [int(seed_str) for seed_str in seeds.split(" ")]

mtree, level = [], []

for line in almanac_list[3:]:
    if line == "" and level:
        mtree.append(level)
        level = []
        continue

    if line[0].isnumeric():
        level.append(MTreeNode(line))

# print(seeds)
# print(mtree)


def find_dest(seed, mtree):
    current_num = seed

    for level in mtree:
        for node in level:
            if current_num in node.source_range:
                # if the current num is mapped by the next level, update it and jump to the next level
                current_num = node.dest_range[node.source_range.index(current_num)]
                break

    return current_num


dests = [find_dest(seed, mtree) for seed in seeds]

# print(dests)
# print(min(dests))

#### Part 2
# Instead of actually going through each seed, think of each node as an interval
# then compose all the intervals onto each other
# represent an interval [a, b) interval as Python tuple (a, b).
#
# To compose an interval A onto the next level's intervals, split it into subintervals.
# Some properties:
# [a, b) + [b, c) = [a, c)
# length of [a, b) = b - a

# print("\n\n\n")


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, point):
        return self.start <= point < self.end

    def __add__(self, addend):
        # add an interval to this one

        if not self.end == addend.start or addend.end == self.start:
            raise ValueError("Intervals are not adjacent")

        start = min(self.start, addend.start)
        end = max(self.end, addend.end)
        return Interval(start, end)

    def __repr__(self):
        return f"[{self.start}, {self.end})"

    def shift(self, delta):
        return Interval(self.start + delta, self.end + delta)


class IntervalMapping:
    def __init__(self, source_interval: Interval, dest_interval: Interval):
        self.source_interval = source_interval
        self.dest_interval = dest_interval
        self.delta = self.dest_interval.start - self.source_interval.start

    def __repr__(self):
        return f"{self.source_interval} -> {self.dest_interval}"


seed_intervals = []
for ii in range(0, len(seeds), 2):
    seed_intervals.append(Interval(seeds[ii], seeds[ii] + seeds[ii + 1]))

print(seed_intervals)

# represent each level as a list of of interval mappings
levels = [
    [
        IntervalMapping(Interval(*node.as_ranges[0]), Interval(*node.as_ranges[1]))
        for node in level
    ]
    for level in mtree
]
# print(levels)


def compose_multiple_interval_mappings(
    mappings: list[IntervalMapping], start_interval: Interval
) -> list[Interval]:
    # do the compositions p composed q
    # [p.start                                                                p.end)
    #                  [q.start                                q.end)
    # [       A       )[                     B                      )[       C     )
    #
    # A: region in p before q.start
    # C: region in p after q.end
    # B: region in p that intersects with q

    res = []
    intervals = [start_interval]

    for mapping in mappings:
        q = mapping.source_interval
        new_intervals = []

        for p in intervals:
            A = (p.start, min(p.end, q.start))
            B = (max(p.start, q.start), min(p.end, q.end))
            C = (max(p.start, q.end), p.end)

            if A[1] > A[0]:
                new_intervals.append(Interval(*A))

            if B[1] > B[0]:
                res.append(Interval(*B).shift(mapping.delta))

            if C[1] > C[0]:
                new_intervals.append(Interval(*C))

        intervals = new_intervals

    return res + intervals


for level in levels:
    print(len(seed_intervals))
    new_intervals = []

    for p in seed_intervals:
        new_intervals.extend(compose_multiple_interval_mappings(level, p))

    seed_intervals = new_intervals

print(min(p.start for p in seed_intervals))
