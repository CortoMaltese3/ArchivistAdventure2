from .enemy_data import monster_data
from .magic_data import magic_data
from .weapon_data import weapon_data


class BaseDataProvider:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self, table_name, schema, data_dict):
        columns_definition = ", ".join(
            [f"{column} {data_type}" for column, data_type in schema.items()]
        )

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        self.db_manager.execute_query(query)

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
    SCHEMA = {
        "name": "TEXT PRIMARY KEY",
        "cooldown": "INTEGER",
        "damage": "INTEGER",
    }

    def initialize_data(self):
        # Create the weapon table first
        self.create_table(self.TABLE_NAME, self.SCHEMA, weapon_data)

        # Insert weapon data into the table
        for name, attributes in weapon_data.items():
            data_to_insert = {
                "name": name,
                "cooldown": attributes.get("cooldown"),
                "damage": attributes.get("damage"),
            }
            self.create(self.TABLE_NAME, data_to_insert)


class MagicDataProvider(BaseDataProvider):
    TABLE_NAME = "magic"
    SCHEMA = {
        "name": "TEXT PRIMARY KEY",
        "cost": "INTEGER",
        "strength": "INTEGER",
    }

    def initialize_data(self):
        # Create the magic table first
        self.create_table(self.TABLE_NAME, self.SCHEMA, magic_data)

        # Insert magic data into the magic_data
        for name, attributes in magic_data.items():
            data_to_insert = {
                "name": name,
                "strength": attributes.get("strength"),
                "cost": attributes.get("cost"),
            }
            self.create(self.TABLE_NAME, data_to_insert)


class MonsterDataProvider(BaseDataProvider):
    TABLE_NAME = "monster"
    SCHEMA = {
        "name": "TEXT PRIMARY KEY",
        "health": "INTEGER",
        "exp": "INTEGER",
        "damage": "INTEGER",
        "attack_type": "TEXT",
        "speed": "INTEGER",
        "resistance": "INTEGER",
        "attack_radius": "INTEGER",
        "notice_radius": "INTEGER",
    }

    def initialize_data(self):
        # Create the magic table first
        self.create_table(self.TABLE_NAME, self.SCHEMA, monster_data)

        # Insert magic data into the magic_data
        for name, attributes in monster_data.items():
            data_to_insert = {
                "name": name,
                "health": attributes.get("health"),
                "exp": attributes.get("exp"),
                "damage": attributes.get("damage"),
                "attack_type": attributes.get("attack_type"),
                "speed": attributes.get("speed"),
                "resistance": attributes.get("resistance"),
                "attack_radius": attributes.get("attack_radius"),
                "notice_radius": attributes.get("notice_radius"),
            }
            self.create(self.TABLE_NAME, data_to_insert)
