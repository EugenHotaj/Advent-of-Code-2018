"""Solution to Advent of Code 2018 Day 6.

--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like
you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal
interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they
places it thinks are safe or dangerous? It recommends you check manual page 729.
The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the
coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by
counting the number of integer X,Y locations that are closest to that coordinate
(and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For
example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting
0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions.
Using the Manhattan distance, each location's closest coordinate can be
determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they
don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while
not shown here, their areas extend forever outside the visible grid. However,
the areas of coordinates D and E are finite: D is closest to 9 locations, and E
is closest to 17 (both including the coordinate's location itself). Therefore,
in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try
to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the
coordinates to be less than 32. For each location, add up the distances to all
of the given coordinates; if the total of those distances is less than 32, that
location is within the desired region. Using the same coordinates as above, the
resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle
of the region. Its calculation is as follows, where abs() is the absolute value
function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location
is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though,
instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total
distance to all given coordinates of less than 10000?
"""

import itertools

import numpy as np
from scipy import spatial
from sklearn.metrics import pairwise

if __name__ == '__main__':
  with open('input/06') as file_:
    lines = file_.read().strip().split('\n')
    points = [line.split(', ') for line in lines]
    points = [[int(point[0]), int(point[1])] for point in points]
    points = np.vstack(points)

  # Part 1.
  areas = np.zeros(len(points))
  x, y = np.min(points, axis=0)
  width, height = np.max(points, axis=0)
  # TODO(eugenhotaj): this can be vectorized to be faster; seems tedious.
  for i in range(x, width):
    for j in range(x, height):
      distances = pairwise.manhattan_distances(points, [[i, j]])
      min_dist = np.min(distances)
      # Discard equidistant points from the area accumulation.
      if len(distances[distances <= min_dist]) == 1:
        idx = np.argmin(distances)
        areas[idx] += 1

  # Discard the convex hull since these points will have infinite area.
  convex_hull = spatial.ConvexHull(points)
  interior = list(set(range(len(points))) - set(convex_hull.vertices))
  interior_areas = areas[interior]

  max_area = np.max(interior_areas)
  print('Largest non-infinite area: ', max_area)

  # Part 2.
  grid = np.array(list(itertools.product(range(x, width), range(y, height))))
  distances = pairwise.manhattan_distances(grid, points)
  distances = np.sum(distances, axis=1)

  region = len(distances[distances < 10000])
  print('Safest region area:', region)
