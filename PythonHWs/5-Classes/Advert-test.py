import json
import pytest
import Advert


def test_zero_price():
    lesson_str = """{
          "title": "iPhone X",
          "class": "хрень"
        }"""
    obj = Advert.Advert(json.loads(lesson_str))
    assert obj.price == 0


def test_wrong_price():
    lesson_str = """{
          "title": "iPhone X",
          "price": -100
        }"""
    with pytest.raises(ValueError):
        obj = Advert.Advert(json.loads(lesson_str))


def test_ok():
    lesson_str = """{
      "title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }"""
    obj = Advert.Advert(json.loads(lesson_str))
    expected = "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
    assert obj.location.address == expected


def test_class_ok():
    lesson_str = """{
      "title": "Вельш-корги",
      "price": 1000,
      "class": "dogs",
      "location": {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
      }
    }"""
    obj = Advert.Advert(json.loads(lesson_str))
    expected = "dogs"
    assert obj.class_ == expected


def test_none():
    with pytest.raises(AttributeError):
        obj = Advert.Advert(None)
