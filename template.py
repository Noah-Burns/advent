# <LINK>
from pathlib import Path


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line and line != [""], lines))

    return lines


### Part 1
print((parse_input("example_1_yydd.txt")))
