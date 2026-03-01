# KHeritageAPI

KHeritageAPI is a Python wrapper designed to facilitate efficient and accurate access to Korea's rich cultural heritage
data. It simplifies the process of querying and interpreting data from [Korea's Cultural Heritage API](https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0202.jsp&mn=NS_04_04_03).

KHeritageAPI는 문화재청이 제공하는 [한국 문화유산 API](https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0202.jsp&mn=NS_04_04_03)를
위한 Python 래퍼입니다. 이 래퍼는 한국의 풍부한 문화유산 데이터에 효율적이고 정확하게 접근할 수 있도록 돕습니다.

## Development Status | 개발 상태 🛠️

This project is now maintained as a stable package and tracks the current 국가유산청 API schema, including event response compatibility updates added in 2.0.

이 프로젝트는 현재 안정적으로 유지보수되고 있으며, 2.0에서 국가유산청 최신 API 스키마(행사 응답 필드 변경 포함)를 반영했습니다.

## Installation | 설치 💿

KHeritageAPI is available on PyPI. You can install it with pip:

KHeritageAPI는 PyPI에 등록되어 있습니다. pip를 통해 설치할 수 있습니다:

`pip install kheritage`

## Features | 기능 🧰

### Easy-to-use, intuitive interface | 사용하기 쉬운 직관적인 인터페이스 💡

Instead of manually constructing the query URL with annigmatic parameters, you can simply create a `Search` object and
use predefined enumerations that actually make sense. Also this will return a `SearchResult` object that contains
all the information you need with a variable name that actually makes sense.

알 수 없는 매개변수로 직접 쿼리 URL을 만드는 대신, `Search` 객체를 만들고 의미있는 미리 정의된 열거형을 사용할 수 있습니다.
또한, 이는 의미있는 변수 이름으로 모든 정보를 담고 있는 `SearchResult` 객체를 반환하여 바로 사용할 수 있습니다.

**Before | 이전 😭**
```Python
import requests

base_url = "https://www.cha.go.kr/cha/SearchKindOpenapiList.do"
paramter = {"stCcbaAsdt": 2020, "stCcbaAedt": 2020, "ccbaCtcd": 11, "ccbaKdcd": 11, "ccbaCndt": 1, "pageUnit": 15, "pageIndex": 1}
response = requests.get(base_url, params=paramter)
```

**After | 이후 🤣**
```Python
from kheritageapi.heritage import HeritageSearcher
from kheritageapi.models import CityCode, Seoul, HeritageType

search = HeritageSearcher(result_count=15, city_code=CityCode.SEOUL, district_code=Seoul.JONGNRO, canceled=False,
                heritage_type=HeritageType.HISTORIC_SITE)

result = search.perform_search()
```

### Structured response handling | 구조화된 응답 처리 ✅
You don't need to parse the response in XML. The response is already parsed and structured into a object like
`SearchResult`, `ItemDetail`, `Event`, and more. This will boost your productivity via auto-completion and type hints
provided by your IDE, eliminating the need to refer to the documentation every time you use the API.
Also, all the objects has __str__ method, so you can print them directly in friendly format for debugging.

더이상 XML로 응답을 파싱할 필요가 없습니다. 응답은 이미 파싱되어 `SearchResult`, `ItemDetail`, `Event` 등과 같은 객체로 구조화되어 있습니다.
이는 IDE에서 제공하는 자동 완성과 타입 힌트를 통해 생산성을 높여주며, API를 사용할 때마다 문서를 참조할 필요가 없습니다.
또한, 모든 객체는 __str__ 메소드를 가지고 있으므로, 디버깅을 위해 친숙한 형식으로 바로 출력할 수 있습니다.

**Before | 이전 😭**
```Python
def parse_search_response(xml_response):
    root = ET.fromstring(xml_response)
    hits = root.find("totalCnt").text
    limit = hits.find("pageUnit").text
    offset = hits.find("pageIndex").text
    
    ...
    
    return SearchResult(hits, limit, offset, items ...)

response = requests.get(base_url, params=paramter)
hits, limit, offset, items ... = parse_search_response(response.text)

print(hits)
print(limit)
print(offset)
```


**After | 이후 🤣**
```Python
# Commit search alredy returns a SearchResult object ready to use!
# 검색 결과는 이미 바로 사용할 수 있는 SearchResult 객체로 반환됩니다!
result = search.perform_search() 

print(result.hits)
print(result.limit)
print(result.offset)
```

### Comprehensive enumeration support | 포괄적인 열거형 지원 📋
Enumerations provided eliminate the need to refer to the documentation every time you use the API, and
eliminates the possibility of making a typo! Also, this will boost your productivity via auto-completion and type hints.

이 패키지에서 제공하는 열거형은 API를 사용할 때마다 문서를 참조할 필요를 없애주며, 오타를 낼 가능성을 없애줍니다!
또한, 이는 IDE에서 제공하는 자동 완성과 타입 힌트를 통해 생산성을 높여줍니다.

**Before | 이전 😭**
```Python
# What is 11? What is 1? What is stCcbaAsdt? What is stCcbaAedt??? 😭
# 11은 무엇인가요? 1은 무엇인가요? stCcbaAsdt는 무엇인가요? stCcbaAedt는 무엇인가요??? 😭

paramter = {"stCcbaAsdt": 2020, "stCcbaAedt": 2020, "ccbaCtcd": 11, "ccbaKdcd": 11, "ccbaCndt": 1, "pageUnit": 15, "pageIndex": 1}
```

**After | 이후 🤣**
```Python
# Oh, we are querying for 2020, December, in Seoul's Jongno district, for 15 historic sites!
# 아, 우리는 2020년 12월, 서울 종로구에 있는 15개의 역사적 유적을 검색하고 있군요!

HeritageSearcher(result_count=15, city_code=CityCode.SEOUL, district_code=Seoul.JONGNRO, canceled=False,
                heritage_type=HeritageType.HISTORIC_SITE)

```

## Example | 사용 예시 📃

Search for 15 historic sites in Seoul's Jongno district, and search for detailed information on the first item, then print it.

서울 종로구에 있는 15개의 역사적 유적을 검색하고, 첫 번째 항목에 대한 상세 정보를 검색하여 출력하기

```python
from kheritageapi.heritage import HeritageSearcher, HeritageInfo
from kheritageapi.models import CityCode, Seoul, HeritageType

# Search for 15 historic sites in Seoul's Jongno district
# 서울 종로구에 있는 15개의 역사적 유적을 검색하기
search = HeritageSearcher(result_count=15, city_code=CityCode.SEOUL, district_code=Seoul.JONGNRO, canceled=False,
                          heritage_type=HeritageType.HISTORIC_SITE)
result = search.perform_search()

# Get detailed information on the first item
# 첫 번째 항목에 대한 상세 정보 가져오기
detail = HeritageInfo(result.items[0])
detail_info = detail.retrieve_detail()
print(detail_info)

# Also, you can get images and videos of the item
# 또한, 항목의 이미지와 동영상을 가져올 수 있습니다
images = detail.retrieve_image()
print(images)

videos = detail.retrieve_video()
print(videos)
```

Use optional filtering parameters introduced for newer docs fields (`ccbaPcd1`, `stRegDt`, `enRegDt`):

최신 문서 필드(`ccbaPcd1`, `stRegDt`, `enRegDt`)를 위한 선택 파라미터도 사용할 수 있습니다:

```python
from kheritageapi.heritage import HeritageSearcher

search = HeritageSearcher(
    era_code="10",                    # ccbaPcd1
    modified_start="20250101000000",  # stRegDt
    modified_end="20251231235959",    # enRegDt
)
```

Search for events in December 2023, and print detailed information for the all the items.

2023년 12월에 있는 행사를 검색하고, 검색 결과를 출력하기

```python
from kheritageapi.heritage import EventSearcher

event_search = EventSearcher(2023, 12)
events = event_search.perform_search()
for event in events:
    print(event)
```

Seatch for all items in Gyenbokgung Palace, and print detailed information for the all the items.

경복궁에 있는 모든 항목을 검색하고, 검색 결과를 출력하기

```python
from kheritageapi.palace import PalaceSearcher, PalaceInfo
from kheritageapi.models import PalaceCode

search = PalaceSearcher(PalaceCode.GYEONGBOKGUNG)
items = search.perform_search()
for item in items:
    detail = PalaceInfo(item)
    print(detail.retrieve_details())
```

## Contributing | 기여하기 🤝

Contributions to KHeritageAPI are welcome. If you're interested in contributing, please fork the repository and submit a
pull request with your changes! 🥰

KHeritageAPI에 기여하는 것을 환영합니다. 기여하고 싶으시다면, 저장소를 포크하고 변경 사항을 반영한 풀 리퀘스트를 제출해주세요! 🥰

## License | 라이선스 ⚖️

This project is licensed under the [MIT License](LICENSE).

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## Acknowledgements | 정보 ℹ️

Developed with the enthusiasm of Jay Suh (jay@joseon.space) from the non-profit organization Joseon
Space ([joseon.space](https://joseon.space)). This module aims to provide easy access to Korea's cultural heritage for
developers and researchers around the world.

비영리 단체 조선 스페이스([joseon.space](https://joseon.space))의 서재웅 (jay@joseon.space)의 열정으로 개발된 프로젝트 입니다.
이 모듈은 전 세계의 개발자와 연구자들이 한국의 문화유산에 쉽게 접근할 수 있도록 목표로 합니다.
