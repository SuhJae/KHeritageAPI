#
# Main module of the Cultural Heritage API.
#
# This module provides easy abstraction of the Cultural Heritage API.
#
# Official API Documentation:
# https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0202.jsp&mn=NS_04_04_03
#
# Developed with the enthusiasm of Jay Suh (jay@joseon.space) from the non-profit organization Joseon Space
# (https://joseon.space). This module aims to facilitate efficient and accurate access  to Korea's rich cultural
# heritage data for developers and researchers globally.
#

import requests
from .models import *


class APIBase:
    ORIGIN_URL = 'http://www.cha.go.kr/cha/'

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params)
        response.raise_for_status()
        return response


class Search(APIBase):
    ENDPOINT = 'SearchKindOpenapiList.do'

    def __init__(self, heritage_type: HeritageType = None, start_year: int = None, end_year: int = None,
                 ko_name: str = None, city_code: CityCode = None, district_code: DistrictCode = None,
                 linked_number: str = None, canceled: bool = None, result_count: int = 10, page_index: int = 1):
        super().__init__()

        self.params = {'pageUnit': result_count, 'pageIndex': page_index}

        if start_year is not None:  # 지정연도 시작 (int)
            self.params['stCcbaAsdt'] = start_year
        if end_year is not None:  # 지정연도 끝 (int)
            self.params['enCcbaAsdt'] = end_year
        if ko_name is not None:  # 문화재명(국문)
            self.params['ccbaMnm1'] = ko_name
        if linked_number is not None:  # 문화재연계번호
            self.params['ccbaCpno'] = linked_number
        if canceled is not None:
            self.params['ccbaCncl'] = 'Y' if canceled else 'N'  # 지정해제여부 (Y, N)
        if heritage_type is not None:  # 지정종목별
            self.params['ccbaKdcd'] = heritage_type.value
        if city_code is not None:
            self.params['ccbaCtcd'] = city_code.value
        if district_code is not None:
            self.params['ccbaLcto'] = district_code.value

    def commit_search(self):
        xml_data = self._get(self.ENDPOINT, params=self.params).text
        return SearchResult(xml_data)

    def set_type(self, heritage_type: HeritageType) -> None:
        self.params['ccbaKdcd'] = heritage_type.value

    def set_start_year(self, start_year: int) -> None:
        self.params['stCcbaAsdt'] = start_year

    def set_end_year(self, end_year: int) -> None:
        self.params['enCcbaAsdt'] = end_year

    def set_ko_name(self, ko_name: str) -> None:
        self.params['ccbaMnm1'] = ko_name

    def set_province(self, city_code: CityCode) -> None:
        self.params['ccbaCtcd'] = city_code.value

    def set_city(self, district_code: DistrictCode) -> None:
        self.params['ccbaLcto'] = district_code.value

    def set_linked_number(self, linked_number: str) -> None:
        self.params['ccbaCpno'] = linked_number

    def set_canceled(self, canceled: bool) -> None:
        self.params['ccbaCncl'] = 'Y' if canceled else 'N'

    def set_limit(self, page_unit: int) -> None:
        self.params['pageUnit'] = page_unit

    def set_page_index(self, page_index: int) -> None:
        self.params['pageIndex'] = page_index


class ItemDetail(APIBase):
    ENDPOINT_INFO = 'SearchKindOpenapiDt.do'
    ENDPOINT_IMAGE = 'SearchImageOpenapi.do'
    ENDPOINT_VIDEO = 'SearchVideoOpenapi.do'

    def __init__(self, preview: SearchResultItems):
        super().__init__()
        self.params = {'ccbaKdcd': preview.type_code, 'ccbaAsno': preview.management_number,
                       'ccbaCtcd': preview.city_code}
        self.preview = preview

    def info(self):
        xml_data = self._get(self.ENDPOINT_INFO, params=self.params).text
        return Detail(xml_data, self.preview)

    def image(self):
        xml_data = self._get(self.ENDPOINT_IMAGE, params=self.params).text
        return Images(xml_data)

    def video(self):
        xml_data = self._get(self.ENDPOINT_VIDEO, params=self.params).text
        return Videos(xml_data)


class EventSearch(APIBase):
    ENDPOINT = "openapi/selectEventListOpenapi.do"

    def __init__(self, year: int, month: int, search_word: str = None, event_type: EventType = None):
        super().__init__()
        self.params = {'searchYear': year, 'searchMonth': month}
        if search_word is not None:
            self.params['searchWrd'] = search_word
        if event_type is not None:
            self.params['siteCode'] = event_type.value

    def commit_search(self):
        xml_data = self._get(self.ENDPOINT, params=self.params).text
        root = ElementTree.fromstring(xml_data)

        # iterate through the items in the XML
        items = []
        for item_element in root.findall('.//item'):
            # Assuming Event is a class that takes an XML element and parses it
            items.append(Event(item_element))

        return items


# Example Usage
if __name__ == '__main__':
    # Search for 15 historic sites in Seoul's Jongno district
    search = Search(result_count=15, city_code=CityCode.SEOUL, district_code=Seoul.JONGNRO, canceled=False,
                    heritage_type=HeritageType.HISTORIC_SITE)
    result = search.commit_search()

    # Get detailed information on the first item
    detail = ItemDetail(result.items[0])
    detail_info = detail.info()
    print(detail_info)

    # Also, you can get images and videos of the item
    images = detail.image()
    print(images)

    videos = detail.video()
    print(videos)

    # Search for events in 2023, December
    event_search = EventSearch(2023, 12)
    events = event_search.commit_search()
    for event in events:
        print(event)

