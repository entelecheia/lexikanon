from lexikanon import __version__, get_version


def test_get_version() -> None:
    assert get_version() == __version__
    assert __version__.count(".") in range(2, 5)
