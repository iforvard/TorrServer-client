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


class BaseAPI:
    def __init__(self, host: str) -> None:
        self._host = host

    def _get(self, url: str, **kwargs) -> requests:
        """
        get request
        """
        return requests.get(f"{self._host}/{url}", **kwargs)

    def _post(self, url: str, **kwargs) -> requests:
        """
        post request
        """
        return requests.post(f"{self._host}/{url}", **kwargs)


class ServerAPI(BaseAPI):
    def _echo(self) -> str:
        """
        return version of server
        """
        return self._get("echo").text

    def _shutdown(self) -> str:
        """
        shutdown server
        """
        return self._get("shutdown").text


class PlaylistAPI(BaseAPI):
    def _get_all_playlists(self) -> str:
        """
        get all http links of all torrents in m3u list
        """
        return self._get("playlistall/all.m3u").text

    def _get_playlist(self, torrent_hash: str, from_last: bool = None) -> str:
        """
        get http links of torrent by hash in m3u list
        from_last: flag to exclude viewed
        """
        params = {"hash": torrent_hash, "fromlast": from_last}
        return self._get("playlist", params=params).text


class TorrentAPI(BaseAPI):
    def _upload_torrent(
        self, path: str, title: str = "", poster: str = "", save_to_db: bool = True
    ) -> dict:
        """
        upload torrent file
        """
        data = {"title": title, "poster": poster, "save": save_to_db}
        with open(path, "rb") as file:
            files_date = {path: file}
            return self._post("torrent/upload", data=data, files=files_date).json()

    def _get_torrents(self) -> dict:
        """
        get list of torrents
        """
        json_data = {"action": "list"}
        return self._post("torrents", json=json_data).json()

    def _delete_torrent(self, torrent_hash: str) -> str:
        """
        delete torrent by hash
        """
        json_data = {"action": "rem", "hash": torrent_hash}
        return self._post("torrents", json=json_data).text

    def _add_torrent(
        self, link: str, title: str = "", poster: str = "", save_to_db: bool = True
    ) -> dict:
        """
        add torrent by link http, https or magnet
        """
        json_data = {
            "action": "add",
            "link": link,
            "title": title,
            "poster": poster,
            "save_to_db": save_to_db,
        }
        return self._post("torrents", json=json_data).json()

    def _get_cache(self, torrent_hash: str) -> dict:
        """
        get torrent by cache
        """
        json_data = {"action": "get", "hash": torrent_hash}
        return self._post("cache", json=json_data).json()

    def list_torrents(self) -> list[Torrent]:
        """
        get list of torrents
        """
        torrents = [
            Torrent(
                title=torrent_dict["title"],
                poster=torrent_dict["poster"],
                files=[
                    File(**file_dict)
                    for file_dict in json.loads(torrent_dict["data"])["TorrServer"][
                        "Files"
                    ]
                ],
                date=datetime.fromtimestamp(torrent_dict["timestamp"]),
                hash=torrent_dict["hash"],
                torrent_size=torrent_dict["torrent_size"],
            )
            for torrent_dict in self._get_torrents()
        ]
        return torrents


class Client(ServerAPI, PlaylistAPI, TorrentAPI):
    """
    TorrServer API client
    """
