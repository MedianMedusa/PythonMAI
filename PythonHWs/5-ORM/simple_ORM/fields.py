import sys

MIN_INT = -sys.maxsize - 1


class Field:
    """
    db field
    """

    def __get__(self, obj, type=None):
        if self._name in obj._data and '_value' in obj._data[self._name]:
            return obj._data[self._name]['_value']
        return self._default_value

    def __set__(self, obj, value):
        obj._data[self._name]['_value'] = value
        # не работает нахрен, всё равно значения шарятся между инстансами. ХЕЛП!!


    def to_sql(self) -> str:
        """
        :return: parameters for sql column
        """
        return self._name + ' ' + self._type


class CharField(Field):
    """
    Char field for db with length check
    """
    _name = ''
    _type = 'TEXT'
    _default_value = ''

    def __init__(self, min_length=0, max_length=255):
        self.min_length = min_length
        self.max_length = max_length

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(obj, self._name, str, value)
        if len(value) > self.max_length or len(value) < self.min_length:
            raise ValueError('value must be between {min} and {max}'.
                             format(min=self.min_length, max=self.max_length))

        super().__set__(obj, value)


class IntegerField(Field):
    """
    Integer field for db with min value check
    """
    _name = ''
    _type = 'INTEGER'
    _default_value = 0

    def __init__(self, min_value=MIN_INT):
        self.min_value = min_value
        self._default_value = min_value

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(obj, self._name, int, value)
        if value < self.min_value:
            raise ValueError('value must be more than {min}'.
                             format(min=self.min_value))
        super().__set__(obj, value)
