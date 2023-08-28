from datetime import datetime
from urllib.parse import urljoin

import requests


class MonobankError(Exception):
    pass


class MonobankClient:
    def __init__(self, token: str, base_url: str = "https://api.monobank.ua/"):
        self._token = token
        self._base_url = base_url

    def _make_url(self, uri):
        return urljoin(self._base_url, uri)

    def _request(self, method, uri, **kwargs):
        response = requests.request(
            method=method,
            url=self._make_url(uri),
            headers={"X-Token": self._token},
            **kwargs
        )

        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.status_code != 200:
            raise MonobankError(
                f"Invalid status code: {response.status_code}. Content: {response.content.decode('utf-8')}."
            )

        try:
            data = response.json()
        except ValueError:
            raise MonobankError(
                f"Cannot parse json in body: {response.content.decode('utf-8')}."
            )

        return data

    def client_info(self):
        return self._request("GET", "/personal/client-info")

    def statement(self, start: datetime, to: datetime):
        return self._request("GET", f"/personal/statement/0/{int(start.timestamp())}/{int(to.timestamp())}")
