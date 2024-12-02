# pylint: disable=missing-function-docstring

def point_value(line: str):
    wins_picks_list = line.split("|")
    wins = wins_picks_list[0].split(":")[1].split()
    picks = wins_picks_list[1].split()
    wins = [win.strip() for win in wins]
    picks = [pick.strip() for pick in picks]
    
    hits = 0
    for pick in picks:
        if pick in wins:
            hits += 1

    return int(max(0, 2**(hits - 1)))


def main(file_name):
    res = 0
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    for line in lines:
        res += point_value(line)
    
    return res


print(main("input.txt"))
