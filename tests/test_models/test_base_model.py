#!/usr/bin/python3
"""Test BaseModel class"""
import time
import unittest
import unittest.mock
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """ """

    def test_instantiation(self):
        """Test that object is correctly created"""
        obj = BaseModel()
        self.assertIs(type(obj), BaseModel)
        obj.name = "Holberton"
        obj.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int,
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, obj.__dict__)
                self.assertIs(type(obj.__dict__[attr]), typ)
        self.assertEqual(obj.name, "Holberton")
        self.assertEqual(obj.number, 89)

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        tic = datetime.now()
        inst1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)

    def test_updated_at(self):
        """Test that updated_at attribute is updated"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for obj in [inst1, inst2]:
            uuid = str(obj.id)  # Convert uuid to string
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(
                    uuid,
                    '^[0-9a-f]{8}-[0-9a-f]{4}'
                    '-[0-9a-f]{4}-[0-9a-f]{4}'
                    '-[0-9a-f]{12}$',
                )
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "my_number",
            "__class__",
        ]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        obj = BaseModel()
        string = "[BaseModel] ({}) {}".format(obj.id, obj.__dict__)
        self.assertEqual(string, str(obj))

    @unittest.mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        obj = BaseModel()
        old_created_at = obj.created_at
        old_updated_at = obj.updated_at
        obj.save()
        new_created_at = obj.created_at
        new_updated_at = obj.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
