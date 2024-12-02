# pylint: disable=missing-function-docstring

BAG = {"red": 12, "green": 13, "blue": 14}

def is_draw_possible(draw_str: str):
    colors = draw_str.split(",")
    colors = [color.strip() for color in colors]

    for draw in colors:
        draw_list = draw.split(" ")
        draw_number = int(draw_list[0])
        draw_color = draw_list[1]

        if draw_number > BAG[draw_color]:
            return False

    return True


def is_game_possible(line_str: str):
    """Returns game ID if the game is possible, 0 if impossible"""

    id_game_list = line_str.split(":")
    id_list = id_game_list[0].split(" ")
    id = int(id_list[1])

    game_list = id_game_list[1].split(";")

    for draw in game_list:
        if not is_draw_possible(draw):
            return 0

    return id


def main(file_name):
    res = 0

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            res += is_game_possible(line)

    return res

print(main("input.txt"))
