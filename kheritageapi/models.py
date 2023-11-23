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


class ProvinceCode(Enum):
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


class CityCode(Enum):
    pass


class Seoul(CityCode):
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


class Busan(CityCode):
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


class Daegu(CityCode):
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


class Incheon(CityCode):
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


class Gwangju(CityCode):
    ALL = '00'  # 전체
    DONG = '11'  # 동구
    SEO = '12'  # 서구
    BUK = '13'  # 북구
    GWANGSAN = '14'  # 광산구
    NAM = '15'  # 남구
    GWANGJU_WIDE = 'ZZ'  # 광주전역


class Daejeon(CityCode):
    ALL = '00'  # 전체
    DONG = '11'  # 동구
    JUNG = '12'  # 중구
    SEO = '13'  # 서구
    YUSEONG = '14'  # 유성구
    DAEDEOK = '15'  # 대덕구
    DAEJEON_WIDE = 'ZZ'  # 대전전역


class Ulsan(CityCode):
    ALL = '00'  # 전체
    NAM = '01'  # 남구
    DONG = '02'  # 동구
    BUK = '03'  # 북구
    JUNG = '04'  # 중구
    ULJU = '05'  # 울주군
    ULSAN_WIDE = 'ZZ'  # 울산전역


class Sejong(CityCode):
    SEJONG_WIDE = '00'  # 세종시전역


class Gyeonggi(CityCode):
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


class Gangwon(CityCode):
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


class Chungbuk(CityCode):
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


class Chungnam(CityCode):
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


class Jeonbuk(CityCode):
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


class Jeonnam(CityCode):
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


class Gyeongbuk(CityCode):
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


class Gyeongnam(CityCode):
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


class Jeju(CityCode):
    ALL = '00'  # 전체
    JEJU_CITY = '01'  # 제주시
    SEOGWIPO = '02'  # 서귀포시
    JEJU_WIDE = 'ZZ'  # 제주전역


if __name__ == '__main__':
    print(HeritageType.TREASURE.value)
    print(EventType.NIGHTTIME_HERITAGE.value)
    print(ProvinceCode.SEOUL.value)
    print(Seoul.JONGNRO.value)

