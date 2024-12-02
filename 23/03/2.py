# pylint: disable=missing-function-docstring

# get start and end coordinates of each number
# search all adjacent coordinates for a symbol
## by searching the rectangle of characters of the number
## and the one-character "layer" surrounding all its digits 


def get_full_num(schem, row, col):
    start_col = 0
    end_col = 0

    jj = col
    while True:
        jj -= 1
        if not schem[row][jj].isnumeric():
            start_col = jj + 1
            break

    jj = col
    while True:
        jj += 1
        if not schem[row][jj].isnumeric():
            end_col = jj - 1
            break

    return int(schem[row][start_col:end_col + 1])


def is_gear(schem, row, col):
    """Returns [is_gear: bool, ratio: int]"""
    adjacent_nums = 0
    ratio = 1

    for ii in range(row - 1, row + 2):
        is_in_num = False

        for jj in range(col - 1, col + 2):
            ch = schem[ii][jj]

            if is_in_num:
                if not ch.isnumeric():
                    is_in_num = False
            else:
                if ch.isnumeric():
                    is_in_num = True
                    adjacent_nums += 1
                    ratio *= get_full_num(schem, ii, jj)

    return [adjacent_nums == 2, ratio]


def get_gear_ratios(schem):
    res = 0

    line: str
    for ii, line in enumerate(schem):
        for jj, ch in enumerate(line):
            
            if ch == "*":
                gear_check = is_gear(schem, ii, jj)
                if gear_check[0]:
                    res += gear_check[1]

    return res


def wrap_schem(schem: list):
    res = schem
    line_len = len(schem[0])
    
    res.insert(0, "."*line_len)
    res.append("."*line_len)

    res = [f".{line}." for line in res]

    return res


def main(file_name):
    res = 0
    with open(file_name, "r", encoding="utf-8") as f:
        schematic = f.read().splitlines()

    schematic = wrap_schem(schematic)
    
    return get_gear_ratios(schematic)


print(main("input.txt"))
