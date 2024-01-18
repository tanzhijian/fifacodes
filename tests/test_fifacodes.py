import pytest

from fifacodes import Countries


class TestCountries:
    @pytest.fixture(scope="class")
    def countries(self) -> Countries:
        return Countries()

    def test_read_data(self, countries: Countries) -> None:
        assert len(countries._default_data) == 211
        assert len(countries._data) == 423

    def test_init(self, countries: Countries) -> None:
        assert len(countries) == 211

    def test_get_key(self, countries: Countries) -> None:
        country = countries.get("ENG")
        if country is not None:
            assert country.code == "ENG"
            assert country.name == "England"

    def test_get_value(self, countries: Countries) -> None:
        country = countries.get("England")
        if country is not None:
            assert country.code == "ENG"
            assert country.name == "England"

    def test_get_custom_value(self, countries: Countries) -> None:
        country = countries["China PR"]
        assert country.code == "CHN"
        assert country.name == "China"

    def test_get_none(self, countries: Countries) -> None:
        country = countries.get("foo")
        assert country is None

    def test_raise_keyerror(self, countries: Countries) -> None:
        with pytest.raises(KeyError):
            countries["foo"]

    def test_search(self, countries: Countries) -> None:
        results = countries.search("ENG")
        assert len(results) == 3
        country = results[0]
        assert country.name == "England"

    def test_search_limit_one(self, countries: Countries) -> None:
        results = countries.search("ENG", limit=1)
        assert len(results) == 1

    def test_search_score_cutoff(self, countries: Countries) -> None:
        results = countries.search("ENG", score_cutoff=90.0)
        assert len(results) == 1

    def test_search_none(self, countries: Countries) -> None:
        results = countries.search("foobar")
        assert len(results) == 0

    def test_search_one(self, countries: Countries) -> None:
        country = countries.search_one("ENG")
        assert country is not None
        assert country.code == "ENG"
        assert country.name == "England"

    def test_search_one_none(self, countries: Countries) -> None:
        country = countries.search_one("foobar")
        assert country is None
