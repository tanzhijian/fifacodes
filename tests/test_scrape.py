import pytest
from httpx import Response

from scrape import parse


@pytest.fixture
def response() -> Response:
    with open("tests/wikipedia_fifacodes.html") as f:
        text = f.read()
    return Response(200, text=text)


def test_parse(response: Response) -> None:
    members = parse(response)
    assert len(members) == 211
    first_member = members[0]
    assert first_member.code == "AFG"
    assert first_member.name == "Afghanistan"
    last_member = members[-1]
    assert last_member.code == "ZIM"
    assert last_member.name == "Zimbabwe"
