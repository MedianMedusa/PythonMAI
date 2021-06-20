from .Model_meta import ModelMeta


class Model(metaclass=ModelMeta):
    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @classmethod
    def create(cls, **query):
        """
        create model in db
        :param query:
        :return:
        """
        inst = cls(**query)
        inst.save()
        return inst

    @classmethod
    def select(cls):
        """
        :return: models from db
        """
        return cls.database.select_entities(cls)

    def save(self):
        """
        save models data to db
        :return:
        """
        self.database.save_entity(self)
