from pathlib import Path


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line and line != [""], lines))
    lines = [[int(el) for el in line] for line in lines]

    return lines


def is_safe(line):
    if line != sorted(line) and list(reversed(line)) != sorted(line):
        return False

    for ii, el in enumerate(line[:-1]):
        if abs(el - line[ii + 1]) > 3 or abs(el - line[ii + 1]) == 0:
            return False

    return True


def is_safe_r(line):
    for ii, el in enumerate(line):
        if is_safe(line[:ii] + line[ii + 1 :]):
            return True

    return False


def eval_lines(lines):
    res = 0

    for line in lines:
        if is_safe(line):
            res += 1

    return res


def eval_lines_r(lines):
    res = 0

    for line in lines:
        if is_safe_r(line):
            res += 1
    return res


### Part 1
print(eval_lines(parse_input("example_2402.txt")))
print(eval_lines(parse_input("input_2402.txt")))

### Part 2
print(eval_lines_r(parse_input("example_2402.txt")))
print(eval_lines_r(parse_input("input_2402.txt")))
