"""Data models and constants for KHeritage API wrappers."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterable, Optional
from xml.etree import ElementTree


def _text(element: Optional[ElementTree.Element], tag: str, *fallback_tags: str) -> Optional[str]:
    """Return stripped text for the first available tag."""
    if element is None:
        return None

    for name in (tag, *fallback_tags):
        found = element.find(name)
        if found is not None and found.text is not None:
            value = found.text.strip()
            if value:
                return value
    return None


def get_text_or_none(element: Optional[ElementTree.Element], tag: str) -> Optional[str]:
    """Backward-compatible helper kept for external callers."""
    return _text(element, tag)


def _parse_struct_time(value: Optional[str], fmt: str) -> Optional[time.struct_time]:
    if not value:
        return None
    try:
        return time.strptime(value, fmt)
    except ValueError:
        return None


@dataclass
class HeritageSearchResults:
    sequence_number: Optional[str]
    uid: Optional[str]
    type: Optional[str]
    name: Optional[str]
    name_hanja: Optional[str]
    city: Optional[str]
    district: Optional[str]
    manager: Optional[str]
    type_code: Optional[str]
    city_code: Optional[str]
    management_number: Optional[str]
    canceled: bool
    linkage_number: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    last_modified: Optional[time.struct_time]

    @classmethod
    def from_xml(cls, element: ElementTree.Element) -> "HeritageSearchResults":
        cncl = _text(element, "ccbaCncl")
        return cls(
            sequence_number=_text(element, "sn"),
            uid=_text(element, "no"),
            type=_text(element, "ccmaName"),
            name=_text(element, "ccbaMnm1"),
            name_hanja=_text(element, "ccbaMnm2"),
            city=_text(element, "ccbaCtcdNm"),
            district=_text(element, "ccsiName"),
            manager=_text(element, "ccbaAdmin"),
            type_code=_text(element, "ccbaKdcd"),
            city_code=_text(element, "ccbaCtcd"),
            management_number=_text(element, "ccbaAsno"),
            canceled=(cncl == "Y"),
            linkage_number=_text(element, "ccbaCpno"),
            longitude=_text(element, "longitude"),
            latitude=_text(element, "latitude"),
            last_modified=_parse_struct_time(_text(element, "regDt"), "%Y-%m-%d %H:%M:%S"),
        )

    def __getitem__(self, item: str) -> Any:
        return self.dict()[item]

    def dict(self) -> dict[str, Any]:
        return {
            "sequence_number": self.sequence_number,
            "uid": self.uid,
            "type": self.type,
            "name": self.name,
            "name_hanja": self.name_hanja,
            "city": self.city,
            "district": self.district,
            "administrator": self.manager,
            "type_code": self.type_code,
            "city_code": self.city_code,
            "management_number": self.management_number,
            "canceled": self.canceled,
            "linkage_number": self.linkage_number,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "last_modified": self.last_modified,
        }


class HeritageSearchResult:
    """Container for list search response."""

    def __init__(self, xml_data: str) -> None:
        root = ElementTree.fromstring(xml_data)
        self.hits = _text(root, "totalCnt") or "0"
        self.limit = _text(root, "pageUnit") or "0"
        self.page_index = _text(root, "pageIndex") or "1"
        self.items = [HeritageSearchResults.from_xml(item) for item in root.findall(".//item")]

    def __getitem__(self, item: int) -> HeritageSearchResults:
        return self.items[item]

    def __iter__(self) -> Iterable[HeritageSearchResults]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def pages(self) -> int:
        hits = int(self.hits)
        limit = int(self.limit)
        return 0 if limit == 0 else (hits + limit - 1) // limit


# Backward compatibility typo in 1.x
HeritagSearchResultItem = HeritageSearchResult


class HeritageDetail:
    def __init__(self, xml_data: str, preview: HeritageSearchResults) -> None:
        root = ElementTree.fromstring(xml_data)
        item = root.find("item")

        self.uid = preview.uid
        self.name = preview.name
        self.name_hanja = preview.name_hanja
        self.city = preview.city
        self.district = preview.district
        self.canceled = preview.canceled
        self.last_modified = preview.last_modified

        self.type_code = _text(root, "ccbaKdcd")
        self.management_number = _text(root, "ccbaAsno")
        self.city_code = _text(root, "ccbaCtcd")
        self.linkage_number = _text(root, "ccbaCpno")
        self.longitude = _text(root, "longitude")
        self.latitude = _text(root, "latitude")
        self.type = _text(item, "ccmaName")
        self.category1 = _text(item, "gcodeName")
        self.category2 = _text(item, "bcodeName")
        self.category3 = _text(item, "mcodeName")
        self.category4 = _text(item, "scodeName")
        self.quantity = _text(item, "ccbaQuan")
        self.registered_date = _parse_struct_time(_text(item, "ccbaAsdt"), "%Y%m%d")
        self.location_description = _text(item, "ccbaLcad")
        self.era = _text(item, "ccceName")
        self.owner = _text(item, "ccbaPoss")
        self.manager = _text(item, "ccbaAdmin")
        self.thumbnail = _text(item, "imageUrl")
        self.content = _text(item, "content")

    def __getitem__(self, item: str) -> Any:
        return self.dict()[item]

    def dict(self) -> dict[str, Any]:
        return {
            "uid": self.uid,
            "name": self.name,
            "name_hanja": self.name_hanja,
            "city": self.city,
            "district": self.district,
            "canceled": self.canceled,
            "last_modified": self.last_modified,
            "type_code": self.type_code,
            "management_number": self.management_number,
            "city_code": self.city_code,
            "linkage_number": self.linkage_number,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "type": self.type,
            "category1": self.category1,
            "category2": self.category2,
            "category3": self.category3,
            "category4": self.category4,
            "quantity": self.quantity,
            "registered_date": self.registered_date,
            "location_description": self.location_description,
            "era": self.era,
            "owner": self.owner,
            "thumbnail": self.thumbnail,
            "content": self.content,
        }


@dataclass
class HeritageImageItem:
    licence: Optional[str]
    image_url: Optional[str]
    description: Optional[str]

    def __getitem__(self, item: str) -> Any:
        return self.dict()[item]

    def dict(self) -> dict[str, Optional[str]]:
        return {
            "image_nuri": self.licence,
            "image_url": self.image_url,
            "description": self.description,
        }


class HeritageImageSet:
    def __init__(self, xml_data: str) -> None:
        root = ElementTree.fromstring(xml_data)

        self.count = _text(root, "totalCnt")
        self.type = _text(root, "ccbaKdcd")
        self.management_number = _text(root, "ccbaAsno")
        self.city_code = _text(root, "ccbaCtcd")
        self.name = _text(root, "ccbaMnm1")
        self.name_hanja = _text(root, "ccbaMnm2")

        self.images: list[HeritageImageItem] = []
        item = root.find("item")
        if item is not None:
            for image_info in zip(item.findall("imageNuri"), item.findall("imageUrl"), item.findall("ccimDesc")):
                self.images.append(
                    HeritageImageItem(
                        image_info[0].text.strip() if image_info[0].text else None,
                        image_info[1].text.strip() if image_info[1].text else None,
                        image_info[2].text.strip() if image_info[2].text else None,
                    )
                )

    def __getitem__(self, item: int) -> HeritageImageItem:
        return self.images[item]

    def __iter__(self):
        return iter(self.images)

    def __len__(self) -> int:
        return len(self.images)


class HeritageVideoSet:
    def __init__(self, xml_data: str) -> None:
        root = ElementTree.fromstring(xml_data)

        self.count = _text(root, "totalCnt")
        self.type = _text(root, "ccbaKdcd")
        self.management_number = _text(root, "ccbaAsno")
        self.city_code = _text(root, "ccbaCtcd")
        self.name = _text(root, "ccbaMnm1")
        self.name_hanja = _text(root, "ccbaMnm2")

        self.videos: list[str] = []
        item = root.find("item")
        if item is not None:
            for node in item.findall("videoUrl"):
                if node.text is None:
                    continue
                url = node.text.strip()
                if url == "http://116.67.83.213/webdata/file_data/media_data/videos/":
                    continue
                if url:
                    self.videos.append(url)

    def __getitem__(self, item: int) -> str:
        return self.videos[item]

    def __iter__(self):
        return iter(self.videos)

    def __len__(self) -> int:
        return len(self.videos)


class HeritageEvent:
    """Data model for event API with support for legacy and current tags."""

    def __init__(self, xml_data: ElementTree.Element) -> None:
        self.sequence_number = _text(xml_data, "sn", "seqNo")
        self.event_type = _text(xml_data, "siteCode")
        self.event_name = _text(xml_data, "siteName", "subTitle")
        self.program_name = self.event_name
        self.event_description = _text(xml_data, "subContent")
        self.host_name = _text(xml_data, "groupName")
        self.contact = _text(xml_data, "contact")
        self.event_location = _text(xml_data, "subDesc")
        self.event_url = _text(xml_data, "subPath")

        # 1.x typo kept for compatibility.
        self.audiance = _text(xml_data, "subDesc1", "subDesc_2")
        self.target_audience = self.audiance

        self.etc = _text(xml_data, "subDesc2", "subDesc_3")
        self.extra_info = self.etc

        self.city = _text(xml_data, "sido")
        self.district = _text(xml_data, "gugun")
        self.time_detail = _text(xml_data, "subDate")

        self.start_date = _parse_struct_time(_text(xml_data, "sDate"), "%Y%m%d")
        self.end_date = _parse_struct_time(_text(xml_data, "eDate"), "%Y%m%d")

    def __getitem__(self, item: str) -> Any:
        return self.dict()[item]

    def dict(self) -> dict[str, Any]:
        return {
            "sequence_number": self.sequence_number,
            "event_type": self.event_type,
            "event_name": self.event_name,
            "program_name": self.program_name,
            "event_description": self.event_description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "host_name": self.host_name,
            "contact": self.contact,
            "event_location": self.event_location,
            "event_url": self.event_url,
            "audiance": self.audiance,
            "target_audience": self.target_audience,
            "etc": self.etc,
            "extra_info": self.extra_info,
            "city": self.city,
            "district": self.district,
            "time_detail": self.time_detail,
        }


@dataclass
class PalaceSearchResultItem:
    serial_number: int
    palace_code: int
    detail_code: int
    item_name: Optional[str]
    item_explanation: Optional[str]
    thubnail: Optional[str]

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "PalaceSearchResultItem":
        return cls(
            serial_number=int(_text(xml_data, "serial_number") or 0),
            palace_code=int(_text(xml_data, "gung_number") or 0),
            detail_code=int(_text(xml_data, "detail_code") or 0),
            item_name=_text(xml_data, "contents_kor"),
            item_explanation=_text(xml_data, "explanation_kor"),
            thubnail=_text(xml_data, "imgUrl"),
        )

    def dict(self) -> dict[str, Any]:
        return {
            "serial_number": self.serial_number,
            "palace_code": self.palace_code,
            "detail_code": self.detail_code,
            "item_name": self.item_name,
            "item_explanation": self.item_explanation,
            "thubnail": self.thubnail,
        }


@dataclass
class PalaceImageItem:
    index: int
    name_ko: Optional[str]
    name_en: Optional[str]
    name_ja: Optional[str]
    name_zh: Optional[str]
    explanation_ko: Optional[str]
    explanation_en: Optional[str]
    explanation_ja: Optional[str]
    explanation_zh: Optional[str]
    url: Optional[str]

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "PalaceImageItem":
        return cls(
            index=int(_text(xml_data, "imageIndex") or 0),
            name_ko=_text(xml_data, "imageContentsKor"),
            name_en=_text(xml_data, "imageContentsEng"),
            name_ja=_text(xml_data, "imageContentsJpa"),
            name_zh=_text(xml_data, "imageContentsChi"),
            explanation_ko=_text(xml_data, "imageExplanationKor"),
            explanation_en=_text(xml_data, "imageExplanationEng"),
            explanation_ja=_text(xml_data, "imageExplanationJpa"),
            explanation_zh=_text(xml_data, "imageExplanationChi"),
            url=_text(xml_data, "imageUrl"),
        )

    def dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "name_ko": self.name_ko,
            "name_en": self.name_en,
            "name_ja": self.name_ja,
            "name_zh": self.name_zh,
            "explanation_ko": self.explanation_ko,
            "explanation_en": self.explanation_en,
            "explanation_ja": self.explanation_ja,
            "explanation_zh": self.explanation_zh,
            "url": self.url,
        }


@dataclass
class PalaceVideoItem:
    index: int
    name_ko: Optional[str]
    name_en: Optional[str]
    name_ja: Optional[str]
    name_zh: Optional[str]
    url_ko: Optional[str]
    url_en: Optional[str]
    url_ja: Optional[str]
    url_zh: Optional[str]

    @classmethod
    def from_xml(cls, xml_data: ElementTree.Element) -> "PalaceVideoItem":
        return cls(
            index=int(_text(xml_data, "movieIndex") or 0),
            name_ko=_text(xml_data, "movieContentsKor"),
            name_en=_text(xml_data, "movieContentsEng"),
            name_ja=_text(xml_data, "movieContentsJpa"),
            name_zh=_text(xml_data, "movieContentsChi"),
            url_ko=_text(xml_data, "movieUrlKor"),
            url_en=_text(xml_data, "movieUrlEng"),
            url_ja=_text(xml_data, "movieUrlJpa"),
            url_zh=_text(xml_data, "movieUrlChi"),
        )

    def dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "name_ko": self.name_ko,
            "name_en": self.name_en,
            "name_ja": self.name_ja,
            "name_zh": self.name_zh,
            "url_ko": self.url_ko,
            "url_en": self.url_en,
            "url_ja": self.url_ja,
            "url_zh": self.url_zh,
        }


class PalaceDetail:
    def __init__(self, xml_data: str) -> None:
        root = ElementTree.fromstring(xml_data)

        self.serial_number = int(_text(root, "serial_number") or 0)
        self.palace_code = int(_text(root, "gung_number") or 0)
        self.detail_code = int(_text(root, "detail_code") or 0)
        self.name_ko = _text(root, "contents_kor")
        self.name_en = _text(root, "contents_eng")
        self.name_ja = _text(root, "contents_jpa")
        self.name_zh = _text(root, "contents_chi")
        self.explanation_ko = _text(root, "explanation_kor")
        self.explanation_en = _text(root, "explanation_eng")
        self.explanation_ja = _text(root, "explanation_jpa")
        self.explanation_zh = _text(root, "explanation_chi")
        self.thubnail = _text(root.find("mainImage"), "imgUrl")

        self.main_image = [(img.text or "").strip() for img in root.findall(".//listImg/image") if (img.text or "").strip()]
        self.main_video = [(mov.text or "").strip() for mov in root.findall(".//listMoving/moving") if (mov.text or "").strip()]

        self.detail_image_list = sorted(
            [PalaceImageItem.from_xml(image_info) for image_info in root.findall(".//imageList/imageInfo")],
            key=lambda x: x.index,
        )
        self.detail_video_list = sorted(
            [PalaceVideoItem.from_xml(video_info) for video_info in root.findall(".//movieList/movieInfo")],
            key=lambda x: x.index,
        )
# ===================================================== CONSTANTS =====================================================


class PalaceCode:
    GYEONGBOKGUNG = 1  # 경복궁
    CHANGDEOKGUNG = 2  # 창덕궁
    CHANGGYEONGGUNG = 3  # 창경궁
    DEOKSUGUNG = 4  # 덕수궁
    JONGMYO = 5  # 종묘


class HeritageType:
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
    REGIONAL_NATURAL_HERITAGE = '55'  # 시도자연유산
    REGIONAL_NATURAL_HERITAGE_MATERIAL = '66'  # 시도자연유산자료
    NATIONAL_REGISTERED_HERITAGE = '79'  # 국가등록문화재
    NORTH_KOREAN_INTANGIBLE_HERITAGE = '80'  # 이북5도무형문화재


class EventType:
    NIGHTTIME_HERITAGE = '01'  # 문화재야행
    VIVID_HERITAGE = '02'  # 생생문화재
    TRADITIONAL_TEMPLE_HERITAGE = '03'  # 전통산사문화재
    HYANGGYO_AND_SEOWON = '04'  # 살아숨쉬는향교서원
    NATIONAL_INTANGIBLE_HERITAGE = '07'  # 국립무형유산원
    CULTURAL_HERITAGE_FOUNDATION = '08'  # 한국문화재재단
    TRADITIONAL_HOUSES = '09'  # 고택종갓집
    WORLD_HERITAGE = '10'  # 세계유산
    OTHERS = '06'  # 기타행사


class CityCode:
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


class DistrictCode:
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
