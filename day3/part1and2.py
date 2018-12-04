"""Solution to Advent of Code 2018 Day 3 Part 1 and 2."""

import numpy as np

if __name__ == '__main__':
  cloth = np.zeros((1000, 1000))
  claims = []
  with open('input') as file_:
    lines = file_.readlines()
    for line in lines:
      _, _, loc, size = line.split()
      x, y = [int(t) for t in loc[:-1].split(',')]  # Remove token then split.
      w, h = [int(t) for t in size.split('x')]
      claims.append((x, y, w, h))
      cloth[x:x + w, y:y + h] += 1

  # Part 1.
  overlap = len(cloth[cloth > 1])
  print('Overlapping Area (in^2):', overlap)

  # Part 2.
  for i, claim in enumerate(claims):
    x, y, w, h = claim
    area = w * h
    if np.sum(cloth[x:x + w, y:y + h]) == area:
      print('Intact Claim #:', i + 1)
