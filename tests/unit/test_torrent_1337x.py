import pytest
import requests
from unittest.mock import patch

from src.pyTorrent.torrent_1337x import TorrentSearch


@pytest.fixture
def torrent_search():
    return TorrentSearch()


def test_init(torrent_search):
    search_parameters = {
        "name": "test",
        "category": "movies",
        "sortBy": "time",
        "minSeeders": 100,
        "minLeechers": 50,
        "maxSizeGB": 1.0,
        "preferredSolution": ["720p", "1080p", "2160p"],
    }
    torrent_search = TorrentSearch(search_parameters)
    assert torrent_search.name == "test"
    assert torrent_search.category == "movies"
    assert torrent_search.sortBy == "time"
    assert torrent_search.minSeeders == 100
    assert torrent_search.minLeechers == 50
    assert torrent_search.maxSizeGB == 1.0
    assert torrent_search.preferredSolution == ["720p", "1080p", "2160p"]


def test_invalid_init():
    invalid_search_parameters = {
        "name": "test",
        "category": "invalid_category",
        "sortBy": "time",
        "minSeeders": 100,
        "minLeechers": 50,
        "maxSizeGB": 1.0,
        "preferredSolution": ["720p"],
    }
    with pytest.raises(ValueError):
        TorrentSearch(invalid_search_parameters)


def test_setattr_errors(torrent_search):
    with pytest.raises(ValueError):
        torrent_search.category = "invalid_category"

    with pytest.raises(ValueError):
        torrent_search.sortBy = "invalid_sortBy"

    with pytest.raises(ValueError):
        torrent_search.minSeeders = -1

    with pytest.raises(ValueError):
        torrent_search.minLeechers = -1

    with pytest.raises(ValueError):
        torrent_search.maxSizeGB = -1.0

    with pytest.raises(ValueError):
        torrent_search.preferredSolution = ["invalid_solution"]


@patch("requests.get")
def test_get_magnet_link(mock_get, torrent_search):
    mock_response = mock_get.return_value
    mock_response.text = '<a href="magnet:?xt=urn:btih:example">Magnet Link</a>'

    result = torrent_search.get_magnet_link("http://example.com")
    assert result == "magnet:?xt=urn:btih:example"


@patch("py1337x.py1337x.py1337x.search")
def test_get_torrent_links(mock_search, torrent_search):
    # Mock the response from py1337x.search
    mock_search.return_value = {
        "items": [
            {
                "name": "test 720p",
                "seeders": "200",
                "leechers": "100",
                "size": "500 MB",
            },
            {
                "name": "test 1080p",
                "seeders": "150",
                "leechers": "50",
                "size": "1.5 GB",
            },
        ]
    }

    # Initialize a TorrentSearch object
    torrent_search.name = "test"
    torrent_search.category = "movies"
    torrent_search.sortBy = "time"
    torrent_search.minSeeders = 100
    torrent_search.minLeechers = 50
    torrent_search.maxSizeGB = 1.0
    torrent_search.preferredSolution = ["720p", "1080p", "2160p"]

    # Call get_torrent_links and verify the result
    result = torrent_search.get_torrent_links()
    assert result == {
        "name": "test 720p",
        "seeders": "200",
        "leechers": "100",
        "size": "500 MB",
    }
