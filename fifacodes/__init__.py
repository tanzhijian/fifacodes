import csv
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Generator, Iterator, NamedTuple

_DATA_PATH = Path(__file__).parent
_DEFAULT_DATA_PATH = _DATA_PATH / "default.csv"
_CUSTOM_DATA_PATH = _DATA_PATH / "custom.csv"


class Country(NamedTuple):
    code: str
    name: str


_DataTypes = dict[str, Country]


class Counties(Mapping[str, Country]):
    def __init__(self) -> None:
        self.data = self._read_data()

    def _read_csv(self, path: Path) -> Generator[tuple[str, str], Any, None]:
        with open(path) as f:
            reader = csv.reader(f)
            next(reader)
            for code, name in reader:
                yield code, name

    def _read_data(self) -> _DataTypes:
        data: _DataTypes = {}
        for code, name in self._read_csv(_DEFAULT_DATA_PATH):
            country = Country(code=code, name=name)
            data[code] = country
            data[name] = country

        for code, name in self._read_csv(_CUSTOM_DATA_PATH):
            country = data[code]
            data[name] = country

        return data

    def __getitem__(self, key: str) -> Country:
        return self.data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)


__all__ = ("Counties", "Country")
