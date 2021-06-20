from simple_ORM import SqliteDB, Model, fields

db = SqliteDB('test.db')


class BaseModel(Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = fields.CharField(max_length=180)
    price = fields.IntegerField(min_value=0)

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


if __name__ == '__main__':
    db.connect()
    db.create_tables([Advert])

    Advert.create(title='iPhone X', price=100)
    adverts = Advert.select()
    print(adverts)
    assert 'iPhone X | 100 ₽' in str(adverts)
    db.disconnect()
