import itertools
import json

FILE_NAME = 'combination_'
COUNT = 2

faces = ["Jack", "Queen", "King", "Ace"]
suit  = ["Spades", "Hearts", "Clubs", "Diamonds"]
rank = []
for i in itertools.count(2):
    if i > 10:
        break
    rank.append(i)

rank = list(itertools.chain(rank, faces))
deck = list(itertools.product(rank,suit))

def write_combinations(count: int) -> None:
    with open(FILE_NAME + str(count) + '.json', "w", encoding="utf-8") as f:
        first = True
        for i in itertools.combinations(deck, count):
            if first:
                f.write("[\n")
                first = False
            json.dump(i, f)
            f.write(",")
        f.write("[\n")

write_combinations(COUNT)