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
import time


# Helper function to get text or None
def get_text_or_none(element, tag):
    found = element.find(tag)
    return found.text.strip() if found is not None else None


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
        self.sequence_number = element.find('sn').text
        self.uid = element.find('no').text
        self.type = element.find('ccmaName').text
        self.name = element.find('ccbaMnm1').text
        self.name_hanja = element.find('ccbaMnm2').text
        self.city = element.find('ccbaCtcdNm').text
        self.district = element.find('ccsiName').text
        self.manager = element.find('ccbaAdmin').text
        self.type_code = element.find('ccbaKdcd').text
        self.city_code = element.find('ccbaCtcd').text
        self.management_number = element.find('ccbaAsno').text
        self.canceled = element.find('ccbaCncl').text == 'Y'
        self.linkage_number = element.find('ccbaCpno').text
        self.longitude = element.find('longitude').text
        self.latitude = element.find('latitude').text
        self.last_modified = time.strptime(element.find('regDt').text, '%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"[Item {self.sequence_number}]\n- UID: {self.uid}\n- Type: {self.type}\n- Name: {self.name}\n" \
               f"- Name (Hanja): {self.name_hanja}\n- City: {self.city}\n- District: {self.district}\n" \
               f"- Administrator: {self.manager}\n- Type Code: {self.type_code}\n" \
               f"- City Code: {self.city_code}\n- Management Number: {self.management_number}\n" \
               f"- Canceled: {self.canceled}\n- Linkage Number: {self.linkage_number}\n" \
               f"- Longitude: {self.longitude}\n- Latitude: {self.latitude}\n" \
               f"- Last Modified: {self.last_modified}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self):
        return {
            'sequence_number': self.sequence_number,
            'uid': self.uid,
            'type': self.type,
            'name': self.name,
            'name_hanja': self.name_hanja,
            'city': self.city,
            'district': self.district,
            'administrator': self.manager,
            'type_code': self.type_code,
            'city_code': self.city_code,
            'management_number': self.management_number,
            'canceled': self.canceled,
            'linkage_number': self.linkage_number,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'last_modified': self.last_modified
        }


class SearchResult:
    def __init__(self, xml_data):
        root = ElementTree.fromstring(xml_data)
        self.hits = root.find('totalCnt').text
        self.limit = root.find('pageUnit').text
        self.page_index = root.find('pageIndex').text
        self.items = [SearchResultItems(item) for item in root.findall('.//item')]

    def __str__(self):
        result_str = f"Total Count: {self.hits}\nPage Unit: {self.limit}\nPage Index: {self.page_index}\n\n"
        result_str += "\n".join(str(item) for item in self.items)
        return result_str

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def count(self):
        """
        The number of results fetched from the API.
        :return: The number of results fetched from the API.
        """
        return len(self.items)

    def pages(self):
        """
        The number of pages that are available from the API.
        :return: The number of pages that are available from the API.
        """
        return int(self.hits) // int(self.limit) + 1


class Detail:
    def __init__(self, xml_data: str, preview: SearchResultItems):
        self.uid = preview.uid
        self.name = preview.name
        self.name_hanja = preview.name_hanja
        self.city = preview.city
        self.district = preview.district
        self.canceled = preview.canceled
        self.last_modified = preview.last_modified

        root = ElementTree.fromstring(xml_data)
        item = root.find('item')

        self.type_code = get_text_or_none(root, 'ccbaKdcd')
        self.management_number = get_text_or_none(root, 'ccbaAsno')
        self.city_code = get_text_or_none(root, 'ccbaCtcd')
        self.linkage_number = get_text_or_none(root, 'ccbaCpno')
        self.longitude = get_text_or_none(root, 'longitude')
        self.latitude = get_text_or_none(root, 'latitude')
        self.type = get_text_or_none(item, 'ccmaName')
        self.category1 = get_text_or_none(item, 'gcodeName')
        self.category2 = get_text_or_none(item, 'bcodeName')
        self.category3 = get_text_or_none(item, 'mcodeName')
        self.category4 = get_text_or_none(item, 'scodeName')
        self.quantity = get_text_or_none(item, 'ccbaQuan')

        # Special handling for date
        date_str = get_text_or_none(item, 'ccbaAsdt')
        self.registered_date = time.strptime(date_str, '%Y%m%d') if date_str else None

        self.location_description = get_text_or_none(item, 'ccbaLcad')
        self.era = get_text_or_none(item, 'ccceName')
        self.owner = get_text_or_none(item, 'ccbaPoss')
        self.manager = get_text_or_none(item, 'ccbaAdmin')
        self.thumbnail = get_text_or_none(item, 'imageUrl')
        self.content = get_text_or_none(item, 'content')

    def __str__(self):
        return f"- UID: {self.uid}\n- Type: {self.type}\n- Name: {self.name}\n" \
               f"- Name (Hanja): {self.name_hanja}\n- City: {self.city}\n- District: {self.district}\n" \
               f"- Administrator: {self.manager}\n- Type Code: {self.type_code}\n" \
               f"- City Code: {self.city_code}\n- Management Number: {self.management_number}\n" \
               f"- Canceled: {self.canceled}\n- Linkage Number: {self.linkage_number}\n" \
               f"- Longitude: {self.longitude}\n- Latitude: {self.latitude}\n" \
               f"- Last Modified: {self.last_modified}\n- Category 1: {self.category1}\n" \
               f"- Category 2: {self.category2}\n- Category 3: {self.category3}\n" \
               f"- Category 4: {self.category4}\n- Quantity: {self.quantity}\n" \
               f"- Registered Date: {self.registered_date}\n- Location Description: {self.location_description}\n" \
               f"- Era: {self.era}\n- Owner: {self.owner}\n- Thumbnail: {self.thumbnail}\n" \
               f"- Content: {self.content}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'name_hanja': self.name_hanja,
            'city': self.city,
            'district': self.district,
            'canceled': self.canceled,
            'last_modified': self.last_modified,
            'type_code': self.type_code,
            'management_number': self.management_number,
            'city_code': self.city_code,
            'linkage_number': self.linkage_number,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'type': self.type,
            'category1': self.category1,
            'category2': self.category2,
            'category3': self.category3,
            'category4': self.category4,
            'quantity': self.quantity,
            'registered_date': self.registered_date,
            'location_description': self.location_description,
            'era': self.era,
            'owner': self.owner,
            'thumbnail': self.thumbnail,
            'content': self.content
        }


class Image:
    def __init__(self, licence, image_url, description):
        self.licence = licence
        self.image_url = image_url
        self.description = description

    def __str__(self):
        return f"- Image Nuri: {self.licence}\n- Image URL: {self.image_url}\n" \
               f"- Description: {self.description}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self):
        return {
            'image_nuri': self.licence,
            'image_url': self.image_url,
            'description': self.description
        }


class Images:
    def __init__(self, xml_data: str):
        root = ElementTree.fromstring(xml_data)

        self.count = get_text_or_none(root, 'totalCnt')
        self.type = get_text_or_none(root, 'ccbaKdcd')
        self.management_number = get_text_or_none(root, 'ccbaAsno')
        self.city_code = get_text_or_none(root, 'ccbaCtcd')
        self.name = get_text_or_none(root, 'ccbaMnm1')
        self.name_hanja = get_text_or_none(root, 'ccbaMnm2')

        self.images = []

        self.images = []
        item = root.find('item')
        if item is not None:
            for image_info in zip(item.findall('sn'), item.findall('imageNuri'), item.findall('imageUrl'),
                                  item.findall('ccimDesc')):
                self.images.append(Image(image_info[1].text, image_info[2].text, image_info[3].text))

    def __str__(self):
        result_str = f"Total Count: {self.count}\nType: {self.type}\nManagement Number: {self.management_number}\n" \
                     f"City Code: {self.city_code}\nName: {self.name}\nName (Hanja): {self.name_hanja}\n\n"
        result_str += "\n".join(str(image) for image in self.images)
        return result_str

    def __getitem__(self, item):
        return self.images[item]

    def __iter__(self):
        return iter(self.images)

    def __len__(self):
        return len(self.images)


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
