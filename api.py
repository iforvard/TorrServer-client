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


class Client:
    def __init__(self, host: str) -> None:
        self._host = host

    def _get(self):
        pass

    def _post(self, url: str, data: dict) -> dict:
        return requests.post(f"{self._host}/{url}", json=data).json()

    def _get_torrents(self) -> dict:
        json_data = {'action': 'list'}
        return self._post(f'torrents', data=json_data)

    def list_torrents(self) -> list[Torrent]:
        torrents = [Torrent(
            title=torrent_dict["title"],
            poster=torrent_dict["poster"],
            files=[File(**file_dict) for file_dict in json.loads(torrent_dict["data"])["TorrServer"]["Files"]],
            date=datetime.fromtimestamp(torrent_dict["timestamp"]),
            hash=torrent_dict["hash"],
            torrent_size=torrent_dict["torrent_size"],
        )
            for torrent_dict in self._get_torrents()]
        return torrents
