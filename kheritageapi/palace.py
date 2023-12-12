#
# Additional module for the Gung API.
#
# Official API Documentation:
# https://www.cha.go.kr/html/HtmlPage.do?pg=/publicinfo/pbinfo3_0301.jsp&mn=NS_04_04_03
#
# Developed with the enthusiasm of Jay Suh (jay@joseon.space) from the non-profit organization Joseon Space
# (https://joseon.space). This module aims to facilitate efficient and accurate access  to Korea's rich cultural
# heritage data for developers and researchers globally.
#

# heri/gungDetail/gogungDetailOpenApi.do

import requests
from .models import PalaceSearchResultItem, PalaceDetail, PalaceCode
from xml.etree import ElementTree


class PalaceAPIBase:
    """Base class that includes the global origin URL and a method to send a GET request to the API."""

    ORIGIN_URL = 'https://www.heritage.go.kr/'

    def __init__(self) -> None:
        """ Initializes the session object for the API."""
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        """ Sends a GET request to the API.

        :param endpoint: Endpoint of the API.
        :param params: Parameters to be sent with the request.
        :return: Requests response object.
        """
        response = self.session.get(self.ORIGIN_URL + endpoint, params=params)
        response.raise_for_status()
        return response


class PalaceSearcher(PalaceAPIBase):
    """Searches for cultural heritage items using various parameters."""

    ENDPOINT = 'heri/gungDetail/gogungListOpenApi.do'

    def __init__(self, palace: PalaceCode) -> None:
        """ Initializes the search parameters.

        :param palace: Palace code of the heritage.
        """
        super().__init__()

        self.params = {'gung_number': palace}

    def perform_search(self) -> list[PalaceSearchResultItem]:
        """ Sends a GET request to the API and returns the results.

        :return: List of PalaceResultItems objects.
        """

        response = self._get(self.ENDPOINT, self.params)
        root = ElementTree.fromstring(response.text)
        elements = root.findall('list')

        # print(response.text)

        search_result = []

        for search_item in elements:
            search_result.append(PalaceSearchResultItem(search_item))

        return search_result


class PalaceInfo(PalaceAPIBase):
    """Retrive detailed information of a cultural heritage item form the search result."""

    ENDPOINT = 'heri/gungDetail/gogungDetailOpenApi.do'

    def __init__(self, preview: PalaceSearchResultItem) -> None:
        """ Initializes the search parameters.

        :param preview: PalaceResultItems object.
        """
        super().__init__()

        self.params = {'serial_number': preview.serial_number, 'gung_number': preview.palace_code,
                       'detail_code': preview.detail_code}

    def retrieve_details(self) -> PalaceDetail:
        """ Sends a GET request to the API and returns the results.

        :return: List of PalaceResultItems objects.
        """

        response = self._get(self.ENDPOINT, self.params)
        return PalaceDetail(response.text)


# Example usage:
if __name__ == '__main__':
    search = PalaceSearcher(PalaceCode.GYEONGBOKGUNG)
    items = search.perform_search()
    for item in items:
        detail = PalaceInfo(item)
        print(detail.retrieve_details())
