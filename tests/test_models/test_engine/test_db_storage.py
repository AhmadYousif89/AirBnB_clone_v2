#!/usr/bin/python3
"""Module for testing database storage"""
import unittest
from models import storage
import os


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'file',
    'Not testing db storage. Using file storage.    ',
)
class test_DBStorage(unittest.TestCase):
    """Class to test the file storage method"""

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""
