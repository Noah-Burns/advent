# https://adventofcode.com/2024/day/4
from pathlib import Path
import numpy as np


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    # lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line and line != [""], lines))

    return lines


def find_horiz(lines):
    res = 0

    for row in lines:
        res += row.count("XMAS") + row.count("SAMX")

    return res


def find_vert(lines):
    res = 0

    for ii, _ in enumerate(lines):
        col = [line[ii] for line in lines]
        col = "".join(col)

        res += col.count("XMAS") + col.count("SAMX")

    return res


def find_diag(lines):
    lines = [list(line) for line in lines]
    lines = np.array(lines)
    anti_lines = np.fliplr(lines)
    res = 0

    for ii in range(1 - len(lines), len(lines)):
        diag1 = lines.diagonal(ii)
        diag1 = "".join(diag1)

        diag2 = anti_lines.diagonal(ii)
        diag2 = "".join(diag2)

        res += diag1.count("XMAS") + diag1.count("SAMX") + diag2.count("XMAS") + diag2.count("SAMX")

    return res


def solve_1(lines):
    return find_horiz(lines) + find_vert(lines) + find_diag(lines)


def solve_2(lines):
    lines = [list(line) for line in lines]
    dim = len(lines)
    lines = np.array(lines)
    res = 0

    for ii in range(dim - 2):
        for jj in range(dim - 2):
            submat = lines[ii : ii + 3, jj : jj + 3]

            diag = submat.diagonal()
            diag = "".join(diag)
            antidiag = np.fliplr(submat).diagonal()
            antidiag = "".join(antidiag)

            if (diag == "MAS" or diag == "SAM") and (antidiag == "MAS" or antidiag == "SAM"):
                res += 1
                # print(submat)

    return res


### Part 1
print(solve_1(parse_input("example_2_2404.txt")))
print(solve_1(parse_input("input_2404.txt")))

### Part 2
print(solve_2(parse_input("example_2_2404.txt")))
print(solve_2(parse_input("input_2404.txt")))
