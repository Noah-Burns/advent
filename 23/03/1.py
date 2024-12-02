# pylint: disable=missing-function-docstring

# get start and end coordinates of each number
# search all adjacent coordinates for a symbol
## by searching the rectangle of characters of the number
## and the one-character "layer" surrounding all its digits

class EngNum:
    def __init__(self, num, coords):
        self.n = num
        self.row = coords[0]
        self.start_col = coords[1]
        self.end_col = coords[2]
 

def get_number_coordinates(schem):
    res = []
    is_in_number = False
    coords = [0, 0, 0] # row, start_col, end_col
    n_str = ""

    line: str
    for ii, line in enumerate(schem):
        for jj, ch in enumerate(line):
            if is_in_number:
                if not ch.isnumeric():
                    coords[2] = jj - 1
                    res.append(EngNum(int(n_str), coords))
                    is_in_number = False
                    n_str= ""
                else:
                    n_str += ch

            else:
                if ch.isnumeric():
                    is_in_number = True
                    n_str += ch
                    coords[0] = ii
                    coords[1] = jj

    return res


def is_symbol(ch: str):
    if ch.isnumeric() or ch == '.':
        return False
    return True


def search_for_symbol(schem: str, num: EngNum):
    """Returns num.n if num is adjacent to a symbol in schem
    else zero."""

    # define the search rectangle
    start_row = num.row - 1
    end_row = num.row + 1
    start_col = num.start_col - 1
    end_col = num.end_col + 1

    # look at everything in there
    for ii in range(start_row, end_row + 1):
        for jj in range(start_col, end_col + 1):
            try:
                if is_symbol(schem[ii][jj]):
                    return num.n
            except IndexError:
                print(num.n, ii, jj)

    return 0


def dump_file(file_name, f_list):
    with open(file_name, "w", encoding="utf-8") as f:
        for item in f_list:
            f.write(f"{item}\n")


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
    
    nums = get_number_coordinates(schematic)
    res_nums = []

    for num in nums:
        p = search_for_symbol(schematic, num)
        if p:
            res_nums.append(p)
        res += p

    n_nums = [x.n for x in nums]

    dump_file("nums.txt", n_nums)
    dump_file("res_nums.txt", res_nums)

    return res

print(main("input.txt"))
