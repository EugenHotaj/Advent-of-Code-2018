"""Solution for Advent of Code Day 5 Part 1."""

import copy


def react(polymer):
  polymer = [c for c in polymer]
  size = len(polymer)
  i = 0
  while i < size - 1:
    if abs(ord(polymer[i]) - ord(polymer[i + 1])) == 32:
      del polymer[i], polymer[i]  # Delete current character and next character.
      i -= 2
      size -= 2
    i += 1
  return polymer


if __name__ == '__main__':
  with open('input') as file_:
    data = file_.read().strip()

  # Part 1.
  print('Reacted polymer length: ', len(react(data)))

  # Part 2.
  shortest_len = 1000000
  for i in range(65, 65 + 26):
    lower = chr(i)
    upper = chr(i + 32)
    stripped = data.replace(lower, '').replace(upper, '')
    reacted_len = len(react(stripped))
    if reacted_len < shortest_len:
      shortest_len = reacted_len
  print('Shortest stripped, reacted polymer:', shortest_len)
