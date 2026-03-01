import unittest

from kheritageapi.models import HeritageEvent, HeritageSearchResult
from xml.etree import ElementTree


class HeritageEventCompatibilityTests(unittest.TestCase):
    def test_parses_current_event_tags(self):
        xml = """
        <item>
          <seqNo>101</seqNo>
          <siteCode>08</siteCode>
          <subTitle>Modern Program</subTitle>
          <subContent>Description</subContent>
          <sDate>20260101</sDate>
          <eDate>20260131</eDate>
          <groupName>Host</groupName>
          <contact>02-0000-0000</contact>
          <subDesc>Seoul</subDesc>
          <subPath>https://example.com</subPath>
          <subDesc_2>Adults</subDesc_2>
          <subDesc_3>Reservation required</subDesc_3>
          <sido>서울특별시</sido>
          <gugun>종로구</gugun>
          <subDate>2026.01.01 ~ 2026.01.31</subDate>
        </item>
        """
        event = HeritageEvent(ElementTree.fromstring(xml))

        self.assertEqual(event.sequence_number, "101")
        self.assertEqual(event.event_name, "Modern Program")
        self.assertEqual(event.audiance, "Adults")
        self.assertEqual(event.etc, "Reservation required")

    def test_parses_legacy_event_tags(self):
        xml = """
        <item>
          <sn>55</sn>
          <siteCode>01</siteCode>
          <siteName>Legacy Program</siteName>
          <subContent>Description</subContent>
          <sDate>20251201</sDate>
          <eDate>20251231</eDate>
          <subDesc1>Family</subDesc1>
          <subDesc2>None</subDesc2>
        </item>
        """
        event = HeritageEvent(ElementTree.fromstring(xml))

        self.assertEqual(event.sequence_number, "55")
        self.assertEqual(event.event_name, "Legacy Program")
        self.assertEqual(event.audiance, "Family")
        self.assertEqual(event.etc, "None")


class HeritageSearchResultRobustnessTests(unittest.TestCase):
    def test_handles_sparse_item_without_crash(self):
        xml = """
        <result>
          <totalCnt>1</totalCnt>
          <pageUnit>10</pageUnit>
          <pageIndex>1</pageIndex>
          <item>
            <sn>1</sn>
            <ccbaMnm1>Only Name</ccbaMnm1>
          </item>
        </result>
        """
        result = HeritageSearchResult(xml)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].name, "Only Name")
        self.assertIsNone(result.items[0].uid)

    def test_pages_uses_ceil(self):
        xml = """
        <result>
          <totalCnt>20</totalCnt>
          <pageUnit>10</pageUnit>
          <pageIndex>1</pageIndex>
        </result>
        """
        result = HeritageSearchResult(xml)
        self.assertEqual(result.pages(), 2)


if __name__ == "__main__":
    unittest.main()
