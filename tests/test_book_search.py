import unittest
from unittest.mock import Mock, patch

import requests

from virtual_library.services import BookSearch


class BookSearchTests(unittest.TestCase):
    @patch("virtual_library.services.book_search.requests.get")
    def test_maps_open_library_result(self, get: Mock) -> None:
        response = Mock()
        response.json.return_value = {"docs": [{"key": "/works/OL1W", "title": "Test", "author_name": ["Author"]}]}
        get.return_value = response

        result = BookSearch().search_books("Test")

        self.assertEqual(result[0]["id"], "ol-OL1W")
        self.assertEqual(result[0]["categories"], ["Усі"])

    @patch("virtual_library.services.book_search.requests.get", side_effect=requests.RequestException)
    def test_returns_empty_list_when_request_fails(self, _get: Mock) -> None:
        self.assertEqual(BookSearch().search_books("Test"), [])


if __name__ == "__main__":
    unittest.main()
