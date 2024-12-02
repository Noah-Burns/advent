from pathlib import Path


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line and line != [""], lines))

    return [[int(entry) for entry in line] for line in lines]


def calculate_diffs(line: list[int]) -> list[int]:
    res = []

    for ii, num in enumerate(line[1:], start=1):
        res.append(num - line[ii - 1])

    return res


def extrapolate(line: list[int], is_forawrd=True) -> int:
    current_line = line
    diff_grid = [current_line]

    while True:
        diffs = calculate_diffs(current_line)
        diff_grid.append(diffs)

        if not any(diffs):
            break

        current_line = diffs

    if is_forawrd:
        return sum([line[-1] for line in diff_grid])
    else:
        res = 0
        for line in diff_grid[::-1]:
            res -= line[0]
            res *= -1

        return res


def sum_extrapolations(grid: list[list[int]], is_forward=True) -> int:
    return sum(extrapolate(line, is_forward) for line in grid)


### Part 1
# Analyze your OASIS report and extrapolate the next value for each history.
# What is the sum of these extrapolated values?
print(sum_extrapolations(parse_input("example_2309.txt")))
print(sum_extrapolations(parse_input("input_2309.txt")))

### Part 2
print(sum_extrapolations(parse_input("example_2309.txt"), is_forward=False))
print(sum_extrapolations(parse_input("input_2309.txt"), is_forward=False))
