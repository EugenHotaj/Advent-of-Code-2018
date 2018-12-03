"""Solution to Advent of Code 2018 Day 2 Part 1."""

def check(line):
    freq = {}
    for c in line:
       freq[c] = line.count(c)

    counts = freq.values()
    two = 1 if 2 in counts else 0
    three = 1 if 3 in counts else 0

    return two, three


if __name__ == '__main__':
    with open("input") as file_:
        data = file_.readlines()
    data = [check(line) for line in data]
    twos = 0
    threes = 0
    for two, three in data:
        twos += two
        threes += three
    print("Checksum:", twos * threes)



