"""Client wrappers for palace/jongmyo APIs."""

from __future__ import annotations

from typing import Optional
from xml.etree import ElementTree

import requests

from .models import PalaceCode, PalaceDetail, PalaceSearchResultItem


class PalaceAPIBase:
    ORIGIN_URL = "https://www.heritage.go.kr/"

    def __init__(self, timeout: float = 15.0) -> None:
        self.session = requests.Session()
        self.timeout = timeout

    def _get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response


class PalaceSearcher(PalaceAPIBase):
    ENDPOINT = "heri/gungDetail/gogungListOpenApi.do"

    def __init__(self, palace: PalaceCode, timeout: float = 15.0) -> None:
        super().__init__(timeout=timeout)
        self.params = {"gung_number": palace}

    def perform_search(self) -> list[PalaceSearchResultItem]:
        response = self._get(self.ENDPOINT, self.params)
        root = ElementTree.fromstring(response.text)
        return [PalaceSearchResultItem.from_xml(search_item) for search_item in root.findall("list")]


class PalaceInfo(PalaceAPIBase):
    ENDPOINT = "heri/gungDetail/gogungDetailOpenApi.do"

    def __init__(self, preview: PalaceSearchResultItem, timeout: float = 15.0) -> None:
        super().__init__(timeout=timeout)
        self.params = {
            "serial_number": preview.serial_number,
            "gung_number": preview.palace_code,
            "detail_code": preview.detail_code,
        }

    def retrieve_details(self) -> PalaceDetail:
        response = self._get(self.ENDPOINT, self.params)
        return PalaceDetail(response.text)
