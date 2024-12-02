# pylint: disable=missing-function-docstring
# pylint: disable=consider-using-enumerate

DIGIT_MAP = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9"
}


def is_digit_str_start(line_str: str):
    res = (0, 0)
    possibilities = set(DIGIT_MAP.keys())

    for poss in possibilities:
        if line_str.startswith(poss):
            return (DIGIT_MAP[poss], len(poss))

    return res


def get_digits(line_str: str):
    first_digit = "0"
    last_digit = "0"

    for ii in range(len(line_str)):
        ch = line_str[ii]

        if int(last_digit) and not int(first_digit):
            first_digit = last_digit

        if ch.isnumeric():
            last_digit = ch
            ii += 1
            continue

        digit, skip_chrs = is_digit_str_start(line_str[ii:])
        if digit:
            last_digit = digit
            ii += skip_chrs
            continue

        ii += 1

    return first_digit + last_digit


def dump_line(line_str, digits):
    with open("line_dump.txt", "a", encoding="utf-8") as f:
        f.write(f"{line_str.strip()} {digits}\n")


def main(file_name):
    res = 0
    with open("line_dump.txt", "w", encoding="utf-8") as f:
        pass

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            digits = get_digits(line)     
            dump_line(line, digits)
            res += int(digits)

    return res

print(main("input.txt"))
