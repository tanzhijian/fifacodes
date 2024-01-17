import pytest

from fifacodes import Counties


class TestCounties:
    @pytest.fixture(scope="class")
    def counties(self) -> Counties:
        return Counties()

    def test_read_data(self, counties: Counties) -> None:
        assert len(counties.data) == 423

    def test_init(self, counties: Counties) -> None:
        assert len(counties) == 423

    def test_get_key(self, counties: Counties) -> None:
        country = counties.get("ENG")
        if country is not None:
            assert country.code == "ENG"
            assert country.name == "England"

    def test_get_value(self, counties: Counties) -> None:
        country = counties.get("England")
        if country is not None:
            assert country.code == "ENG"
            assert country.name == "England"

    def test_get_custom_value(self, counties: Counties) -> None:
        country = counties["China PR"]
        assert country.code == "CHN"
        assert country.name == "China"

    def test_get_none(self, counties: Counties) -> None:
        country = counties.get("foo")
        assert country is None

    def test_raise_keyerror(self, counties: Counties) -> None:
        with pytest.raises(KeyError):
            counties["foo"]

    def test_search(self, counties: Counties) -> None:
        results = counties.search("ENG")
        assert len(results) == 3
        country = results[0]
        assert country.name == "England"

    def test_search_limit_one(self, counties: Counties) -> None:
        results = counties.search("ENG", limit=1)
        assert len(results) == 1

    def test_search_score_cutoff(self, counties: Counties) -> None:
        results = counties.search("ENG", score_cutoff=90.0)
        assert len(results) == 1

    def test_search_none(self, counties: Counties) -> None:
        results = counties.search("foobar")
        assert len(results) == 0

    def test_search_one(self, counties: Counties) -> None:
        country = counties.search_one("ENG")
        assert country is not None
        assert country.code == "ENG"
        assert country.name == "England"

    def test_search_one_none(self, counties: Counties) -> None:
        country = counties.search_one("foobar")
        assert country is None
