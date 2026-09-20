Run the account window from the repository root:

```powershell
python -m virtual_library.ui.views_login
```

Set `MONGO_URI`, `MONGO_USERS_DB_NAME`, and `MONGO_ACCOUNTS_COLLECTION_NAME`
in a local `.env` file. The original `MONGO_ACCAUNTS_COLLECTION_NAME` spelling
is also accepted. Registration requires permission to create a unique username
index. Existing duplicate usernames must be resolved before that index can be created.
The regular `python main.py` command still opens the offline catalogue.

Run account regression checks with `python -m unittest discover -s tests -v`.
