import sys

import numpy as np

from read_datasets import read_datasets
from solver import NearestN, TwoOpt

result = lambda a, b, c: True if b > c else False

format_str = """Name: {name}
\tVanila: {a}
\tNN: {b}
\t2opt: {c}
"""

stats_str = """{name} & {max} & {min} & {mean} & {std} \\\ """


def main():
  datasets = read_datasets()

  for dataset in datasets:
    results = []
    for i in range(5):
      print(i, file=sys.stderr)
      nn = NearestN(dataset)
      a = nn.set_total_dist()
      nn.solve()
      b = nn.dist
      opt = TwoOpt(dataset, nn)
      opt.solve()
      c = opt.dist
      results.append(c)
    print(stats_str.format(name=dataset.name, max=np.max(results), min=np.min(results), mean=np.mean(results),
                           std=np.std(results)))
    # assert result(a, b, c), "Not Correct!!"


if __name__ == '__main__':
  main()
