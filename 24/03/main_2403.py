# https://adventofcode.com/2024/day/3
from pathlib import Path
import re


def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    return input_file.read_text()


def p_str(s):
    subs = re.findall(r"mul\(\d+,\d+\)", s)

    res = 0

    for sub in subs:
        digits = re.findall(r"\d+", sub)
        res += int(digits[0]) * int(digits[1])

    return res


def p_2(s):
    subs = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", s)
    is_enabled = True

    res = 0

    for sub in subs:
        if sub == "do()":
            is_enabled = True
        elif sub == "don't()":
            is_enabled = False
        else:
            if is_enabled:
                digits = re.findall(r"\d+", sub)
                res += int(digits[0]) * int(digits[1])

    return res


### Part 1
print(p_str(parse_input("example_1_2403.txt")))
print(p_str(parse_input("input_2403.txt")))

### Part 2
print(p_2(parse_input("example_2_2403.txt")))
print(p_2(parse_input("input_2403.txt")))
