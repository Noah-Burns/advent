from pathlib import Path


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line and line != [""], lines))
    lines = [[int(entry) for entry in line] for line in lines]

    list_1 = [line[0] for line in lines]
    list_2 = [line[1] for line in lines]

    return list_1, list_2


def compare_lists(list_1, list_2):
    list_1 = sorted(list_1)
    list_2 = sorted(list_2)

    diffs = []

    for entry_1, entry_2 in zip(list_1, list_2):
        diffs.append(abs(entry_1 - entry_2))

    return sum(diffs)


def get_score(list_1, list_2):
    list_1 = sorted(list_1)
    list_2 = sorted(list_2)

    res = 0

    for entry in list_1:
        res += entry * list_2.count(entry)

    return res


### Part 1
print(compare_lists(*parse_input("example_2401.txt")))
print(compare_lists(*parse_input("input_2401.txt")))

### Part 2
print(get_score(*parse_input("example_2401.txt")))
print(get_score(*parse_input("input_2401.txt")))
