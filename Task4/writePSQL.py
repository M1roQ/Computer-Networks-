import psycopg2

class PSQLwriter:
    def __init__(self, user, database, table):
        self.connection = psycopg2.connect(
            database=database,
            user=user,
        )
        self.cursor = self.connection.cursor()
        self.table = table

    def clear_table(self):
        self.cursor.execute(f"TRUNCATE TABLE {self.table} RESTART IDENTITY;")
        self.connection.commit()

    def write_data(self, data):
        self.cursor.executemany(f"INSERT INTO {self.table} (name, price, article, availability, link) VALUES (%s, %s, %s, %s, %s)", data)
        self.connection.commit()

    def write_data_to_json(self, file_path="results.json"):
        self.cursor.execute(f"SELECT * FROM {self.table};")
        rows = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]

        if file_path:
            with open(file_path, 'w') as file:
                json.dump(result, file, ensure_ascii=False, indent=4)

        return result
