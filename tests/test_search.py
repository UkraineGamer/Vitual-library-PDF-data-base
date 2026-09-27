import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

import requests

from virtual_library.services.book_search import BookSearch


class SearchTests(unittest.TestCase):
    @patch('virtual_library.services.book_search.requests.get')
    def test_handles_network_and_malformed_responses(self, get):
        search = BookSearch()
        self.assertEqual(search.search_books(' '), [])
        get.assert_not_called()
        get.side_effect = requests.Timeout()
        self.assertEqual(search.search_books('book'), [])
        get.side_effect = None
        get.return_value.json.side_effect = ValueError('invalid JSON')
        self.assertEqual(search.search_books('book'), [])
        get.return_value.json.side_effect = None
        for payload in (None, [], {'docs': None}, {'docs': [None, 1]}):
            get.return_value.json.return_value = payload
            self.assertEqual(search.search_books('book'), [])

    @patch('virtual_library.services.book_search.requests.get')
    def test_normalizes_optional_fields_and_deduplicates_results(self, get):
        book = {'key': '/works/one', 'title': None, 'author_name': None, 'isbn': None}
        get.return_value.json.return_value = {'docs': [book, book, {'author_name': 'Author', 'isbn': 'invalid'}]}
        results = BookSearch().search_books('book')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 'ol-one')
        self.assertIsInstance(results[0]['title'], str)
        self.assertEqual(results[1]['author'], 'Author')
        self.assertEqual(results[1]['isbn'], '—')

    def test_database_search_matches_uploaded_filenames_as_literal_text(self):
        spec = importlib.util.spec_from_file_location('database_search', Path(__file__).resolve().parents[1] / 'Search and display books.py')
        module = importlib.util.module_from_spec(spec)
        with patch('pymongo.MongoClient') as client:
            spec.loader.exec_module(module)
            app = module.LibraryApp()
        client.assert_not_called()
        app.collection = Mock()
        app.collection.find.return_value = [{'filename': 'book[1].pdf'}]
        self.assertEqual(len(app.search_books('book[1]')), 1)
        query = app.collection.find.call_args.args[0]
        self.assertEqual(query['$or'][1]['filename']['$regex'], r'book\[1\]')
        self.assertEqual(app.download_by_id(None), 'Invalid file ID.')


if __name__ == '__main__':
    unittest.main()
