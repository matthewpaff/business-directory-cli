from copy import deepcopy
from pathlib import Path
import unittest

from directory_lab.core import query_directory
from directory_lab.fixture_check import check


class DirectoryTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{"id": key, "name": name, "city": "Town", "category": "cafe"} for key, name in ((9, "Nine"), (2, "Two%"), (5, "Five"))]

    def test_keyset_pages_have_no_overlaps_and_terminal_cursor(self):
        first = query_directory({"businesses": self.rows, "limit": 2})
        second = query_directory({"businesses": self.rows, "limit": 2, "after_id": first["next_cursor"]})
        self.assertEqual([row["id"] for row in first["items"]], [2, 5])
        self.assertEqual([row["id"] for row in second["items"]], [9])
        self.assertIsNone(second["next_cursor"])

    def test_literal_search_and_case_insensitive_filter(self):
        result = query_directory({"businesses": self.rows, "search": "%", "city": "TOWN"})
        self.assertEqual([row["id"] for row in result["items"]], [2])
        self.assertEqual(query_directory({"businesses": self.rows, "search": "' OR 1=1 --"})["items"], [])

    def test_validation_and_input_is_not_modified(self):
        original = deepcopy(self.rows)
        query_directory({"businesses": self.rows})
        self.assertEqual(self.rows, original)
        for data in ({"businesses": self.rows, "limit": True}, {"businesses": self.rows, "after_id": -1}, {"businesses": [self.rows[0], self.rows[0]]}):
            with self.assertRaises(ValueError):
                query_directory(data)

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", query_directory), 350)


if __name__ == "__main__":
    unittest.main()
