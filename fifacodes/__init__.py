import csv
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable, Generator, Iterator, NamedTuple

from rapidfuzz import process

__version__ = "0.1.2"

_DATA_PATH = Path(__file__).parent
_DEFAULT_DATA_PATH = _DATA_PATH / "default.csv"
_CUSTOM_DATA_PATH = _DATA_PATH / "custom.csv"


class Member(NamedTuple):
    code: str
    name: str


_DataTypes = dict[str, Member]


class Members(Mapping[str, Member]):
    """
    A mapping of FIFA member codes to member names.

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
            member = Member(code=code, name=name)

            default_data[code] = member

            data[code] = member
            data[name] = member

        for code, name in self._read_csv(_CUSTOM_DATA_PATH):
            member = data[code]
            data[name] = member

        return default_data, data

    def __getitem__(self, key: str) -> Member:
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
        case_sensitive: bool = False,
    ) -> list[Member]:
        """
        Search for a member by name or code.

        The search uses fuzzy string matching to find potential results.

        Args:
            key: The search query.
            limit: The maximum number of results to return. Defaults to 3.
            score_cutoff: The minimum score for a result to be returned.
                Defaults to 60.
            case_sensitive: Whether to perform a case-sensitive search.
                Defaults to False.

        Returns:
            A list of potential results.
        """
        processor: Callable[[str], str] | None = (
            None if case_sensitive else lambda x: x.lower()
        )
        results = process.extract(
            key,
            self._data.keys(),
            limit=limit,
            processor=processor,
            score_cutoff=score_cutoff,
        )
        return list({self._data[result[0]]: None for result in results})

    def search_one(self, key: str) -> Member | None:
        """
        Search for a member by name or code and return the first result.
        """
        try:
            return self.search(key, limit=1)[0]
        except IndexError:
            return None


__all__ = ("Members", "Member")
