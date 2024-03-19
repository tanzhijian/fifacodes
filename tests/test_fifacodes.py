import pytest

from fifacodes import Members


def test_singleton() -> None:
    s1 = Members()
    s2 = Members()
    assert s1 is s2


class TestMembers:
    @pytest.fixture(scope="class")
    def members(self) -> Members:
        return Members()

    def test_read_data(self, members: Members) -> None:
        assert len(members._default_data) == 211
        assert len(members._data) == 427

    def test_init(self, members: Members) -> None:
        assert len(members) == 211

    def test_get_key(self, members: Members) -> None:
        member = members.get("ENG")
        if member is not None:
            assert member.code == "ENG"
            assert member.name == "England"

    def test_get_value(self, members: Members) -> None:
        member = members.get("England")
        if member is not None:
            assert member.code == "ENG"
            assert member.name == "England"

    def test_get_custom_value(self, members: Members) -> None:
        member = members["China PR"]
        assert member.code == "CHN"
        assert member.name == "China"

    def test_get_none(self, members: Members) -> None:
        member = members.get("foo")
        assert member is None

    def test_raise_keyerror(self, members: Members) -> None:
        with pytest.raises(KeyError):
            members["foo"]

    def test_search(self, members: Members) -> None:
        results = members.search("eng")
        assert len(results) == 2
        member = results[0]
        assert member.name == "England"

    def test_search_limit_one(self, members: Members) -> None:
        results = members.search("eng", limit=1)
        assert len(results) == 1

    def test_search_score_cutoff(self, members: Members) -> None:
        results = members.search("eng", score_cutoff=90.0)
        assert len(results) == 1

    def test_search_case_sensitive_true(self, members: Members) -> None:
        results = members.search("ENG", case_sensitive=True)
        assert len(results) == 3
        member = results[0]
        assert member.name == "England"

    def test_search_none(self, members: Members) -> None:
        results = members.search("12345")
        assert len(results) == 0

    def test_search_one(self, members: Members) -> None:
        member = members.search_one("eng")
        assert member is not None
        assert member.code == "ENG"
        assert member.name == "England"

    def test_search_one_none(self, members: Members) -> None:
        member = members.search_one("12345")
        assert member is None
