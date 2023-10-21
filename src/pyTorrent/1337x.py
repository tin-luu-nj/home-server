from py1337x import py1337x
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union


class TorrentSearch:
    """
    A class for searching torrents on 1337x.

    Attributes:
        name (str): The name of the torrent to search for.
        category (str): The category of the torrent. Must be one of the valid categories.
        sortBy (str): The attribute to sort the search results by. Must be one of the valid sortBy values.
        minSeeders (int): The minimum number of seeders the torrent must have.
        minLeechers (int): The minimum number of leechers the torrent must have.
        maxSizeGB (float): The maximum size of the torrent in GB.
        preferredSolution (list[str]): The preferred solutions for the torrent. Must be a subset of the valid solutions.

    Class Attributes:
        VALID_CATEGORIES (list[str]): The valid categories for a torrent.
        VALID_SORT_BY (list[str]): The valid attributes to sort the search results by.
        VALID_SOLUTIONS (list[str]): The valid solutions for a torrent.

    Methods:
        get_magnet_link(url: str) -> str: Get the magnet link from a torrent page.
        get_torrent_links() -> dict: Get the magnet links for a specific search query.
    """

    VALID_CATEGORIES: List[str] = [
        "movies",
        "tv",
        "games",
        "music",
        "apps",
        "anime",
        "documentaries",
    ]
    VALID_SORT_BY: List[str] = ["time", "size", "seeders", "leechers"]
    VALID_SOLUTIONS: List[str] = ["2160p", "1080p", "720p"]

    def __init__(
        self, data: Optional[Dict[str, Union[str, int, float, List[str]]]] = None
    ):
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def __setattr__(self, key, value):
        """
        Overrides the dot notation to set values.
        Raises ValueError if value does not meet the constraints.
        """
        if key == "category" and value not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category. Valid categories are: {self.VALID_CATEGORIES}"
            )

        if key == "sortBy" and value not in self.VALID_SORT_BY:
            raise ValueError(
                f"Invalid sortBy. Valid sortBy values are: {self.VALID_SORT_BY}"
            )

        if key in ["minSeeders", "minLeechers"] and (
            not isinstance(value, int) or value < 0
        ):
            raise ValueError(
                f"Invalid value for {key}. It should be a positive integer."
            )

        if key == "maxSizeGB" and (not isinstance(value, float) or value < 0):
            raise ValueError(f"Invalid value for {key}. It should be a positive float.")

        if key == "preferredSolution" and not set(value).issubset(
            set(self.VALID_SOLUTIONS)
        ):
            raise ValueError(
                f"Invalid preferredSolution. It should be a subset of: {self.VALID_SOLUTIONS}"
            )

        super().__setattr__(key, value)

    @staticmethod
    def get_magnet_link(url: str) -> str:
        """
        Get the magnet link from a torrent page.

        Args:
            url (str): The URL of the torrent page.

        Returns:
            str: The magnet link from the torrent page.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        link = soup.find("a", href=lambda href: href and href.startswith("magnet:?"))

        return link["href"]

    def get_torrent_links(self) -> Optional[Dict[str, Union[str, int]]]:
        """
        Get the magnet links for a specific search query.

        Returns:
            dict: A dictionary containing the torrent with the largest number of seeders.
                  Returns None if no matching torrents are found.
        """
        torrent_search = py1337x()

        search_results = torrent_search.search(
            self.name, category=self.category, sortBy=self.sortBy
        )

        valid_torrents = [
            result
            for result in search_results["items"]
            if int(result["seeders"]) >= self.minSeeders
            and int(result["leechers"]) >= self.minLeechers
            and convert_to_gb(result["size"]) <= self.maxSizeGB
        ]

        matching_torrents = []
        for preferred_solution in search_query.preferredSolution:
            for torrent in valid_torrents:
                if preferred_solution in torrent["name"]:
                    matching_torrents.append(torrent)
                    break
            if matching_torrents:
                break

        # Sort matching_torrents by 'seeders' in descending order and return the first item
        matching_torrents.sort(key=lambda x: int(x["seeders"]), reverse=True)

        return matching_torrents[0] if matching_torrents else None


def convert_to_gb(size_str):
    """
    Convert a string representing a size in GB or MB into GB.

    Args:
      size_str (str): The size string to convert.

    Returns:
      float: The size in GB.
    """
    size, unit = size_str.split()
    size = float(size)

    if unit.lower() == "mb":
        size /= 1024  # Convert MB to GB

    return size


# Create a TorrentSearch object with the desired search parameters
search_query = TorrentSearch(
    {
        "name": "Inception",
        "category": "movies",
        "sortBy": "size",
        "minSeeders": 10,
        "minLeechers": 10,
        "maxSizeGB": 30.0,
        "preferredSolution": ["2160p", "1080p", "720p"],
    }
)

# Get the torrent links
torrent = search_query.get_torrent_links()

# If a torrent was found, get its magnet link
if torrent:
    print(torrent["name"])
    magnet_link = TorrentSearch.get_magnet_link(torrent["link"])
    print(f"Magnet link for the torrent: {magnet_link}")
else:
    print("No torrents found that match the search criteria.")


from qbittorrent import Client
qb = Client('http://192.168.19.107:8080/')

qb.login('admin', 'Pass1234')
# defaults to admin:admin.
# to use defaults, just do qb.login()

# qb.download_from_link(magnet_link)

torrents = qb.torrents()

for torrent in torrents:
    print(torrent['name'])
