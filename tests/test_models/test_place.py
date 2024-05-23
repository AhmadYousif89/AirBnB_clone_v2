#!/usr/bin/python3
"""Test module for Place class"""
import unittest
from models.place import Place
from models import storage_type
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id_attr(self):
        """Test Place has attr city_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        if storage_type == 'db':
            self.assertEqual(place.city_id, None)
        else:
            self.assertEqual(place.city_id, "")

    def test_user_id_attr(self):
        """Test Place has attr user_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        if storage_type == 'db':
            self.assertEqual(place.user_id, None)
        else:
            self.assertEqual(place.user_id, "")

    def test_name_attr(self):
        """Test Place has attr name, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        if storage_type == 'db':
            self.assertEqual(place.name, None)
        else:
            self.assertEqual(place.name, "")

    def test_description_attr(self):
        """Test Place has attr description, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        if storage_type == 'db':
            self.assertEqual(place.description, None)
        else:
            self.assertEqual(place.description, "")

    def test_number_rooms_attr(self):
        """Test Place has attr number_rooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        if storage_type == 'db':
            self.assertEqual(place.number_rooms, None)
        else:
            self.assertEqual(type(place.number_rooms), int)
            self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        if storage_type == 'db':
            self.assertEqual(place.number_bathrooms, None)
        else:
            self.assertEqual(type(place.number_bathrooms), int)
            self.assertEqual(place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        if storage_type == 'db':
            self.assertEqual(place.max_guest, None)
        else:
            self.assertEqual(type(place.max_guest), int)
            self.assertEqual(place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test Place has attr price_by_night, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        if storage_type == 'db':
            self.assertEqual(place.price_by_night, None)
        else:
            self.assertEqual(type(place.price_by_night), int)
            self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        if storage_type == 'db':
            self.assertEqual(place.latitude, None)
        else:
            self.assertEqual(type(place.latitude), float)
            self.assertEqual(place.latitude, 0.0)

    def test_longitude_attr(self):
        """Test Place has attr longitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        if storage_type == 'db':
            self.assertEqual(place.longitude, None)
        else:
            self.assertEqual(type(place.longitude), float)
            self.assertEqual(place.longitude, 0.0)

    @unittest.skipIf(storage_type == 'db', "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Test Place has attr amenity_ids, and it's an empty list"""
        place = Place()
        self.assertTrue(hasattr(place, "amenity_ids"))
        self.assertEqual(type(place.amenity_ids), list)
        self.assertEqual(len(place.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))
