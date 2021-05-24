import json


class ColorizeMixin:
    repr_color_code = 33  # жёлтый

    def __repr__(self):
        return f'\033[1;{self.repr_color_code};1m' \
               f'{self.title} | {self.price} ₽'


class Advert(ColorizeMixin):
    def __init__(self, mapping: dict):
        self.__dict__["price_"] = 0  # дефолтное значение поля price
        for k, v in mapping.items():
            self.__setattr__(k, v)

    def __setattr__(self, key, value):
        if key == "price" and value < 0:
            raise ValueError("Invalid price - less than 0")
        if isinstance(value, dict):
            self.__setattr__(key, Advert(value))  # Неправильно. Не придумал другого
        else:
            self.__dict__[key + "_"] = value

    def __getattr__(self, item):
        return self.__dict__[item + "_"]


lesson_str = """{
  "title": "Вельш-корги",
  "class": "dogs",
  "location": {
    "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
  }
}"""

if __name__ == '__main__':
    jsonObj = json.loads(lesson_str)
    myTest = Advert(jsonObj)
    print(myTest.title)
    print(myTest.class_)
    print(myTest.location.address)
    print(myTest.price)
    print(myTest)
