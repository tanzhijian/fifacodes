import pytest
from httpx import Response

from scrape import parse


@pytest.fixture
def response() -> Response:
    with open("tests/wikipedia_fifacodes.html") as f:
        text = f.read()
    return Response(200, text=text)


def test_parse(response: Response) -> None:
    countries = parse(response)
    assert len(countries) == 211
    first_country = countries[0]
    assert first_country.code == "AFG"
    assert first_country.name == "Afghanistan"
    last_country = countries[-1]
    assert last_country.code == "ZIM"
    assert last_country.name == "Zimbabwe"
