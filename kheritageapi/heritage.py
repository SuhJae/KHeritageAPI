"""Client wrappers for the Cultural Heritage APIs."""

from __future__ import annotations

from typing import Optional
from xml.etree import ElementTree

import requests

from .models import (
    CityCode,
    DistrictCode,
    EventType,
    HeritageDetail,
    HeritageEvent,
    HeritageImageSet,
    HeritageSearchResult,
    HeritageSearchResults,
    HeritageType,
    HeritageVideoSet,
)


class HeritageAPIBase:
    """Base API client with shared session and request handling."""

    ORIGIN_URL = "https://www.cha.go.kr/cha/"

    def __init__(self, timeout: float = 15.0) -> None:
        self.session = requests.Session()
        self.timeout = timeout

    def _get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response


class HeritageSearcher(HeritageAPIBase):
    ENDPOINT = "SearchKindOpenapiList.do"

    def __init__(
        self,
        heritage_type: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        ko_name: Optional[str] = None,
        city_code: Optional[str] = None,
        district_code: Optional[str] = None,
        linked_number: Optional[str] = None,
        canceled: Optional[bool] = None,
        result_count: int = 10,
        page_index: int = 1,
        era_code: Optional[str] = None,
        modified_start: Optional[str] = None,
        modified_end: Optional[str] = None,
        timeout: float = 15.0,
    ) -> None:
        super().__init__(timeout=timeout)

        self.params: dict[str, object] = {"pageUnit": result_count, "pageIndex": page_index}

        if start_year is not None:
            self.params["stCcbaAsdt"] = start_year
        if end_year is not None:
            self.params["enCcbaAsdt"] = end_year
        if ko_name is not None:
            self.params["ccbaMnm1"] = ko_name
        if linked_number is not None:
            self.params["ccbaCpno"] = linked_number
        if canceled is not None:
            self.params["ccbaCncl"] = "Y" if canceled else "N"
        if heritage_type is not None:
            self.params["ccbaKdcd"] = heritage_type
        if city_code is not None:
            self.params["ccbaCtcd"] = city_code
        if district_code is not None:
            self.params["ccbaLcto"] = district_code
        if era_code is not None:
            self.params["ccbaPcd1"] = era_code
        if modified_start is not None:
            self.params["stRegDt"] = modified_start
        if modified_end is not None:
            self.params["enRegDt"] = modified_end

    def perform_search(self) -> HeritageSearchResult:
        xml_data = self._get(self.ENDPOINT, params=self.params).text
        return HeritageSearchResult(xml_data)

    def set_type(self, heritage_type: HeritageType) -> None:
        self.params["ccbaKdcd"] = heritage_type

    def set_start_year(self, start_year: int) -> None:
        self.params["stCcbaAsdt"] = start_year

    def set_end_year(self, end_year: int) -> None:
        self.params["enCcbaAsdt"] = end_year

    def set_ko_name(self, ko_name: str) -> None:
        self.params["ccbaMnm1"] = ko_name

    def set_province(self, city_code: CityCode) -> None:
        self.params["ccbaCtcd"] = city_code

    def set_city(self, district_code: DistrictCode) -> None:
        self.params["ccbaLcto"] = district_code

    def set_linked_number(self, linked_number: str) -> None:
        self.params["ccbaCpno"] = linked_number

    def set_canceled(self, canceled: bool) -> None:
        self.params["ccbaCncl"] = "Y" if canceled else "N"

    def set_limit(self, page_unit: int) -> None:
        self.params["pageUnit"] = page_unit

    def set_page_index(self, page_index: int) -> None:
        self.params["pageIndex"] = page_index

    def set_era_code(self, era_code: str) -> None:
        self.params["ccbaPcd1"] = era_code

    def set_modified_start(self, modified_start: str) -> None:
        self.params["stRegDt"] = modified_start

    def set_modified_end(self, modified_end: str) -> None:
        self.params["enRegDt"] = modified_end


class HeritageInfo(HeritageAPIBase):
    ENDPOINT_INFO = "SearchKindOpenapiDt.do"
    ENDPOINT_IMAGE = "SearchImageOpenapi.do"
    ENDPOINT_VIDEO = "SearchVideoOpenapi.do"

    def __init__(self, preview: HeritageSearchResults, timeout: float = 15.0) -> None:
        super().__init__(timeout=timeout)
        self.params = {
            "ccbaKdcd": preview.type_code,
            "ccbaAsno": preview.management_number,
            "ccbaCtcd": preview.city_code,
        }
        self.preview = preview

    def retrieve_detail(self) -> HeritageDetail:
        xml_data = self._get(self.ENDPOINT_INFO, params=self.params).text
        return HeritageDetail(xml_data, self.preview)

    def retrieve_image(self) -> HeritageImageSet:
        xml_data = self._get(self.ENDPOINT_IMAGE, params=self.params).text
        return HeritageImageSet(xml_data)

    def retrieve_video(self) -> HeritageVideoSet:
        xml_data = self._get(self.ENDPOINT_VIDEO, params=self.params).text
        return HeritageVideoSet(xml_data)


class EventSearcher(HeritageAPIBase):
    ENDPOINT = "openapi/selectEventListOpenapi.do"

    def __init__(
        self,
        year: int,
        month: int,
        search_word: Optional[str] = None,
        event_type: Optional[EventType] = None,
        timeout: float = 15.0,
    ) -> None:
        super().__init__(timeout=timeout)
        self.params: dict[str, object] = {"searchYear": year, "searchMonth": month}
        if search_word is not None:
            self.params["searchWrd"] = search_word
        if event_type is not None:
            self.params["siteCode"] = event_type

    def perform_search(self) -> list[HeritageEvent]:
        xml_data = self._get(self.ENDPOINT, params=self.params).text
        root = ElementTree.fromstring(xml_data)
        return [HeritageEvent(item_element) for item_element in root.findall(".//item")]
