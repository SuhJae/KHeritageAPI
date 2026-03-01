import unittest

import kheritageapi
from kheritageapi.heritage import HeritageSearcher


class ClientParameterTests(unittest.TestCase):
    def test_searcher_maps_new_optional_params(self):
        searcher = HeritageSearcher(
            era_code="10",
            modified_start="20250101000000",
            modified_end="20251231235959",
        )
        self.assertEqual(searcher.params["ccbaPcd1"], "10")
        self.assertEqual(searcher.params["stRegDt"], "20250101000000")
        self.assertEqual(searcher.params["enRegDt"], "20251231235959")

    def test_searcher_uses_https_origin(self):
        searcher = HeritageSearcher()
        self.assertTrue(searcher.ORIGIN_URL.startswith("https://"))


class ExportTests(unittest.TestCase):
    def test_top_level_exports(self):
        self.assertTrue(hasattr(kheritageapi, "HeritageSearcher"))
        self.assertTrue(hasattr(kheritageapi, "EventSearcher"))
        self.assertTrue(hasattr(kheritageapi, "PalaceSearcher"))
        self.assertEqual(kheritageapi.__version__, "2.0.0")


if __name__ == "__main__":
    unittest.main()
