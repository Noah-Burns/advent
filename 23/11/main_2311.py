from pathlib import Path


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = list(filter(lambda line: line and line != [""], lines))

    return lines


def add_empty_rc(universe):
    res = universe
    len_line = len(universe[0])
    rows_to_add = []
    cols_to_add = []

    for ii, line in enumerate(universe):
        if line == "." * len_line:
            rows_to_add.append(ii)

    for jj in range(len_line):
        col = [line[jj] for line in universe]
        col = "".join(col)

        if col == "." * len(universe):
            cols_to_add.append(jj)

    while rows_to_add:
        n_row = rows_to_add.pop(0)
        res.insert(n_row, "." * len_line)

        rows_to_add = [n_row + 1 for n_row in rows_to_add]

    while cols_to_add:
        n_col = cols_to_add.pop(0)
        for jj, line in enumerate(res):
            res[jj] = line[:n_col] + "." + line[n_col:]

        cols_to_add = [n_col + 1 for n_col in cols_to_add]

    return res


def find_galaxies(universe):
    galaxies = []
    for ii, line in enumerate(universe):
        for jj, char in enumerate(line):
            if char == "#":
                galaxies.append((ii, jj))

    return galaxies


def construct_pairs(galaxies):
    pairs = []

    for ii, g1 in enumerate(galaxies):
        for g2 in galaxies[ii + 1 :]:
            pairs.append((g1, g2))

    return pairs


def find_shortest_distance(galaxies):
    g1 = galaxies[0]
    g2 = galaxies[1]

    # taxicab disance formula
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


def solve_1(universe):
    universe = add_empty_rc(universe)
    galaxies = find_galaxies(universe)
    pairs = construct_pairs(galaxies)
    distances = [find_shortest_distance(pair) for pair in pairs]

    return sum(distances)


def tag_pair(pair, universe):
    g1 = pair[0]
    g2 = pair[1]
    n_spanned = 0

    for ii in range(min(g1[0], g2[0]) + 1, max(g1[0], g2[0])):
        if universe[ii] == "." * len(universe[0]):
            n_spanned += 1

    for jj in range(min(g1[1], g2[1]) + 1, max(g1[1], g2[1])):
        col = [line[jj] for line in universe]
        col = "".join(col)

        if col == "." * len(universe):
            n_spanned += 1

    return (g1, g2, n_spanned)


def solve_2(universe, x):
    galaxies = find_galaxies(universe)
    pairs = construct_pairs(galaxies)
    tagged_pairs = [tag_pair(pair, universe) for pair in pairs]
    distances = [find_shortest_distance(tagged_pair[:2]) + x * tagged_pair[2] for tagged_pair in tagged_pairs]

    return sum(distances)


### Part 1
print(solve_1(parse_input("example_1_2311.txt")))
print(solve_1(parse_input("input_2311.txt")))

### Part 2
# adding x r/c just increases the distance between
# any pair that spans those added r/c by x.
# If we "tag" each pair by how many added r/c it spans,
# we can just add that many to its distance
print(solve_2(parse_input("example_1_2311.txt"), 10))
print(solve_2(parse_input("example_1_2311.txt"), 100))
# print(solve_2(parse_input("input_2311.txt"), 1e6))
