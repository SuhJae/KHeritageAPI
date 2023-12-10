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
from models import *


class APIBase:
    ORIGIN_URL = 'http://www.cha.go.kr/cha/'

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params)
        response.raise_for_status()
        return response


class Search(APIBase):
    ENDPOINT_BASE = 'SearchKindOpenapiList.do'

    def __init__(self, heritage_type: HeritageType = None, start_year: int = None, end_year: int = None,
                 ko_name: str = None, province_code: ProvinceCode = None, city_code: CityCode = None,
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
        if province_code is not None:
            self.params['ccbaCtcd'] = province_code.value
        if city_code is not None:
            self.params['ccbaLcto'] = city_code.value

    def commit_search(self):
        xml_data = self._get(self.ENDPOINT_BASE, params=self.params).text
        return SearchResult(xml_data)

    def set_type(self, heritage_type: HeritageType) -> None:
        self.params['ccbaKdcd'] = heritage_type.value

    def set_start_year(self, start_year: int) -> None:
        self.params['stCcbaAsdt'] = start_year

    def set_end_year(self, end_year: int) -> None:
        self.params['enCcbaAsdt'] = end_year

    def set_ko_name(self, ko_name: str) -> None:
        self.params['ccbaMnm1'] = ko_name

    def set_province(self, province_code: ProvinceCode) -> None:
        self.params['ccbaCtcd'] = province_code.value

    def set_city(self, city_code: CityCode) -> None:
        self.params['ccbaLcto'] = city_code.value

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


if __name__ == '__main__':
    search = Search()
    search.set_province(ProvinceCode.SEOUL)
    search.set_type(HeritageType.NATIONAL_TREASURE)
    search.set_limit(3)
    search.set_page_index(1)

    results = search.commit_search()

    for result in results:
        detail = ItemDetail(result)
        print(detail.image())
