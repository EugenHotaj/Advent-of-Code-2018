r"""Solution to Advent of Code 2018 Day 13.

--- Day 13: Mine Cart Madness ---
A crop of this size requires significant logistics to transport produce, soil,
fertilizer, and so on. The Elves are very busy pushing things around in carts on
some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for
another 1000 years, the Elves seem to be making this up as they go along. They
haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections
(+). Curves connect exactly two perpendicular pieces of track; for example, this
is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a
cart is capable of turning left, turning right, or continuing straight. Here are
two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v),
left (<), or right (>). (On your initial map, the track under each cart is a
straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it
turns left the first time, goes straight the second time, turns right the third
time, and then repeats those directions starting again with left the fourth
time, straight the fifth time, and so on. This process is independent of the
particular intersection at which the cart has arrived - that is, the cart has no
per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a
time. They do this based on their current location: carts on the top row move
first (acting from left to right), then carts on the second row move (again from
left to right), then carts on the third row, and so on. Once each cart has moved
one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square.
Second, the bottom cart moves. It is facing up (^), so it moves up one square.
Because all carts have moved, the first tick ends. Then, the process repeats,
starting with the first cart. The first cart moves down, then the second cart
moves up - right into the first cart, colliding with it! (The location of the
crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/
After following their respective paths for a while, the carts eventually crash.
To help prevent crashes, you'd like to know the location of the first crash.
Locations are given in X,Y coordinates, where the furthest left column is X=0
and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/
In this example, the location of the first crash is 7,3.

--- Part Two ---
There isn't much you can do to prevent crashes in this ridiculous system.
However, by predicting the crashes, the Elves know where to be in advance and
instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out
of carts. It could be useful to figure out where the last cart that hasn't
crashed will end up.

For example:

/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\
|   |
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\
|   |
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\
|   |
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/
After four very expensive crashes, a tick ends with only one cart remaining; its
final location is 6,4.

What is the location of the last cart at the end of the first tick where it is
the only cart left?
"""

import copy

import numpy as np

DIRECTION_TO_VELOCITY = {
    '>': np.array([0, 1]),
    '^': np.array([-1, 0]),
    '<': np.array([0, -1]),
    'v': np.array([1, 0]),
}
ROTATE = {
    '>': { 'l': '^', 's': '>', 'r': 'v' },
    '^': { 'l': '<', 's': '^', 'r': '>' },
    '<': { 'l': 'v', 's': '<', 'r': '^' },
    'v': { 'l': '>', 's': 'v', 'r': '<' },
}
NEXT_ROTATION = {'l': 's', 's': 'r', 'r': 'l'}
CORNER = {
    '>': { '/': '^', '\\': 'v' },
    '^': { '/': '>', '\\': '<' },
    '<': { '/': 'v', '\\': '^' },
    'v': { '/': '<', '\\': '>' },
}


class Minecart(object):
    def __init__(self, row, col, direction, next_rotation):
        self._direction = direction
        self._next_rotation = next_rotation
        self.pos = np.array((row, col))
        self.alive = True

    @property
    def vel(self):
        return DIRECTION_TO_VELOCITY[self._direction]

    def rotate(self):
        self._direction = ROTATE[self._direction][self._next_rotation]
        self._next_rotation = NEXT_ROTATION[self._next_rotation]

    def corner(self, corner):
        self._direction = CORNER[self._direction][corner]


def parse_minecarts(tracks, direction, under):
    locs = np.where(tracks == direction)
    minecarts = [Minecart(row, col, direction, 'l') for row, col in zip(*locs)]
    tracks[locs] = under
    return minecarts


def tick(tracks, minecarts):
    minecarts = sorted(minecarts, key=lambda minecart: tuple(minecart.pos))
    collisions = []
    for i, minecart in enumerate(minecarts):
        if not minecart.alive:
            continue
        track = tracks[minecart.pos[0], minecart.pos[1]]
        if track == '+':
            minecart.rotate()
        elif track == '/' or track == '\\':
            minecart.corner(track)
        minecart.pos += minecart.vel
        for j, other in enumerate(minecarts):
            if i != j and np.all(minecart.pos == other.pos):
                collisions.append(minecart.pos)
                minecart.alive = False
                other.alive = False
    return collisions


if __name__ == '__main__':
    with open('input/13') as file_:
        lines = file_.readlines()
    tracks = np.array([list(line)[:-1] for line in lines])
    initial_minecarts = []
    initial_minecarts = parse_minecarts(tracks, '>', '-')
    initial_minecarts += parse_minecarts(tracks, '^', '|')
    initial_minecarts += parse_minecarts(tracks, '<', '-')
    initial_minecarts += parse_minecarts(tracks, 'v', '|')

    # Part 1.
    minecarts = copy.deepcopy(initial_minecarts)
    collisions = []
    while not collisions:
        collisions = tick(tracks, minecarts)
    collision = collisions[0]
    print("First collision at:", (collision[1], collision[0]))

    # Part 2.
    minecarts = copy.deepcopy(initial_minecarts)
    while len(minecarts) > 1:
        tick(tracks, minecarts)
        minecarts = [m for m in minecarts if m.alive]
    survivor = minecarts[0]
    print("Last minecart at:", (survivor.pos[1], survivor.pos[0]))
