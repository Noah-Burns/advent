from pathlib import Path

# Card precedence
# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2

CARD_RANK = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def most_common_card(hand: str) -> str:
    return max(set(hand), key=hand.count)


def rank_hand(hand: str, jokers: bool = False) -> int:
    # Hand values, first digit:
    # 1 - high card
    # 2 - one pair
    # 3 - two pairs
    # 4 - three of a kind
    # 5 - full house
    # 6 - four of a kind
    # 7 - five of a kind

    if jokers:
        remaining_hand = hand.replace("J", "")

        if remaining_hand:
            hand = hand.replace("J", most_common_card(remaining_hand))

    if len(set(hand)) == 1:
        # if there is only one unique card in the hand
        return 7

    cards_frequency = {card: hand.count(card) for card in hand}

    if len(set(hand)) == 2:
        # if there are two unique cards in the hand

        if min(cards_frequency.values()) == 1:
            # if it's 4 and 1
            return 6

        # else it's 3 and 2
        return 5

    if 3 in cards_frequency.values():
        # if there's three of a kind
        return 4

    if 2 in cards_frequency.values():
        # if there's a pair

        if list(cards_frequency.values()).count(2) == 2:
            # if there's two pairs
            return 3

        # else one pair
        return 2

    # else high card
    return 1


def score_hand(hand: str, jokers: bool = False) -> int:
    # 11 or 12-digit number
    # first digit or two: rank
    # then 10 digits of card precendes for each card of the hand

    return rank_hand(hand, jokers) * 10**10 + sum(
        CARD_RANK[card] * 100**i for i, card in enumerate(hand[::-1])
    )


def get_total_winnings(bids: dict[str, int], jokers: bool = False) -> int:
    def score_hand_wrapper(hand: str) -> int:
        return score_hand(hand, jokers)

    hands = bids.keys()
    hands = sorted(hands, key=score_hand_wrapper)

    # for ii, hand in enumerate(hands):
    #     print(f"{ii}\t{hand}\t{score_hand(hand)}")

    return sum(ii * bids[hand] for ii, hand in enumerate(hands, start=1))


def parse_input(fname: str) -> dict[str, int]:
    P = Path(__file__).parent.resolve() / fname
    lines = P.read_text().split("\n")
    lines = [line.split() for line in lines]

    return {line[0]: int(line[1]) for line in lines}


### Part 1
print(get_total_winnings(parse_input("example_2307.txt")))
print(get_total_winnings(parse_input("input_2307.txt")))


### Part 2
CARD_RANK["J"] = 1
print(get_total_winnings(parse_input("example_2307.txt"), jokers=True))
print(get_total_winnings(parse_input("input_2307.txt"), jokers=True))
