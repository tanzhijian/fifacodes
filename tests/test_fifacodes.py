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
