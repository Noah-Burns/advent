from pathlib import Path
from typing import Any


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")

    return lines


class Cell:
    def __init__(self, ii: int, jj: int, shape: str):
        self.ii = ii
        self.jj = jj
        self.shape = shape

        self.coords = (self.ii, self.jj)

    def __repr__(self):
        return f"Cell({self.ii}, {self.jj}, {self.shape})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented

        return self.coords == other.coords


class Step:
    def __init__(self, start: Cell, arrow: str, end: Cell):
        self.start = start
        self.end = end
        self.arrow = arrow

    def __repr__(self):
        return f"Step( {self.start} {self.arrow} {self.end} )"


def find_start(pipes: list[str]) -> Cell:
    for ii, line in enumerate(pipes):
        for jj, cell in enumerate(line):
            if cell == "S":
                return Cell(ii, jj, "S")


def get_step(pipes: list[str], start: Cell, prev: Cell = None) -> Step:
    ii, jj = start.coords

    checks_map = {
        "↑": (
            ii > 0 and start.shape in "S|JL" and pipes[ii - 1][jj] in "S|7F",
            (ii - 1, jj),
        ),
        "↓": (
            ii < len(pipes) - 1
            and start.shape in "S|7F"
            and pipes[ii + 1][jj] in "S|LJ",
            (ii + 1, jj),
        ),
        "←": (
            jj > 0 and start.shape in "S-J7" and pipes[ii][jj - 1] in "S-LF",
            (ii, jj - 1),
        ),
        "→": (
            jj < len(pipes[0]) - 1
            and start.shape in "S-LF"
            and pipes[ii][jj + 1] in "S-J7",
            (ii, jj + 1),
        ),
    }

    for direction_checking in checks_map:
        if checks_map[direction_checking][0]:
            # prospective next cell
            ii, jj = checks_map[direction_checking][1]
            next_cell = Cell(ii, jj, pipes[ii][jj])

            if not prev:
                return Step(start, direction_checking, next_cell)
            elif next_cell.coords != prev.coords:
                return Step(start, direction_checking, next_cell)
            # else keep checking

    raise ValueError("No valid next step found")


def get_first_steps(pipes: list[str]) -> tuple[Cell, list[Step]]:
    res = []
    start = find_start(pipes)

    res.append(get_step(pipes, start))
    res.append(get_step(pipes, start, prev=res[0].end))

    return start, res


def traverse_loop(pipes: list[str], return_loop=False):
    start, first_steps = get_first_steps(pipes)

    paths = ([start, first_steps[0].end]), ([start, first_steps[1].end])

    ii = 1
    while True:
        paths[0].append(get_step(pipes, paths[0][-1], prev=paths[0][-2]).end)
        paths[1].append(get_step(pipes, paths[1][-1], prev=paths[1][-2]).end)

        if paths[0][-1] == paths[1][-1]:
            # if the paths just stepped onto the same cell
            if return_loop:
                return paths
            return ii + 1

        if paths[0][-1] == paths[1][-2]:
            # if the paths just swapped between the same two cells
            if return_loop:
                return paths
            return ii

        ii += 1


### Part 1
print(traverse_loop(parse_input("example_2310.txt")))
print(traverse_loop(parse_input("input_2310.txt")))


### Part 2
# Instead of |-FJL7, replace the loop pipes with up, down, left, or right arrows pointing to the next pipe in the loop.
# Then, for a cell to be in the loop, it must have an odd number of arrows between it and the edge of the grid
# in each direction.
# But we only ever have to count in one of the four directions, since if the loop is closed,
# one of the four directions being valid => all four are.


def replace_cell(pipes: list[str], cell: Cell, new_shape: str) -> list[str]:
    new_row = list(pipes[cell.ii])
    new_row[cell.jj] = new_shape
    pipes[cell.ii] = "".join(new_row)

    return pipes


def arrowify_pipes(pipes: list[str]) -> list[list[str]]:
    # remove all pipes not in the loop
    loop_cells = traverse_loop(pipes, return_loop=True)
    loop_cells = loop_cells[0] + loop_cells[1]
    loop_coords = [cell.coords for cell in loop_cells]

    for ii, line in enumerate(pipes):
        for jj, _ in enumerate(line):
            if (ii, jj) not in loop_coords:
                pipes = replace_cell(pipes, Cell(ii, jj, ""), ".")

    # Traverse the loop and replace with arrows
    start, first_steps = get_first_steps(pipes)
    first_step = first_steps[0]
    current_cell = first_step.end

    while True:
        print(current_cell)
        for row in pipes:
            print(row)

        step = get_step(pipes, current_cell)
        pipes = replace_cell(pipes, current_cell, step.arrow)
        current_cell = step.end

        if current_cell.coords == start.coords:
            return pipes


def is_cell_inside(pipes: list[str], cell: tuple[int]) -> bool:
    n_pipes = 0

    for cell_in_row in pipes[cell[0]][: cell[1]]:
        if cell_in_row in "↑↓←→":
            n_pipes += 1

    return bool(n_pipes % 2)


def count_area_inside_loop(pipes: list[str]) -> int:
    pipes = arrowify_pipes(pipes)

    # count the inside cells
    res = 0

    for ii, line in enumerate(pipes):
        for jj, cell in enumerate(line):
            if cell == "." and is_cell_inside(pipes, (ii, jj)):
                pipes = replace_cell(pipes, Cell(ii, jj, ""), "X")
                res += 1

    return res


print(count_area_inside_loop(parse_input("example2_2310.txt")))
print(count_area_inside_loop(parse_input("example3_2310.txt")))
# print(traverse_loop(parse_input("input_2310.txt")))
