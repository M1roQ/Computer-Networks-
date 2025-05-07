import json
from decimal import Decimal

import psycopg2
from psycopg2 import sql

class PSQLwriter:
    def __init__(self, user, database, table):
        try:
            self.connection = psycopg2.connect(
                dbname="products_db",
                user="postgres",
                password="BVal41790",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            self.connection = None
            self.cursor = None
        self.table = table

    def clear_table(self):
        if self.connection:
            try:
                query = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY;").format(sql.Identifier(self.table))
                self.cursor.execute(query)
                self.connection.commit()
                print(f"Таблица {self.table} успешно очищена.")
            except psycopg2.Error as e:
                print(f"Ошибка очистки таблицы: {e}")

    def write_data_to_json(self, file_path="results.json"):
        if self.connection:
            try:
                self.cursor.execute(f"SELECT * FROM {self.table};")
                column_names = [desc[0] for desc in self.cursor.description]
                rows = self.cursor.fetchall()

                data = []
                for row in rows:
                    row_dict = {}
                    for i, column_name in enumerate(column_names):
                        value = row[i]
                        if isinstance(value, Decimal):
                            value = float(value)
                        row_dict[column_name] = value
                    data.append(row_dict)

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                print(f"Данные из таблицы {self.table} успешно записаны в {file_path}.")
                return json.dumps(data)
            except psycopg2.Error as e:
                print(f"Ошибка записи данных в JSON: {e}")
                return None
