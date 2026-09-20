import importlib
import unittest
from unittest.mock import Mock, patch

import bcrypt
from pymongo.errors import DuplicateKeyError

from login_register.register import UserRegister


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.service = UserRegister.__new__(UserRegister)
        self.service.mongo_collection = Mock()

    def test_missing_user_never_authenticates(self):
        self.service.mongo_collection.find_one.return_value = None
        self.assertIs(self.service.login_user('missing', 'password'), False)

    def test_password_verification_and_legacy_hashes(self):
        hashed = bcrypt.hashpw(b'password', bcrypt.gensalt(rounds=4))
        for stored in (hashed, hashed.decode()):
            self.service.mongo_collection.find_one.return_value = {'password': stored}
            self.assertTrue(self.service.login_user('user', 'password'))
            self.assertFalse(self.service.login_user('user', 'wrong'))
        for stored in (None, 'broken hash'):
            self.service.mongo_collection.find_one.return_value = {'password': stored}
            self.assertFalse(self.service.login_user('user', 'password'))

    def test_registration_hashes_password_and_handles_concurrent_duplicates(self):
        self.service.mongo_collection.find_one.return_value = None
        self.assertTrue(self.service.register_user(' user ', 'password'))
        document = self.service.mongo_collection.insert_one.call_args.args[0]
        self.assertEqual(document['username'], 'user')
        self.assertTrue(bcrypt.checkpw(b'password', document['password'].encode()))
        self.service.mongo_collection.insert_one.side_effect = DuplicateKeyError('duplicate')
        self.assertFalse(self.service.register_user('user', 'password'))

    def test_rejects_invalid_credentials_before_querying(self):
        for username, password in (('', 'x'), ('user', ''), ('user', 'я' * 37), ({'$ne': None}, 'x')):
            with self.assertRaises(ValueError):
                self.service.register_user(username, password)
            self.assertFalse(self.service.login_user(username, password))
        self.service.mongo_collection.find_one.assert_not_called()

    def test_importing_login_view_does_not_open_a_window(self):
        with patch('tkinter.Tk') as root:
            importlib.import_module('virtual_library.ui.views_login')
        root.assert_not_called()


if __name__ == '__main__':
    unittest.main()
