# KHeritageAPI

KHeritageAPI is a Python wrapper designed to facilitate efficient and accurate access to Korea's rich cultural heritage
data. It simplifies the process of querying and interpreting data
from [Korea's Cultural Heritage API](https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0202.jsp&mn=NS_04_04_03),
making it an
invaluable tool for developers and researchers globally.

## Development Status

This project is currently **under active development**. While core functionalities are being implemented and tested, the
package is not yet available on PyPI. Stay tuned for updates and the official release.

## Features

- Easy-to-use interface for accessing Korea's Cultural Heritage API.
- Structured response handling for efficient data manipulation.
- Comprehensive enumeration for types, provinces, and city codes.
- Ongoing development and support for additional API functionalities.

## Installation

`pip install kheritage`

## Usage

Here's a basic example of how to use the KHeritageAPI to perform a search:

```python
from kheritageapi.api import Search, ItemDetail, EventSearch
from kheritageapi.models import CityCode, Seoul, HeritageType

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
```

## Contributing

Contributions to KHeritageAPI are welcome. If you're interested in contributing, please fork the repository and submit a
pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Developed with the enthusiasm of Jay Suh (jay@joseon.space) from the non-profit organization Joseon
Space ([joseon.space](https://joseon.space)). This module aims to provide easy access to Korea's cultural heritage for
developers and researchers around the world.