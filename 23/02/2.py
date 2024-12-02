# pylint: disable=missing-function-docstring

COLOR_MAP = {"red": 0, "green": 1, "blue": 2}

def min_rgbs(game_str):
    res = [0, 0, 0] # rgb

    id_game = game_str.split(":")
    draws = id_game[1].split(";")

    for draw in draws:
        draw_colors = draw.split(",")
        draw_colors = [color.strip() for color in draw_colors]

        for draw_color in draw_colors:
            dc_list = draw_color.split(" ")
            n_drawn = int(dc_list[0])
            color = COLOR_MAP[dc_list[1]] # index

            res[color] = max(res[color], n_drawn)

    return res


def main(file_name):
    res = 0

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line_val = 1
            line_mins = min_rgbs(line)

            for this_min in line_mins:
                line_val *= this_min

            res += line_val

    return res

print(main("input.txt"))
