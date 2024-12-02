from pathlib import Path
import math


def parse_input(fname: str) -> dict:
    P = Path(__file__).parent.resolve() / fname
    lines = P.read_text().split("\n")
    lines = [[int(n) for n in line.split()[1:]] for line in lines]

    return dict(zip(*lines))


def possible_victories(time: int, distance: int) -> int:
    # victory if y = time_held * (Time - time_held) > distance
    # y = -x^2 + T*x > d
    # -x^2 + T*x - d > 0

    # Calculate the discriminant
    discriminant = time**2 - 4 * distance  # b^2 - 4ac
    if discriminant <= 0:
        return 0

    # Calculate roots
    c_1 = (-time + discriminant**0.5) / -2
    c_2 = (-time - discriminant**0.5) / -2

    # return number of integers in (c_1, c_2)
    res = int(c_2) - int(c_1)
    if c_1.is_integer() or c_2.is_integer():
        res -= 1

    return res


def dict_value(input_dict: dict) -> int:
    victs = [possible_victories(t, d) for t, d in input_dict.items()]
    return math.prod(victs)


### Part 1
print(dict_value(parse_input("example_2306.txt")))

print(dict_value(parse_input("input_2306.txt")))


### Part 2
split_digit_dict = parse_input("input_2306.txt")
single_dict = {
    int("".join(str(k) for k in split_digit_dict)): int(
        "".join([str(v) for v in split_digit_dict.values()])
    )
}
print(single_dict)

print(dict_value(single_dict))
