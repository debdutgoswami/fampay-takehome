import datetime as dt
import logging

import requests
from urllib.parse import urlencode


class YTHandler:
    BASE_URL = "https://www.googleapis.com/youtube/"

    def __init__(self, keys: list):
        self.api_keys = keys
        self.current = 0
        self.end = len(keys) - 1
        if self.end == -1:
            raise ValueError("Atleast one API Key is mandatory!")

    @staticmethod
    def __construct_endpoint_with_parameter(endpoint: str, params: dict) -> str:
        return endpoint + "?" + urlencode(params)

    def __make_get(self, url: str):
        res = requests.get(self.BASE_URL + url, headers={"Accept": "application/json"})
        if res.status_code != 200:
            raise ValueError
        return res.json()

    def search(
        self, published_after: dt.datetime = None, page_token: str = None
    ) -> tuple[str | None, list[dict]]:
        if self.current > self.end:
            raise IndexError("All API Keys exhausted.")
        params = {
            "part": "snippet",
            "maxResults": 50,  # per page
            "type": "video",
            "order": "date",
            "key": self.api_keys[self.current],
        }
        if published_after:
            params["publishedAfter"] = published_after.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )  # according to RFC 3339
        if page_token:
            params["pageToken"] = page_token
        url = self.__construct_endpoint_with_parameter("v3/search", params)
        data = self.__make_get(url)

        items, items_per_page = list(), 0
        for item in data["items"]:
            items.append(
                {
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"],
                    "channel_name": item["snippet"]["channelTitle"],
                }
            )
            items_per_page += 1

        if items_per_page != data["pageInfo"]["resultsPerPage"]:
            logging.warning(
                f"Inconsistent `resultsPerPage`, expected {data['pageInfo']['resultsPerPage']}, found {items_per_page}"
            )

        return data.get("nextPageToken"), items

    def get_all_data(self, published_after: dt.datetime = None) -> list[dict]:
        next_page_token, result = None, list()
        while True:
            try:
                next_page_token, items = self.search(published_after, next_page_token)
            except ValueError:
                self.current += 1
            except IndexError:
                logging.warning("Incomplete data received. All API Keys exhausted")
                break
            else:
                result.extend(items)
                if next_page_token is None:
                    break
        return result
