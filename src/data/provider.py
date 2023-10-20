from .weapon_data import weapon_data as weapon_data_module
from .magic_data import magic_data as magic_data_module


class BaseDataProvider:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create(self, table_name, data_dict):
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["?"] * len(data_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(data_dict.values()))

    def read(self, table_name, condition=None):
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.db_manager.execute_query(query).fetchall()

    def update(self, table_name, data_dict, condition):
        set_values = ", ".join([f"{key} = ?" for key in data_dict.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        self.db_manager.execute_query(query, tuple(data_dict.values()))

    def delete(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.db_manager.execute_query(query)


class WeaponDataProvider(BaseDataProvider):
    TABLE_NAME = "weapon"

    def initialize_data(self):
        for weapon, attributes in weapon_data_module.weapon_data.items():
            self.create(self.TABLE_NAME, attributes)


class MagicDataProvider(BaseDataProvider):
    TABLE_NAME = "magic"

    def initialize_data(self):
        for magic, attributes in magic_data_module.magic_data.items():
            self.create(self.TABLE_NAME, attributes)
