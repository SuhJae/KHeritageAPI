#
# Main module of the Cultural Heritage API.
#
# This module provides easy abstraction of the Cultural Heritage API.
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

    def get_url(self) -> str:
        """
        Get the URL of the search.
        :return: URL of the search.
        """

        return self.ORIGIN_URL + self.ENDPOINT_BASE + '?' + '&'.join(
            [f'{key}={value}' for key, value in self.params.items() if value])


class ConstructSearch(APIBase):
    ENDPOINT_BASE = 'SearchKindOpenapiList.do'

    def __init__(self, heritage_type: HeritageType = None, start_year: int = None, end_year: int = None,
                 ko_name: str = None, province_code: ProvinceCode = None, city_code: CityCode = None,
                 linked_number: str = None, canceled: bool = None, result_count: int = None, page_index: int = None):
        super().__init__()

        self.params = {}

        if start_year is not None:  # 지정연도 시작 (int)
            self.params['stCcbaAsdt'] = start_year
        if end_year is not None:  # 지정연도 끝 (int)
            self.params['enCcbaAsdt'] = end_year
        if ko_name is not None:  # 문화재명(국문)
            self.params['ccbaMnm1'] = ko_name
        if linked_number is not None:  # 문화재연계번호
            self.params['ccbaCpno'] = linked_number
        if result_count is not None:  # 페이징 처리 시 페이지당 건 수 (int)
            self.params['pageUnit'] = result_count
        if page_index is not None:  # 조회할 페이지 숫자 (int)
            self.params['pageIndex'] = page_index
        if canceled is not None:
            self.params['ccbaCncl'] = 'Y' if canceled else 'N'  # 지정해제여부 (Y, N)
        if heritage_type is not None:  # 지정종목별
            self.params['ccbaKdcd'] = heritage_type.value
        if province_code is not None:
            self.params['ccbaCtcd'] = province_code.value
        if city_code is not None:
            self.params['ccbaLcto'] = city_code.value

    def set_type(self, heritage_type: HeritageType) -> None:
        self.params['ccbaKdcd'] = heritage_type.value

    def set_start_year(self, start_year: int) -> None:
        self.params['stCcbaAsdt'] = start_year

    def set_end_year(self, end_year: int) -> None:
        self.params['enCcbaAsdt'] = end_year

    def set_ko_name(self, ko_name: str) -> None:
        self.params['ccbaMnm1'] = ko_name

    def set_province_code(self, province_code: ProvinceCode) -> None:
        self.params['ccbaCtcd'] = province_code.value

    def set_city_code(self, city_code: CityCode) -> None:
        self.params['ccbaLcto'] = city_code.value

    def set_linked_number(self, linked_number: str) -> None:
        self.params['ccbaCpno'] = linked_number

    def set_canceled(self, canceled: bool) -> None:
        self.params['ccbaCncl'] = 'Y' if canceled else 'N'

    def set_result_count(self, page_unit: int) -> None:
        self.params['pageUnit'] = page_unit

    def set_page_index(self, page_index: int) -> None:
        self.params['pageIndex'] = page_index


if __name__ == '__main__':
    search = ConstructSearch(city_code=Seoul.JONGNRO)
    search.set_result_count(50)
    search.set_type(HeritageType.INTANGIBLE_HERITAGE)
    print(search.get_url())
