"""Solution to Advent of Code 2018 Day 10.

--- Day 10: The Stars Align ---
It's no use; your navigation system simply isn't capable of providing walking
directions in the arctic circle, and certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue
operations will arrange points of light in the sky to guide missing Elves back
to base. Unfortunately, the message is easy to miss: the points move slowly
enough that it takes hours to align them, but have so much momentum that they
only stay aligned for a second. If you blink at the wrong time, it might be
hours before another message appears.

You can see these points of light floating in the distance, and record their
position in the sky and their velocity, the relative change in position per
second (your puzzle input). The coordinates are all given from your perspective;
given enough time, those positions and velocities will move the points into a
cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the
points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
Each line represents one point. Positions are given as <X, Y> pairs: X
represents how far left (negative) or right (positive) the point appears, while
Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's
velocity is added to its position. So, a point with velocity <1, -2> is moving
to the right, but is moving upward twice as quickly. If this point's initial
position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................
After 3 seconds, the message appeared briefly: HI. Of course, your message will
be much longer and will take many more seconds to appear.

What message will eventually appear in the sky?

--- Part Two ---
Good thing you didn't have to wait, because that would have taken a long time -
much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious:
exactly how many seconds would they have needed to wait for that message to
appear?
"""

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
  with open('input/10') as file_:
    lines = file_.readlines()

  positions = []
  velocities = []
  for line in lines:
    line = line.strip()
    line = line.replace(' ', '')
    line = line.replace('position=<', '')
    line = line.replace('velocity=<', '')
    line = line.replace('>', ',')[:-1]
    x, y, vx, vy = line.split(',')
    positions.append([int(x), int(y)])
    velocities.append([int(vx), int(vy)])
  initial_positions = np.array(positions)
  velocities = np.array(velocities)

  # Part 1.
  min_sec = -1
  min_area = 100000000000
  positions = np.copy(initial_positions)
  for i in range(20000):
    positions += velocities
    min_x, min_y = np.min(positions, axis=0)
    max_x, max_y = np.max(positions, axis=0)
    area = (max_x - min_x) * (max_y - min_y)
    if area < min_area:
      min_area = area
      min_sec = i + 1

  final_positions = initial_positions + min_sec * velocities
  # NOTE(ehotaj): as is custom in graphics programming, I believe the origin is
  # the top, left corner of the screen. So we invert y here to get the text
  # flipped right side up.
  plt.scatter(final_positions[:, 0], -final_positions[:, 1])
  plt.show()

  # Part 2.
  # NOTE(ehotaj): you must close out of the pyplot figure to continue execution.
  print('Wait time: ', min_sec)
