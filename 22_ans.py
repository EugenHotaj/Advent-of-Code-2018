"""Solution to Advent of Code 2018 Day 2 Part 2."""

def naive_find_common(data):
    for left in data:
        for right in data:
            if left == right:
                continue
            diff_len = 0
            common = []
            for l, r in zip(left, right):
                if l != r:
                    diff_len += 1
                else:
                    common.append(l)
            if diff_len == 1:
                return ''.join(common)

if __name__ == '__main__':
    with open("2_input") as file_:
        data = file_.readlines()
    common = naive_find_common(data)
    print("Common Letters:", common)



