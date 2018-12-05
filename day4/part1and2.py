"""Solution to Advent of Code 2018 Day 4 Part 1 and 2."""

import collections

import numpy as np


def process_timestamp(string_timestamp):
  return int(string_timestamp[-3:-1])


if __name__ == '__main__':
  guards = collections.defaultdict(lambda: np.zeros(60))
  with open('input') as file_:
    lines = file_.readlines()
  lines = sorted(lines)

  guard_id = None
  asleep = None
  for line in lines:
    tokens = line.split()
    if len(tokens) == 6:  # New guard begins shift.
      _, _, _, guard_id, _, _ = tokens
      guard_id = int(guard_id[1:])
      asleep = None
    else:
      _, timestamp, _, action = tokens
      timestamp = process_timestamp(timestamp)
      if action == 'asleep':
        asleep = timestamp
      elif action == 'up':
        guards[guard_id][asleep:timestamp] += 1

  guards = dict(guards)
  guard_ids = []
  shifts = []
  for guard_id, shift in guards.items():
    guard_ids.append(guard_id)
    shifts.append(shift)

  shifts = np.vstack(shifts)

  # Part 1.
  most_asleep = np.argmax(np.sum(shifts, axis=1))
  most_asleep_id = guard_ids[most_asleep]
  most_asleep_minute = np.argmax(shifts[most_asleep])
  print('Guard most asleep id x minute most asleep:',
        most_asleep_id * most_asleep_minute)

  # Part 2.
  most_asleep = np.argmax(np.max(shifts, axis=1))
  most_asleep_id = guard_ids[most_asleep]
  most_asleep_minute = np.argmax(shifts[most_asleep])
  print('Guard most asleep id x minute most asleep:',
        most_asleep_id * most_asleep_minute)
