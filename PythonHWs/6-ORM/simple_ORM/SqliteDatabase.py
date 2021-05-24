import sqlite3


class SqliteDatabase:
    _create_table_template = 'create table if not exists {table_name} (' \
                             '{fields});'
    _replace_template = 'replace into {table_name}({column_list}) ' \
                        'values({value_list});'
    _select_template = 'select {column_list} from {table_name};'

    def __init__(self, db_name: str):
        self.db_name = db_name

    def connect(self):
        """
        create connection to sqlite db
        :return:
        """
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        """
        close connection to sqlite db
        :return:
        """
        self.conn.close()

    def create_tables(self, entities: list):
        """
        create tables in db for entities
        :param entities:
        :return:
        """
        delimiter = ' '
        queries = [self._create_table_template.format(
            table_name=entity._name,
            fields=self.column_info(entity._data),
        ) for entity in entities]
        query = delimiter.join(queries)
        print(query)
        self.conn.execute(query)

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
        self.conn.execute(query)
        self.conn.commit()

    def select_entities(self, entity_cls: type):
        """
        :param entity_cls:
        :return: all scanned entities from db
        """
        query = self._select_template.format(
            table_name=entity_cls._name,
            column_list=self.column_list(entity_cls._data)
        )
        result = self.conn.execute(query)
        entities = []
        for row in result:
            entity = entity_cls()
            idx = 0
            for k in entity_cls._data.keys():
                setattr(entity, k, row[idx])
                idx += 1
            entities.append(entity)
        return entities

    def column_info(self, data: dict) -> str:
        """
        :param data:
        :return: column parameters for create table
        """
        delimiter = ', '
        res = [field['_meta'].to_sql() for _, field in data.items()]
        return delimiter.join(res)

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