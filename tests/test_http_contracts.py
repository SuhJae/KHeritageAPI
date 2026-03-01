import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from kheritageapi.heritage import EventSearcher, HeritageInfo, HeritageSearcher
from kheritageapi.models import HeritageSearchResult, HeritageVideoSet
from kheritageapi.palace import PalaceSearcher


FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class HttpContractTests(unittest.TestCase):
    def test_heritage_search_calls_expected_endpoint_and_params(self):
        searcher = HeritageSearcher(
            heritage_type="11",
            city_code="11",
            era_code="10",
            modified_start="20250101000000",
            modified_end="20251231235959",
            timeout=9,
        )

        response = SimpleNamespace(text=fixture("heritage_list.xml"), raise_for_status=Mock())
        searcher.session.get = Mock(return_value=response)

        result = searcher.perform_search()

        searcher.session.get.assert_called_once_with(
            "https://www.cha.go.kr/cha/SearchKindOpenapiList.do",
            params=searcher.params,
            timeout=9,
        )
        self.assertIsInstance(result, HeritageSearchResult)
        self.assertEqual(result.items[0].name, "서울 숭례문")

    def test_event_searcher_parses_current_tags_from_response(self):
        searcher = EventSearcher(2026, 2, timeout=7)
        response = SimpleNamespace(text=fixture("event_current.xml"), raise_for_status=Mock())
        searcher.session.get = Mock(return_value=response)

        items = searcher.perform_search()

        searcher.session.get.assert_called_once_with(
            "https://www.cha.go.kr/cha/openapi/selectEventListOpenapi.do",
            params={"searchYear": 2026, "searchMonth": 2},
            timeout=7,
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].sequence_number, "4569")
        self.assertEqual(items[0].event_name, "북악산 한양도성 자율입산제 시행 안내")

    def test_heritage_info_detail_parses(self):
        preview = HeritageSearchResult(fixture("heritage_list.xml")).items[0]
        info = HeritageInfo(preview, timeout=8)

        response = SimpleNamespace(text=fixture("heritage_detail.xml"), raise_for_status=Mock())
        info.session.get = Mock(return_value=response)

        detail = info.retrieve_detail()

        info.session.get.assert_called_once_with(
            "https://www.cha.go.kr/cha/SearchKindOpenapiDt.do",
            params={"ccbaKdcd": "11", "ccbaAsno": "0000010000000", "ccbaCtcd": "11"},
            timeout=8,
        )
        self.assertEqual(detail.type, "국보")
        self.assertEqual(detail.era, "조선 태조 7년")

    def test_palace_searcher_parses_list(self):
        searcher = PalaceSearcher(3, timeout=6)
        response = SimpleNamespace(text=fixture("palace_list.xml"), raise_for_status=Mock())
        searcher.session.get = Mock(return_value=response)

        items = searcher.perform_search()

        searcher.session.get.assert_called_once_with(
            "https://www.heritage.go.kr/heri/gungDetail/gogungListOpenApi.do",
            params={"gung_number": 3},
            timeout=6,
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].item_name, "홍화문")

    def test_video_parser_filters_placeholder_url(self):
        videos = HeritageVideoSet(fixture("heritage_video.xml"))
        self.assertEqual(videos.videos, ["http://116.67.83.213/valid.mp4"])

    def test_http_error_is_propagated(self):
        searcher = HeritageSearcher(timeout=5)
        response = SimpleNamespace(text="", raise_for_status=Mock(side_effect=RuntimeError("boom")))
        searcher.session.get = Mock(return_value=response)

        with self.assertRaises(RuntimeError):
            searcher.perform_search()


if __name__ == "__main__":
    unittest.main()
