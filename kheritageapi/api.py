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
import xml.etree.ElementTree as ElementTree


class APIBase:
    ORIGIN_URL = 'http://www.cha.go.kr/cha/'

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params)
        response.raise_for_status()
        return response


class SearchResultItems:
    def __init__(self, element):
        self.sn = element.find('sn').text
        self.no = element.find('no').text
        self.ccma_name = element.find('ccmaName').text
        self.crltsno_nm = element.find('crltsnoNm').text
        self.ccba_mnm1 = element.find('ccbaMnm1').text
        self.ccba_mnm2 = element.find('ccbaMnm2').text
        self.ccba_ctcd_nm = element.find('ccbaCtcdNm').text
        self.ccsi_name = element.find('ccsiName').text
        self.ccba_admin = element.find('ccbaAdmin').text
        self.ccba_kdcd = element.find('ccbaKdcd').text
        self.ccba_ctcd = element.find('ccbaCtcd').text
        self.ccba_asno = element.find('ccbaAsno').text
        self.ccba_cncl = element.find('ccbaCncl').text
        self.ccba_cpno = element.find('ccbaCpno').text
        self.longitude = element.find('longitude').text
        self.latitude = element.find('latitude').text
        self.reg_dt = element.find('regDt').text

    def __str__(self):
        return f"[Item {self.sn}]\n-No {self.no}\n-CCMA Name: {self.ccma_name}\n-Crltsno Name: {self.crltsno_nm}\n-" \
               f"CCBA Mnm1: {self.ccba_mnm1}\n-CCBA Mnm2: {self.ccba_mnm2}\n-CCBA Ctcd Name: {self.ccba_ctcd_nm}\n-" \
               f"CCSI Name: {self.ccsi_name}\n-CCBA Admin: {self.ccba_admin}\n-CCBA Kdcd: {self.ccba_kdcd}\n-" \
               f"CCBA Ctcd: {self.ccba_ctcd}\n-CCBA Asno: {self.ccba_asno}\n-CCBA Cncl: {self.ccba_cncl}\n-" \
               f"CCBA Cpno: {self.ccba_cpno}\n-Longitude: {self.longitude}\n-Latitude: {self.latitude}\n-" \
               f"Reg Dt: {self.reg_dt}"


class SearchResult:
    def __init__(self, xml_data):
        root = ElementTree.fromstring(xml_data)
        self.total_cnt = root.find('totalCnt').text
        self.page_unit = root.find('pageUnit').text
        self.page_index = root.find('pageIndex').text
        self.items = [SearchResultItems(item) for item in root.findall('.//item')]

    def __str__(self):
        result_str = f"Total Count: {self.total_cnt}\nPage Unit: {self.page_unit}\nPage Index: {self.page_index}\n\n"
        result_str += "\n".join(str(item) for item in self.items)
        return result_str


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

    def commit_search(self):
        # Parse the XML data
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

    def set_result_count(self, page_unit: int) -> None:
        self.params['pageUnit'] = page_unit

    def set_page_index(self, page_index: int) -> None:
        self.params['pageIndex'] = page_index


if __name__ == '__main__':
    search = ConstructSearch()
    search.set_province(ProvinceCode.SEOUL.JONGNRO)
    search.set_city(Seoul.JONGNRO)
    search.set_type(HeritageType.HISTORIC_SITE)

    results = search.commit_search()

    print(results)
