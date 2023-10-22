import os
import sys

# get the current working directory
# add the current working directory to sys.path
sys.path.append(os.getcwd())
from src.pyTorrent.torrent_1337x import TorrentSearch

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

qb = Client("http://192.168.19.107:8080/")

qb.login("admin", "Pass1234")
# defaults to admin:admin.
# to use defaults, just do qb.login()

# qb.download_from_link(magnet_link)

torrents = qb.torrents()

for torrent in torrents:
    print(torrent["name"])
