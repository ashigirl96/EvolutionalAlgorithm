from read_datasets import read_datasets
from solver import NearestN, TwoOpt

result = lambda a, b, c: True if b > c else False

format_str = """Name: {name}
\tVanila: {a}
\tNN: {b}
\t2opt: {c}
"""


def main():
  datasets = read_datasets()

  for dataset in datasets:
    nn = NearestN(dataset)
    a = nn.set_total_dist()
    nn.solve()
    b = nn.dist
    opt = TwoOpt(dataset, nn)
    opt.solve()
    c = opt.dist
    print(format_str.format(name=dataset.name, a=a, b=b, c=c))
    assert result(a, b, c), "Not Correct!!"


if __name__ == '__main__':
  main()
