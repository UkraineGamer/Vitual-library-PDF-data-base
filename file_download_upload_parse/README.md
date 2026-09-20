Install `requirements.txt`, copy `.env.example` to `.env` in the repository
root and set `MONGO_URI`. Keep the connection string out of version control.
All storage modules use `MONGO_DB_NAME` and `MONGO_COLLECTION_NAME`.

Run `python read_and_save.py` to upload a PDF. `upload_file_gfs(path)` returns
the GridFS ID accepted by `Books_download.download_file_gfs(id, output_folder)`.
Downloads refuse to overwrite existing files. Batch discovery returns only
new PDF filenames; join each name to the input directory before uploading.

Uploads require permission to create a unique index on metadata `filename`.
Resolve existing duplicate filename records before using uploads with an old
database; index creation intentionally fails instead of discarding data.

Run the offline storage checks with `python -m unittest discover -s tests -v`.
