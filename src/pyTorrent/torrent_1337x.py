import re
from typing import Dict, List, Optional, Union

import requests
from bs4 import BeautifulSoup
from py1337x import py1337x


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
        self, search_parameters: Optional[Dict[str, Union[str, int, float, List[str]]]] = None
    ) -> None:
        """
        Initializes the instance with the provided search parameters.

        Args:
            search_parameters (dict): The search parameters to set.
        """
        if search_parameters is not None:
            for parameter, value in search_parameters.items():
                setattr(self, parameter, value)

    def __setattr__(self, parameter: str, value: Union[str, int, float, List[str]]) -> None:
        """
        Overrides the dot notation to set values.
        Raises ValueError if value does not meet the constraints.

        Args:
            parameter (str): The parameter to set.
            value (str/int/float/list): The value to set.

        Raises:
            ValueError: If the value does not meet the constraints.
        """
        validators = {
            "category": {
                "check": lambda x: x in self.VALID_CATEGORIES,
                "error": f"Invalid category. Valid categories are: {self.VALID_CATEGORIES}",
            },
            "sortBy": {
                "check": lambda x: x in self.VALID_SORT_BY,
                "error": f"Invalid sortBy. Valid sortBy xs are: {self.VALID_SORT_BY}",
            },
            "minSeeders": {
                "check": lambda x: isinstance(x, int) and x >= 0,
                "error": f"Invalid x for {parameter}. It should be a positive integer.",
            },
            "minLeechers": {
                "check": lambda x: isinstance(x, int) and x >= 0,
                "error": f"Invalid x for {parameter}. It should be a positive integer.",
            },
            "maxSizeGB": {
                "check": lambda x: isinstance(x, float) and x >= 0,
                "error": f"Invalid x for {parameter}. It should be a positive float.",
            },
            "preferredSolution": {
                "check": lambda x: len(x) == 3 and set(x).issubset(set(self.VALID_SOLUTIONS)),
                "error": f"Invalid preferredSolution. It should be a subset of: {self.VALID_SOLUTIONS}",
            },
        }

        if parameter in validators and not validators[parameter]["check"](value):
            raise ValueError(validators[parameter]["error"])

        super().__setattr__(parameter, value)

    @staticmethod
    def get_magnet_link(torrent_page_url: str) -> str:
        """
        Get the magnet link from a torrent page.

        Args:
            torrent_page_url (str): The URL of the torrent page.

        Returns:
            str: The magnet link from the torrent page.
        """
        response = requests.get(torrent_page_url)
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
            and convert_size(result["size"], "GB") <= self.maxSizeGB
        ]

        matching_torrents = []
        
        for preferred_solution in self.preferredSolution:
            for torrent in valid_torrents:
                if preferred_solution in torrent["name"]:
                    matching_torrents.append(torrent)
                    break
            if matching_torrents:
                break

        
        # Sort matching_torrents by 'seeders' in descending order and return the first item
        matching_torrents.sort(key=lambda x: int(x["seeders"]), reverse=True)

        return matching_torrents[0] if matching_torrents else None


def convert_size(size_str: str, to_unit: str) -> float:
    """
    Convert a string representing a size in KB, MB, GB, or TB into the specified unit.

    Args:
      size_str (str): The size string to convert.
      to_unit (str): The unit to convert to.

    Returns:
      float: The size in the specified unit.
    """
    # Check if size_str and to_unit are in the correct format using regex
    if not re.match(r"^\d+(\.\d+)?\s(KB|MB|GB|TB)$", size_str, re.IGNORECASE):
        raise ValueError(
            "size_str must be a string in the format '<number> <unit>', where <unit> is either 'KB', 'MB', 'GB' or 'TB'"
        )
    if not re.match(r"^(KB|MB|GB|TB)$", to_unit, re.IGNORECASE):
        raise ValueError(
            "to_unit must be a string, where <unit> is either 'KB', 'MB', 'GB' or 'TB'"
        )

    size, from_unit = size_str.split()
    size = float(size)

    units = ["kb", "mb", "gb", "tb"]
    size *= 1024 ** (units.index(from_unit.lower()) - units.index(to_unit.lower()))

    return size
