#
# Data Models and Enums for the Cultural Heritage API
#
# This module provides data models and enumerations for handling API parameters in English, enhancing developer
# convenience and code readability. Enum values are sourced from the official API documentation, reflecting
# the latest data as of November 23, 2023.
#
# Official API Documentation:
# https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0202.jsp
#
# Developed with the enthusiasm of Jay Suh (jay@joseon.space) from the non-profit organization Joseon Space
# (https://joseon.space). This module aims to facilitate efficient and accurate access  to Korea's rich cultural
# heritage data for developers and researchers globally.
#

from enum import Enum
import time
from xml.etree import ElementTree
from typing import Optional


def get_text_or_none(element: ElementTree, tag: str) -> Optional[str]:
    """ Helper function to get text from an XML element or None if the element is not found.

    :param element: XML element to search.
    :param tag: Tag of the element to search.
    :return: Text of the element or None if the element is not found.
    """
    found = element.find(tag)
    if found is None:
        return None
    if found.text is None:
        return None

    return found.text.strip()


class SearchResultItems:
    """ Data model for a single search result item.
    This class is used internally by the SearchResult class for storing search results.

    :ivar sequence_number: Sequence number of the search result item.
    :ivar uid: Unique ID of the search result item.
    :ivar type: Type of the search result item.
    :ivar name: Korean name of the search result item.
    :ivar name_hanja: Name of the search result item in Chinese characters.
    :ivar city: City name of the search result item.
    :ivar district: District name of the search result item.
    :ivar manager: Administrator name of the search result item.
    :ivar type_code: Type code of the search result item.
    :ivar city_code: City code of the search result item.
    :ivar management_number: Management number of the search result item.
    :ivar canceled: Whether the search result item is removed from the registered list of cultural heritage.
    :ivar linkage_number: Linkage number of the search result item.
    :ivar longitude: Longitude of the search result item.
    :ivar latitude: Latitude of the search result item.
    :ivar last_modified: Last modified date of the search result item.
    """

    def __init__(self, element: ElementTree) -> None:
        """ Initializes the search result item.

        :param element: XML element of the search result item.
        """

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

    def __str__(self) -> str:
        return f"[Item {self.sequence_number}]\n- UID: {self.uid}\n- Type: {self.type}\n- Name: {self.name}\n" \
               f"- Name (Hanja): {self.name_hanja}\n- City: {self.city}\n- District: {self.district}\n" \
               f"- Administrator: {self.manager}\n- Type Code: {self.type_code}\n" \
               f"- City Code: {self.city_code}\n- Management Number: {self.management_number}\n" \
               f"- Canceled: {self.canceled}\n- Linkage Number: {self.linkage_number}\n" \
               f"- Longitude: {self.longitude}\n- Latitude: {self.latitude}\n" \
               f"- Last Modified: {self.last_modified}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self) -> dict:
        """ Returns the search result item as a dictionary.

        :return: The search result item as a dictionary in the following format:
            {
                'sequence_number': Sequence number of the search result item.
                'uid': Unique ID of the search result item.
                'type': Type of the search result item.
                'name': Korean name of the search result item.
                'name_hanja': Name of the search result item in Chinese characters.
                'city': City name of the search result item.
                'district': District name of the search result item.
                'administrator': Administrator name of the search result item.
                'type_code': Type code of the search result item.
                'city_code': City code of the search result item.
                'management_number': Management number of the search result item.
                'canceled': Whether the search result item is removed from the registered list of cultural heritage.
                'linkage_number': Linkage number of the search result item.
                'longitude': Longitude of the search result item.
                'latitude': Latitude of the search result item.
                'last_modified': Last modified date of the search result item.
            }
        """
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
    """ Data model for holding multiple search results returned from the API.
    Iteration or indexing of this class will return SearchResultItems.

    :ivar hits: Total number of results available from the API.
    :ivar limit: Number of results per page.
    :ivar page_index: Index of the current page.
    :ivar items: List of search result items.
    """

    def __init__(self, xml_data: str) -> None:
        """ Initializes the search result.

        :param xml_data: XML data returned from the API.
        """
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

    def pages(self) -> int:
        """
        The number of pages that are available from the API.
        :return: The number of pages that are available from the API.
        """
        return int(self.hits) // int(self.limit) + 1


class Detail:
    """ Data model for a detailed information of a single cultural heritage item.

    :ivar uid: Unique ID of the search result item.
    :ivar name: Korean name of the search result item.
    :ivar name_hanja: Name of the search result item in Chinese characters.
    :ivar city: City name of the search result item.
    :ivar district: District name of the search result item.
    :ivar canceled: Whether the search result item is removed from the registered list of cultural heritage.
    :ivar last_modified: Last modified date of the search result item.
    :ivar type_code: Type code of the search result item.
    :ivar management_number: Management number of the search result item.
    :ivar city_code: City code of the search result item.
    :ivar linkage_number: Linkage number of the search result item.
    :ivar longitude: Longitude of the search result item.
    :ivar latitude: Latitude of the search result item.
    :ivar type: Type of the search result item.
    :ivar category1: Parent category of the category2. The broadest category.
    :ivar category2: Child category of the category1. The second broadest category.
    :ivar category3: Child category of the category2. The second narrowest category.
    :ivar category4: Child category of the category3. The narrowest category.
    :ivar quantity: Quantity of the cultural heritage item.
    :ivar registered_date: Registered date of the cultural heritage item.
    :ivar location_description: Location description of the cultural heritage item.
    :ivar era: Era of the cultural heritage item.
    :ivar owner: Owner of the cultural heritage item.
    :ivar manager: Manager of the cultural heritage item.
    :ivar thumbnail: Thumbnail of the cultural heritage item.
    :ivar content: Content of the cultural heritage item.
    """

    def __init__(self, xml_data: str, preview: SearchResultItems) -> None:
        """ Initializes the detailed information of a single cultural heritage item.

        :param xml_data: XML data returned from the API.
        :param preview: Preview information of the cultural heritage item used to search this item.
        """

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

    def dict(self) -> dict:
        """ Returns the detailed information of the cultural heritage item as a dictionary.

        :return: The detailed information of the cultural heritage item as a dictionary in the following format:
            {
                'uid': Unique ID of the search result item.
                'name': Korean name of the search result item.
                'name_hanja': Name of the search result item in Chinese characters.
                'city': City name of the search result item.
                'district': District name of the search result item.
                'canceled': Whether the search result item is removed from the registered list of cultural heritage.
                'last_modified': Last modified date of the search result item.
                'type_code': Type code of the search result item.
                'management_number': Management number of the search result item.
                'city_code': City code of the search result item.
                'linkage_number': Linkage number of the search result item.
                'longitude': Longitude of the search result item.
                'latitude': Latitude of the search result item.
                'type': Type of the search result item.
                'category1': Parent category of the category2. The broadest category.
                'category2': Child category of the category1. The second broadest category.
                'category3': Child category of the category2. The second narrowest category.
                'category4': Child category of the category3. The narrowest category.
                'quantity': Quantity of the cultural heritage item.
                'registered_date': Registered date of the cultural heritage item.
                'location_description': Location description of the cultural heritage item.
                'era': Era of the cultural heritage item.
                'owner': Owner of the cultural heritage item.
                'thumbnail': Thumbnail of the cultural heritage item.
                'content': Content of the cultural heritage item.
            }
        """
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
    """Data model for an image of a cultural heritage item.

    :ivar licence: Licence of the image.
    :ivar image_url: URL of the image.
    :ivar description: Description of the image."""

    def __init__(self, licence: str, image_url: str, description: str) -> None:
        """ Initializes the image of a cultural heritage item.

        :param licence: Licence code of the image.
        :param image_url: URL of the image.
        :param description: Description of the image.
        """

        self.licence = licence
        self.image_url = image_url
        self.description = description

    def __str__(self):
        return f"- Image Nuri: {self.licence}\n- Image URL: {self.image_url}\n" \
               f"- Description: {self.description}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self) -> dict:
        """ Returns the image of the cultural heritage item as a dictionary.

        :return: The image of the cultural heritage item as a dictionary in the following format:
            {
                'image_nuri': Licence code of the image.
                'image_url': URL of the image.
                'description': Description of the image.
            }
        """
        return {
            'image_nuri': self.licence,
            'image_url': self.image_url,
            'description': self.description
        }


class Images:
    """Data model for multiple images of a cultural heritage item.

    :ivar count: Total number of images available.
    :ivar type: Type of the cultural heritage item.
    :ivar management_number: Management number of the cultural heritage item.
    :ivar city_code: City code of the cultural heritage item.
    :ivar name: Korean name of the cultural heritage item.
    :ivar name_hanja: Name of the cultural heritage item in Chinese characters.
    :ivar images: List of images of the cultural heritage item.
    """

    def __init__(self, xml_data: str) -> None:
        """ Initializes the images of a cultural heritage item.

        :param xml_data: XML data returned from the API.
        """

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
                     f"City Code: {self.city_code}\nName: {self.name}\nName (Hanja): {self.name_hanja}\n"
        result_str += "\n".join(str(image) for image in self.images)
        return result_str

    def __getitem__(self, item):
        return self.images[item]

    def __iter__(self):
        return iter(self.images)

    def __len__(self):
        return len(self.images)


class Videos:
    """Data model for multiple videos of a cultural heritage item.
    Indexes and iteration of this class will return the video URLs.

    :ivar count: Total number of videos available.
    :ivar type: Type of the cultural heritage item.
    :ivar management_number: Management number of the cultural heritage item.
    :ivar city_code: City code of the cultural heritage item.
    :ivar name: Korean name of the cultural heritage item.
    :ivar name_hanja: Name of the cultural heritage item in Chinese characters.
    :ivar videos: List of videos of the cultural heritage item.
    """

    def __init__(self, xml_data: str) -> None:
        """Initializes the videos of a cultural heritage item.

        :param xml_data: XML data returned from the API.
        """
        root = ElementTree.fromstring(xml_data)

        self.count = get_text_or_none(root, 'totalCnt')
        self.type = get_text_or_none(root, 'ccbaKdcd')
        self.management_number = get_text_or_none(root, 'ccbaAsno')
        self.city_code = get_text_or_none(root, 'ccbaCtcd')
        self.name = get_text_or_none(root, 'ccbaMnm1')
        self.name_hanja = get_text_or_none(root, 'ccbaMnm2')

        self.videos = []
        item = root.find('item')
        if item is not None:
            for video_info in zip(item.findall('sn'), item.findall('videoUrl')):
                if video_info[1].text == "http://116.67.83.213/webdata/file_data/media_data/videos/":
                    continue
                self.videos.append(video_info[1].text)

    def __str__(self):
        result_str = f"Total Count: {self.count}\nType: {self.type}\nManagement Number: {self.management_number}\n" \
                     f"City Code: {self.city_code}\nName: {self.name}\nName (Hanja): {self.name_hanja}\n"
        result_str += "\n".join(str(video) for video in self.videos)
        return result_str

    def __getitem__(self, item):
        return self.videos[item]

    def __iter__(self):
        return iter(self.videos)

    def __len__(self):
        return len(self.videos)


class Event:
    """Data model for a single event.

    :ivar sequence_number: Sequence number of the event.
    :ivar event_type: Type of the event.
    :ivar event_name: Name of the event.
    :ivar event_description: Description of the event.
    :ivar start_date: Start date of the event.
    :ivar end_date: End date of the event.
    :ivar host_name: Host name of the event.
    :ivar contact: Contact information of the event.
    :ivar event_location: Location of the event.
    :ivar event_url: URL of the event.
    :ivar audiance: Audiance of the event.
    :ivar etc: Additional information of the event.
    :ivar city: City of the event.
    :ivar district: District of the event.
    :ivar time_detail: Time detail of the event.
    """

    def __init__(self, xml_data: str) -> None:
        """Initializes the event object.

        :param xml_data: XML data returned from the API.
        """
        self.sequence_number = get_text_or_none(xml_data, 'sn')
        self.event_type = get_text_or_none(xml_data, 'siteCode')
        self.event_name = get_text_or_none(xml_data, 'siteName')
        self.event_description = get_text_or_none(xml_data, 'subContent')
        self.host_name = get_text_or_none(xml_data, 'groupName')
        self.contact = get_text_or_none(xml_data, 'contact')
        self.event_location = get_text_or_none(xml_data, 'subDesc')
        self.event_url = get_text_or_none(xml_data, 'subPath')
        self.audiance = get_text_or_none(xml_data, 'subDesc1')
        self.etc = get_text_or_none(xml_data, 'subDesc2')
        self.city = get_text_or_none(xml_data, 'sido')
        self.district = get_text_or_none(xml_data, 'gugun')
        self.time_detail = get_text_or_none(xml_data, 'subDate')

        s_date = get_text_or_none(xml_data, 'sDate')
        e_date = get_text_or_none(xml_data, 'eDate')
        self.start_date = time.strptime(s_date, '%Y%m%d') if s_date is not None else None
        self.end_date = time.strptime(e_date, '%Y%m%d') if e_date is not None else None

    def __str__(self):
        return f"[Event {self.sequence_number}]\n- Type: {self.event_type}\n- Name: {self.event_name}\n" \
               f"- Description: {self.event_description}\n- Start Date: {self.start_date}\n" \
               f"- End Date: {self.end_date}\n- Host Name: {self.host_name}\n- Contact: {self.contact}\n" \
               f"- Location: {self.event_location}\n- URL: {self.event_url}\n- Audiance: {self.audiance}\n" \
               f"- Etc: {self.etc}\n- City: {self.city}\n- District: {self.district}\n" \
               f"- Time Detail: {self.time_detail}"

    def __getitem__(self, item):
        return self.dict()[item]

    def dict(self) -> dict:
        """ Returns the event as a dictionary.
        :return: The event as a dictionary in the following format:
            {
                'sequence_number': Sequence number of the event.
                'event_type': Type of the event.
                'event_name': Name of the event.
                'event_description': Description of the event.
                'start_date': Start date of the event.
                'end_date': End date of the event.
                'host_name': Host name of the event.
                'contact': Contact information of the event.
                'event_location': Location of the event.
                'event_url': URL of the event.
                'audiance': Audiance of the event.
                'etc': Additional information of the event.
                'city': City of the event.
                'district': District of the event.
                'time_detail': Time detail of the event.
            }
        """

        return {
            'sequence_number': self.sequence_number,
            'event_type': self.event_type,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'host_name': self.host_name,
            'contact': self.contact,
            'event_location': self.event_location,
            'event_url': self.event_url,
            'audiance': self.audiance,
            'etc': self.etc,
            'city': self.city,
            'district': self.district,
            'time_detail': self.time_detail
        }


# ===================================================== CONSTANTS =====================================================

class HeritageType(Enum):
    NATIONAL_TREASURE = '11'  # 국보
    TREASURE = '12'  # 보물
    HISTORIC_SITE = '13'  # 사적
    HISTORIC_AND_SCENIC_SITE = '14'  # 사적및명승
    SCENIC_SITE = '15'  # 명승
    NATURAL_MONUMENT = '16'  # 천연기념물
    INTANGIBLE_HERITAGE = '17'  # 국가무형문화재
    FOLKLORE_HERITAGE = '18'  # 국가민속문화재
    REGIONAL_HERITAGE = '21'  # 시도유형문화재
    REGIONAL_INTANGIBLE_HERITAGE = '22'  # 시도무형문화재
    REGIONAL_MONUMENT = '23'  # 시도기념물
    REGIONAL_FOLKLORE_HERITAGE = '24'  # 시도민속문화재
    REGIONAL_REGISTERED_HERITAGE = '25'  # 시도등록문화재
    HERITAGE_MATERIAL = '31'  # 문화재자료
    NATIONAL_REGISTERED_HERITAGE = '79'  # 국가등록문화재
    NORTH_KOREAN_INTANGIBLE_HERITAGE = '80'  # 이북5도무형문화재


class EventType(Enum):
    NIGHTTIME_HERITAGE = '01'  # 문화재야행
    VIVID_HERITAGE = '02'  # 생생문화재
    TRADITIONAL_TEMPLE_HERITAGE = '03'  # 전통산사문화재
    HYANGGYO_AND_SEOWON = '04'  # 살아숨쉬는향교서원
    NATIONAL_INTANGIBLE_HERITAGE = '07'  # 국립무형유산원
    CULTURAL_HERITAGE_FOUNDATION = '08'  # 한국문화재재단
    TRADITIONAL_HOUSES = '09'  # 고택종갓집
    WORLD_HERITAGE = '10'  # 세계유산
    OTHERS = '06'  # 기타행사


class CityCode(Enum):
    SEOUL = '11'  # 서울
    BUSAN = '21'  # 부산
    DAEGU = '22'  # 대구
    INCHEON = '23'  # 인천
    GWANGJU = '24'  # 광주
    DAEJEON = '25'  # 대전
    ULSAN = '26'  # 울산
    SEJONG = '45'  # 세종
    GYEONGGI = '31'  # 경기
    GANGWON = '32'  # 강원
    CHUNGBUK = '33'  # 충북
    CHUNGNAM = '34'  # 충남
    JEONBUK = '35'  # 전북
    JEONNAM = '36'  # 전남
    GYEONGBUK = '37'  # 경북
    GYEONGNAM = '38'  # 경남
    JEJU = '50'  # 제주
    NATIONAL = 'ZZ'  # 전국일원


class DistrictCode(Enum):
    pass


class Seoul(DistrictCode):
    ALL = '00'  # 전체
    JONGNRO = '11'  # 종로구
    JUNG = '12'  # 중구
    YONGSAN = '13'  # 용산구
    SEONGDONG = '14'  # 성동구
    DONGDAEMUN = '15'  # 동대문구
    SEONGBUK = '16'  # 성북구
    DOBONG = '17'  # 도봉구
    EUNPYEONG = '18'  # 은평구
    SEOULDAEMUN = '19'  # 서대문구
    MAPO = '20'  # 마포구
    GANGSEO = '21'  # 강서구
    GURO = '22'  # 구로구
    YEONGDEUNGPO = '23'  # 영등포구
    DONGJAK = '24'  # 동작구
    GWANAK = '25'  # 관악구
    GANGNAM = '26'  # 강남구
    GANGDONG = '27'  # 강동구
    SONGPA = '28'  # 송파구
    JUNGNANG = '29'  # 중랑구
    NOWON = '30'  # 노원구
    SEOCHO = '31'  # 서초구
    YANGCHEON = '32'  # 양천구
    GWANGJIN = '33'  # 광진구
    GANGBUK = '34'  # 강북구
    GEUMCHEON = '35'  # 금천구
    HAN_RIVER = '99'  # 한강일원
    SEOUL_WIDE = 'ZZ'  # 서울전역


class Busan(DistrictCode):
    ALL = '00'  # 전체
    JUNG = '11'  # 중구
    SEO = '12'  # 서구
    DONG = '13'  # 동구
    YEONGDO = '14'  # 영도구
    BUSANJIN = '15'  # 부산진구
    DONGNAE = '16'  # 동래구
    NAM = '17'  # 남구
    BUK = '18'  # 북구
    HAEUNDAE = '19'  # 해운대구
    SAHA = '20'  # 사하구
    GEUMJEONG = '21'  # 금정구
    GANGSEO = '22'  # 강서구
    YEONJE = '23'  # 연제구
    SUYEONG = '24'  # 수영구
    SASANG = '25'  # 사상구
    GIJANG = '26'  # 기장군
    BUSAN_WIDE = 'ZZ'  # 부산전역


class Daegu(DistrictCode):
    ALL = '00'  # 전체
    JUNG = '11'  # 중구
    DONG = '12'  # 동구
    SEO = '13'  # 서구
    NAM = '14'  # 남구
    BUK = '15'  # 북구
    SUSEONG = '16'  # 수성구
    DALSEO = '17'  # 달서구
    DALSEONG = '18'  # 달성군
    DAEGU_WIDE = 'ZZ'  # 대구전역
    GUNWI = '32'  # 군위군


class Incheon(DistrictCode):
    ALL = '00'  # 전체
    JUNG = '11'  # 중구
    DONG = '12'  # 동구
    MICHUHOL = '20'  # 미추홀구
    SEO = '15'  # 서구
    NAMDONG = '16'  # 남동구
    YEONSU = '17'  # 연수구
    BUPYEONG = '18'  # 부평구
    GYEYANG = '19'  # 계양구
    GANGHWA = '30'  # 강화군
    ONGJIN = '31'  # 옹진군
    INCHEON_WIDE = 'ZZ'  # 인천전역


class Gwangju(DistrictCode):
    ALL = '00'  # 전체
    DONG = '11'  # 동구
    SEO = '12'  # 서구
    BUK = '13'  # 북구
    GWANGSAN = '14'  # 광산구
    NAM = '15'  # 남구
    GWANGJU_WIDE = 'ZZ'  # 광주전역


class Daejeon(DistrictCode):
    ALL = '00'  # 전체
    DONG = '11'  # 동구
    JUNG = '12'  # 중구
    SEO = '13'  # 서구
    YUSEONG = '14'  # 유성구
    DAEDEOK = '15'  # 대덕구
    DAEJEON_WIDE = 'ZZ'  # 대전전역


class Ulsan(DistrictCode):
    ALL = '00'  # 전체
    NAM = '01'  # 남구
    DONG = '02'  # 동구
    BUK = '03'  # 북구
    JUNG = '04'  # 중구
    ULJU = '05'  # 울주군
    ULSAN_WIDE = 'ZZ'  # 울산전역


class Sejong(DistrictCode):
    SEJONG_WIDE = '00'  # 세종시전역


class Gyeonggi(DistrictCode):
    ALL = '00'  # 전체
    SUWON = '11'  # 수원시
    SEONGNAM = '12'  # 성남시
    UIJEONGBU = '13'  # 의정부시
    ANYANG = '14'  # 안양시
    BUCHEON = '15'  # 부천시
    GWANGMYEONG = '16'  # 광명시
    ANSEONG = '17'  # 안성시
    DONGDUCHEON = '18'  # 동두천시
    GURI = '19'  # 구리시
    PYEONGTAEK = '20'  # 평택시
    GWACHEON = '21'  # 과천시
    ANSAN = '22'  # 안산시
    OSAN = '25'  # 오산시
    UIWANG = '26'  # 의왕시
    GUNPO = '27'  # 군포시
    SIHEUNG = '28'  # 시흥시
    HANAM = '30'  # 하남시
    YANGJU = '31'  # 양주시
    YEOJU = '70'  # 여주시
    HWASEONG = '35'  # 화성시
    PAJU = '37'  # 파주시
    GWANGJU = '39'  # 광주시
    YEONCHEON = '40'  # 연천군
    POCHUN = '41'  # 포천시
    GAPYEONG = '42'  # 가평군
    YANGPYEONG = '43'  # 양평군
    ICHEON = '44'  # 이천시
    YONGIN = '45'  # 용인시
    KIMPO = '47'  # 김포시
    GOYANG = '50'  # 고양시
    NAMYANGJU = '51'  # 남양주시
    GYEONGGI_WIDE = 'ZZ'  # 경기전역


class Gangwon(DistrictCode):
    ALL = '00'  # 전체
    CHUNCHEON = '11'  # 춘천시
    WONJU = '12'  # 원주시
    GANGNEUNG = '13'  # 강릉시
    DONGHAE = '14'  # 동해시
    TAEBAEK = '15'  # 태백시
    SOKCHO = '16'  # 속초시
    SAMCHEOK = '17'  # 삼척시
    HONGCHEON = '32'  # 홍천군
    HOENGSEONG = '33'  # 횡성군
    YEONGWOL = '35'  # 영월군
    PYEONGCHANG = '36'  # 평창군
    JEONGSEON = '37'  # 정선군
    CHEORWON = '38'  # 철원군
    HWACHEON = '39'  # 화천군
    YANGGU = '40'  # 양구군
    INJE = '41'  # 인제군
    GOSEONG = '42'  # 고성군
    YANGYANG = '43'  # 양양군
    MYEONGJU = '44'  # 명주군
    GANGWON_WIDE = 'ZZ'  # 강원전역


class Chungbuk(DistrictCode):
    ALL = '00'  # 전체
    CHEONGJU = '20'  # 청주시
    CHUNGJU = '12'  # 충주시
    JECHON = '13'  # 제천시
    BOEUN = '32'  # 보은군
    OKCHEON = '33'  # 옥천군
    YEONGDONG = '34'  # 영동군
    JINCHEON = '35'  # 진천군
    GOESAN = '36'  # 괴산군
    EUMSEONG = '37'  # 음성군
    DANYANG = '40'  # 단양군
    JEUNGPO = '42'  # 증평군
    CHUNGBUK_WIDE = 'ZZ'  # 충북전역


class Chungnam(DistrictCode):
    ALL = '00'  # 전체
    CHEONAN = '11'  # 천안시
    GONGJU = '12'  # 공주시
    SEOSAN = '15'  # 서산시
    ASAN = '16'  # 아산시
    BORYEONG = '17'  # 보령시
    GYERYONG = '18'  # 계룡시
    GEUMSAN = '31'  # 금산군
    NONSAN = '35'  # 논산시
    BUYEO = '36'  # 부여군
    SEOCHUN = '37'  # 서천군
    CHEONGYANG = '39'  # 청양군
    HONGSEONG = '40'  # 홍성군
    YESAN = '41'  # 예산군
    DANGJIN = '43'  # 당진시
    TAEAN = '46'  # 태안군
    CHUNGNAM_WIDE = 'ZZ'  # 충남전역


class Jeonbuk(DistrictCode):
    ALL = '00'  # 전체
    JEONJU = '11'  # 전주시
    GUNSAN = '12'  # 군산시
    NAMWON = '15'  # 남원시
    KIMJE = '16'  # 김제시
    JEONGEUP = '17'  # 정읍시
    IKSAN = '18'  # 익산시
    WANJU = '31'  # 완주군
    JINAN = '32'  # 진안군
    MUJU = '33'  # 무주군
    JANGSU = '34'  # 장수군
    IMSIL = '35'  # 임실군
    SUNCHANG = '37'  # 순창군
    GOCHANG = '39'  # 고창군
    BUAN = '40'  # 부안군
    JEONBUK_WIDE = 'ZZ'  # 전북전역


class Jeonnam(DistrictCode):
    ALL = '00'  # 전체
    MOKPO = '11'  # 목포시
    YEOSU = '12'  # 여수시
    SUNCHEON = '13'  # 순천시
    NAJU = '14'  # 나주시
    YEOCHEON = '15'  # 여천시
    GWANGYANG = '17'  # 광양시
    DAMYANG = '32'  # 담양군
    GOKSEONG = '33'  # 곡성군
    GURYE = '34'  # 구례군
    YEOCHEONGUN = '36'  # 여천군
    GOHEUNG = '38'  # 고흥군
    BOSEONG = '39'  # 보성군
    HWASUN = '40'  # 화순군
    JANGHEUNG = '41'  # 장흥군
    GANGJIN = '42'  # 강진군
    HAENAM = '43'  # 해남군
    YEONGAM = '44'  # 영암군
    MUAN = '45'  # 무안군
    HAMPYEONG = '47'  # 함평군
    YEONGGWANG = '48'  # 영광군
    JANGSEONG = '49'  # 장성군
    WANDO = '50'  # 완도군
    JINDO = '51'  # 진도군
    SINAN = '52'  # 신안군
    SEUNGJU = '53'  # 승주군
    JEONNAM_WIDE = 'ZZ'  # 전남전역


class Gyeongbuk(DistrictCode):
    ALL = '00'  # 전체
    POHANG = '11'  # 포항시
    GYEONGJU = '12'  # 경주시
    GIMCHEON = '13'  # 김천시
    ANDONG = '14'  # 안동시
    GUMI = '15'  # 구미시
    YEONGJU = '16'  # 영주시
    YEONGCHEON = '17'  # 영천시
    SANGJU = '18'  # 상주시
    GYEONGSAN = '20'  # 경산시
    MUNGYEONG = '21'  # 문경시
    UISEONG = '33'  # 의성군
    CHEONGSONG = '35'  # 청송군
    YEONGYANG = '36'  # 영양군
    YEONGDEOK = '37'  # 영덕군
    CHEONGDO = '42'  # 청도군
    GORYEONG = '43'  # 고령군
    SEONGJU = '44'  # 성주군
    CHILGOK = '45'  # 칠곡군
    YECHON = '50'  # 예천군
    BONGHWA = '52'  # 봉화군
    ULJIN = '53'  # 울진군
    ULLUNG = '54'  # 울릉군
    GYEONGBUK_WIDE = 'ZZ'  # 경북전역


class Gyeongnam(DistrictCode):
    ALL = '00'  # 전체
    JINJU = '13'  # 진주시
    CHANGWON = '50'  # 창원시
    GIMHAE = '18'  # 김해시
    MILYANG = '22'  # 밀양시
    TONGYEONG = '25'  # 통영시
    GEOJE = '26'  # 거제시
    SACHEON = '27'  # 사천시
    UIRYEONG = '32'  # 의령군
    HAMAN = '33'  # 함안군
    CHANGNYEONG = '34'  # 창녕군
    YANGSAN = '36'  # 양산시
    UISEONG = '39'  # 의창군
    GOSEONG = '42'  # 고성군
    NAMHAE = '44'  # 남해군
    HADONG = '45'  # 하동군
    SANCHEONG = '46'  # 산청군
    HAMYANG = '47'  # 함양군
    GEORGCHEONG = '48'  # 거창군
    HAPCHEON = '49'  # 합천군
    GYEONGNAM_WIDE = 'ZZ'  # 경남전역


class Jeju(DistrictCode):
    ALL = '00'  # 전체
    JEJU_CITY = '01'  # 제주시
    SEOGWIPO = '02'  # 서귀포시
    JEJU_WIDE = 'ZZ'  # 제주전역
