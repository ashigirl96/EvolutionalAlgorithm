from abc import ABCMeta, abstractmethod
from random import randint

import nmath
from read_datasets import TSPDataSet


class Solver(metaclass=ABCMeta):
  def __init__(self, dataset: TSPDataSet):
    self.dataset = dataset
    self.dim = self.dataset.dim
    self.tour = []
    self.dist = 0

  @abstractmethod
  def solve(self):
    pass

  def set_total_dist(self, visited=None):
    if not visited:
      self.dist = 0
      for v in range(1, self.dataset.dim):
        self.dist += nmath.dist(self.dataset.coords[v - 1], self.dataset.coords[v])
    return self.dist

  def visited_total_dist(self, visited):
    dist = 0
    for v in range(1, self.dim):
      v1 = visited[v - 1]
      v2 = visited[v]
      dist += nmath.dist(self.dataset.coords[v1], self.dataset.coords[v2])
    return dist


class NearestN(Solver):

  def __init__(self, dataset: TSPDataSet):
    super().__init__(dataset)
    self.never_visited = list(range(0, self.dim))
    self.visited = []

  def solve(self):
    self.dist = 0
    nearest_city = None
    last_city = randint(0, self.dim)
    self.never_visited.remove(last_city)
    while self.never_visited:
      nearest_city_dist = 10000000000
      for v in self.never_visited:
        length = nmath.dist(self.dataset.coords[last_city],
                            self.dataset.coords[v])
        if length < nearest_city_dist:
          nearest_city = v
          nearest_city_dist = length
      self.dist += nearest_city_dist
      self.visited.append(last_city)
      if last_city in self.never_visited:
        self.never_visited.remove(last_city)
      assert nearest_city is not None, "nearest_city must be not None."
      last_city = nearest_city


class TwoOpt(Solver):

  def __init__(self, dataset: TSPDataSet, nn: NearestN):
    super().__init__(dataset)
    self.nn = nn
    self.dist = self.nn.dist
    self.visited = self.nn.visited

  def solve(self):
    visited = self._improve(self.visited)
    while visited != self.nn.visited:
      self.visited = visited
      visited = self._improve(self.visited)

  def _improve(self, visited):
    for i in range(0, self.dim - 1):
      for j in map(self._l, range(i + 2, i + self.dim - 1)):
        j1 = self._l(j + 1)
        # print(i, i + 1, "|", j, j1)
        _tmp_visited = visited
        if i + 1 < j:
          _tmp_visited[i + 1:j + 1] = reversed(_tmp_visited[i + 1:j + 1])
        else:
          _tmp = 2 * _tmp_visited
          J = j1 + self.dim
          _tmp[i + 1:J] = reversed(_tmp[i + 1:J])
          _tmp_visited = _tmp[:self.dim]
          _tmp_visited[0:j1 + 1] = _tmp[self.dim:J + 1]
        _total_dist = self.visited_total_dist(_tmp_visited)
        if _total_dist < self.dist:
          self.dist = _total_dist
          visited = _tmp_visited
    return visited

  def _l(self, j):
    return j % self.dim
