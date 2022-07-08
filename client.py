import json
from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class File:
    id: int
    path: str
    length: int


@dataclass
class Torrent:
    title: str
    poster: str
    files: list[File]
    date: datetime
    hash: str
    torrent_size: int


def get_torrents():
    json_data = {'action': 'list'}
    response = requests.post('http://192.168.1.5:8090/torrents', json=json_data)
    torrents = [Torrent(
        title=torrent_dict["title"],
        poster=torrent_dict["poster"],
        files=[File(**file_dict) for file_dict in json.loads(torrent_dict["data"])["TorrServer"]["Files"]],
        date=datetime.fromtimestamp(torrent_dict["timestamp"]),
        hash=torrent_dict["hash"],
        torrent_size=torrent_dict["torrent_size"],
    )
        for torrent_dict in response.json()]
    return torrents
