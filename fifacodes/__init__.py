import csv
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Generator, Iterator, NamedTuple

from rapidfuzz import process

_DATA_PATH = Path(__file__).parent
_DEFAULT_DATA_PATH = _DATA_PATH / "default.csv"
_CUSTOM_DATA_PATH = _DATA_PATH / "custom.csv"


class Country(NamedTuple):
    code: str
    name: str


_DataTypes = dict[str, Country]


class Counties(Mapping[str, Country]):
    """
    A mapping of FIFA country codes to country names.

    The default data is sourced from Wikipedia.
    """

    def __init__(self) -> None:
        self._default_data, self._data = self._read_data()

    def _read_csv(self, path: Path) -> Generator[tuple[str, str], Any, None]:
        with open(path) as f:
            reader = csv.reader(f)
            next(reader)
            for code, name in reader:
                yield code, name

    def _read_data(self) -> tuple[_DataTypes, _DataTypes]:
        default_data: _DataTypes = {}
        data: _DataTypes = {}
        for code, name in self._read_csv(_DEFAULT_DATA_PATH):
            country = Country(code=code, name=name)

            default_data[code] = country

            data[code] = country
            data[name] = country

        for code, name in self._read_csv(_CUSTOM_DATA_PATH):
            country = data[code]
            data[name] = country

        return default_data, data

    def __getitem__(self, key: str) -> Country:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._default_data)

    def __len__(self) -> int:
        return len(self._default_data)

    def search(
        self,
        key: str,
        *,
        limit: int = 3,
        score_cutoff: int | float = 60,
    ) -> list[Country]:
        """
        Search for a country by name or code.

        The search uses fuzzy string matching to find potential results.

        Args:
            key: The search query.
            limit: The maximum number of results to return. Defaults to 3.
            score_cutoff: The minimum score for a result to be returned.
                Defaults to 60.

        Returns:
            A list of potential results.
        """
        results = process.extract(
            key, self._data.keys(), limit=limit, score_cutoff=score_cutoff
        )
        return [self._data[result[0]] for result in results]

    def search_one(self, key: str) -> Country | None:
        """
        Search for a country by name or code and return the first result.
        """
        try:
            return self.search(key, limit=1)[0]
        except IndexError:
            return None


__all__ = ("Counties", "Country")
