import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from file_download_upload_parse.upload import Books_upload
from file_download_upload_parse.download import Books_download
from file_download_upload_parse.db_parse import BookDB_parse


class StorageTests(unittest.TestCase):
    def test_upload_returns_gridfs_id_and_rejects_duplicates(self):
        uploader = Books_upload.__new__(Books_upload)
        uploader.mongo_collection = Mock()
        uploader.mongo_collection.find_one.return_value = None
        uploader.fs = Mock()
        file_id = ObjectId()
        uploader.fs.put.return_value = file_id
        with TemporaryDirectory() as folder:
            pdf = Path(folder) / 'book.pdf'
            pdf.write_bytes(b'%PDF-1.4\n')
            self.assertEqual(uploader.upload_file_gfs(pdf), file_id)
            uploader.mongo_collection.find_one.assert_called_with({'filename': 'book.pdf'})
            uploader.mongo_collection.find_one.return_value = {'filename': 'book.pdf'}
            with self.assertRaises(FileExistsError):
                uploader.upload_file_gfs(pdf)
            uploader.fs.put.assert_called_once()
            uploader.mongo_collection.find_one.return_value = None
            for error in (RuntimeError('insert failed'), DuplicateKeyError('duplicate')):
                uploader.mongo_collection.insert_one.side_effect = error
                with self.assertRaises((RuntimeError, FileExistsError)):
                    uploader.upload_file_gfs(pdf)
                uploader.fs.delete.assert_called_with(file_id)
            pdf.write_bytes(b'not a PDF')
            with self.assertRaises(ValueError):
                uploader.upload_file_gfs(pdf)

    def test_download_rejects_paths_and_preserves_existing_files(self):
        downloader = Books_download.__new__(Books_download)
        downloader.fs = Mock()
        file_id = ObjectId()
        with TemporaryDirectory() as folder:
            for invalid in (None, {}, [], 'invalid'):
                with self.assertRaises(ValueError):
                    downloader.download_file_gfs(invalid, folder)
            downloader.fs.get.assert_not_called()
            for filename in ('../outside.pdf', r'..\outside.pdf', '/outside.pdf', r'C:\outside.pdf', 'file:stream', None):
                data = io.BytesIO(b'PDF')
                data.filename = filename
                downloader.fs.get.return_value = data
                with self.assertRaises(ValueError):
                    downloader.download_file_gfs(file_id, folder)
                self.assertEqual(list(Path(folder).iterdir()), [])
            for _ in range(2):
                data = io.BytesIO(b'PDF')
                data.filename = 'book.pdf'
                downloader.fs.get.return_value = data
                if (Path(folder) / 'book.pdf').exists():
                    with self.assertRaises(FileExistsError):
                        downloader.download_file_gfs(file_id, folder)
                else:
                    result = downloader.download_file_gfs(str(file_id), folder)
                    self.assertEqual(result.read_bytes(), b'PDF')

    def test_failed_download_removes_partial_file(self):
        downloader = Books_download.__new__(Books_download)
        data = io.BytesIO(b'PDF')
        data.filename = 'book.pdf'
        downloader.fs = Mock()
        downloader.fs.get.return_value = data
        with TemporaryDirectory() as folder, patch('file_download_upload_parse.download.copyfileobj', side_effect=OSError('read failed')):
            with self.assertRaises(OSError):
                downloader.download_file_gfs(ObjectId(), folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_mass_upload_only_returns_new_pdf_files(self):
        parser = BookDB_parse.__new__(BookDB_parse)
        parser.mongo_collection = Mock()
        parser.mongo_collection.find.return_value = [{'filename': 'old.pdf'}, {}]
        with TemporaryDirectory() as folder:
            for name in ('old.pdf', 'new.PDF', 'text.txt'):
                (Path(folder) / name).touch()
            (Path(folder) / 'directory.pdf').mkdir()
            self.assertEqual(parser.for_mass_upload(folder), ['new.PDF'])


if __name__ == '__main__':
    unittest.main()
