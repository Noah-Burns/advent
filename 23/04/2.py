# pylint: disable=missing-function-docstring

class Card:
    def __init__(self, line: str):
        wins_picks_list = line.split("|")
        idx_wins_list = wins_picks_list[0].split(":")

        idx_str = idx_wins_list[0].split()[-1]
        wins_list = wins_picks_list[0].split(":")[1].split()
        picks_list = wins_picks_list[1].split()

        self.idx = int(idx_str)
        self.wins = [w.strip() for w in wins_list]
        self.picks = [p.strip() for p in picks_list]

    def hits(self):
        res = 0

        for pick in self.picks:
            if pick in self.wins:
                res += 1

        return res


def main(file_name):
    res = 0
    with open(file_name, "r", encoding="utf-8") as f:
        deck = [Card(line) for line in f.read().splitlines()]  

    orig_deck = deck.copy()

    while deck:
        res += 1
        this_card = deck.pop(0)

        won_cards = orig_deck[
            this_card.idx : this_card.idx + this_card.hits()]

        if won_cards:
            deck += won_cards

        print(len(deck))

    return res


print(main("input.txt"))
