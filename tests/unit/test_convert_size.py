import pytest
from src.pyTorrent.torrent_1337x import convert_size


def test_convert_size():
    # Test conversion from KB to MB
    assert convert_size("1024 KB", "MB") == 1.0

    # Test conversion from MB to GB
    assert convert_size("1024 MB", "GB") == 1.0

    # Test conversion from GB to TB
    assert convert_size("1024 GB", "TB") == 1.0

    # Test conversion from TB to GB
    assert convert_size("1 TB", "GB") == 1024.0

    # Test conversion from same unit to same unit
    assert convert_size("1 TB", "TB") == 1.0


def test_invalid_input():
    # Test invalid size_str format
    with pytest.raises(ValueError):
        convert_size("1024 kilobytes", "MB")

    # Test invalid to_unit format
    with pytest.raises(ValueError):
        convert_size("1024 KB", "megabytes")
