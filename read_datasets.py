from collections import namedtuple

datasets = ["ch130", "eil51", "kroA100", "kroA200", "lin318", "pr76", "rat99", "rat195", "tsp225", "u159"]
Coord = namedtuple('Coord', ['X', 'Y'])


def read_datasets():
  _datasets = []
  for dataset in datasets:
    _datasets.append(TSPDataSet(dataset))
  return _datasets


class TSPDataSet:

  def __init__(self, name, debug=False):
    self.name = name
    self.dim, self.coords = self._read_dataset(name)
    if debug:
      print("{name}: (dim:{dim}) == (len(Coords) = {len})".format(
          name=self.name, dim=self.dim, len=len(self.coords)))
      print(self.coords)

  @staticmethod
  def _read_dataset(name):
    dim = 0
    is_start_coord = False
    coords = []
    with open("./datasets/{0}.tsp".format(name)) as f:
      for line in f.readlines():
        _str = line.split()
        if _str[0] == 'EOF':
          break
        if _str[0] == "DIMENSION":
          dim = int(_str[2])
        if _str[0] == "NODE_COORD_SECTION":
          is_start_coord = True
        elif is_start_coord:
          coords.append(
              Coord(float(_str[1]), float(_str[2])))
    assert dim != 0, "dim must not be 0"
    assert dim == len(coords), "dim must be len(coords)"
    return dim, coords


if __name__ == '__main__':
  for i, dataset in enumerate(datasets):
    print(i, dataset)
    tsp = TSPDataSet(dataset)
