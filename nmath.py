from read_datasets import Coord


def dist(c1: Coord, c2: Coord):
  x = c2.X - c1.X
  y = c2.Y - c1.Y
  return int(x ** 2 + y ** 2 + 0.5)
