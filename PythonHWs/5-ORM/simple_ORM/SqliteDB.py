import sqlite3


class SqliteDB:
    _create_table_template = 'create table if not exists {table_name} (' \
                             '{fields});'
    _replace_template = 'replace into {table_name}({column_list}) ' \
                        'values({value_list});'
    _select_template = 'select {column_list} from {table_name};'
    _unique_index_template = 'create unique index if not exists {index_name} ' \
                             'on {table_name} ({position_name})'

    def __init__(self, db_name: str):
        self.db_name = db_name

    def connect(self):
        """
        create connection to sqlite db
        :return:
        """
        self.connection = sqlite3.connect(self.db_name)

    def disconnect(self):
        """
        close connection to sqlite db
        :return:
        """
        self.connection.close()

    def create_tables(self, entities: list):
        """
        create tables in db for entities
        :param entities:
        :return:
        """
        queries = []
        for entity in entities:
            queries.append(self._create_table_template.format(
                table_name=entity._name,
                fields=self.column_info(entity._data)
            ))
            queries.append(self._unique_index_template.format(
                index_name='unique_' + self.main_field(entity),
                position_name=self.main_field(entity),
                table_name=entity._name,
            ))

        for query in queries:
            self.connection.execute(query)
        self.connection.commit()

    def save_entity(self, entity: object):
        """
        insert or update entity in db
        :param entity:
        :return:
        """
        query = self._replace_template.format(
            table_name=entity._name,
            column_list=self.column_list(entity._data),
            value_list=self.column_values(entity._data)
        )
        self.connection.execute(query)
        self.connection.commit()

    def select_entities(self, entity_cls: type):
        """
        :param entity_cls:
        :return: all scanned entities from db
        """
        query = self._select_template.format(
            table_name=entity_cls._name,
            column_list=self.column_list(entity_cls._data)
        )
        result = self.connection.execute(query)
        entities = []
        for row in result:
            print(row)
            entity = entity_cls()
            idx = 0
            for k in entity_cls._data.keys():
                entity.k = row[idx]
                # setattr(entity, k, row[idx])
                idx += 1
            entities.append(entity)
        return entities

    def main_field(self, entity: dict) -> str:
        """
        :rtype: str
        :param entity:
        :return: main field name of a table (asserting it is the first)
        """
        values = list(entity._data.values())
        return values[0]['_meta']._name

    def column_info(self, data: dict) -> str:
        """
        :param data:
        :return: column parameters for create table
        """
        res = [field['_meta'].to_sql() for field in data.values()]
        return ', '.join(res)

    def column_list(self, data: dict) -> str:
        """
        :param data:
        :return: list of columns for entity
        """
        delimiter = ', '
        res = [field_name for field_name in data.keys()]
        return delimiter.join(res)

    def column_values(self, data: dict) -> str:
        """
        :param data:
        :return: values of entity for insert query
        """
        delimiter = ', '
        res = []
        for _, field in data.items():
            if isinstance(field['_value'], str):
                res.append('\'' + field['_value'] + '\'')
            else:
                res.append(str(field['_value']))
        return delimiter.join(res)
