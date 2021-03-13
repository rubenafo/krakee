from krakee.api.utils import as_list


def test_as_list():
    assert as_list((1)) == [1]
    assert as_list((1, 2)) == [1, 2]
    assert as_list((["1"])) == ["1"]
    assert as_list(([1,2])) == [1,2]

