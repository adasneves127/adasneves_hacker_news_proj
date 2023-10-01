import sqlite3


article_dict = {
    "objectID": "integer primary key",
    "created_at": "text",
    "title": "text",
    "url": "text",
    "author": "text",
    "points": "Integer",
    "num_comments": "Integer",
    "created_at_i": "Integer",
}

comment_dict = {
    "id": "integer primary key",
    "parent_id": "integer",
    "company": "text",
    "location": "text",
    "salary_low": "text",
    "salary_high": "text",
    "raw_comment": "blob",
    "foreign key(parent_id)": "references articles(objectID)",
}


class db_conn:
    def __init__(self, db_name: str):
        self.tables = {}
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def execute(self, query: str) -> None:
        try:
            self.cursor.execute(query)
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
        except Exception as e:
            print(f"SQL Syntax Error! {e}\n{query}")

    def exec_raw(self, query: str) -> list:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"SQL Syntax Error! {e}\n{query}")
            
    def query(self, table, *params):
        query = f"SELECT * FROM {table} WHERE "
        
        for param in params:
            col = param[0]
            op = param[1]
            val = param[2]
            query += f"{col} {op} {val} AND"
        
        query = query[:-3]
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
        

    def execute_with_params(self, query: str, params: list) -> None:
        try:
            self.cursor.execute(query, params)
            self.db.commit()
        except sqlite3.IntegrityError:
            pass  # The data is already in the database.
        except Exception as e:
            print(f"SQL Syntax Error! {e}\n{query} {params}")

    def create_table(self, table_name: str, table_dict: dict):
        self.tables[table_name] = table_dict
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            {','.join([f'{x} {y}' for x,y in table_dict.items()])}
            );"""

        self.execute(query)

    def insert(self, table_name: str, table_dict: dict):
        # Keep only the keys that are in the table
        filtered_dict = {
            key: table_dict.get(key)
            for key in self.tables[table_name].keys()
            if key in table_dict.keys()
        }

        query = f"""INSERT INTO {table_name} ({','.join(filtered_dict.keys())})
            VALUES ({','.join(['?' for x in filtered_dict.keys()])});"""
        self.execute_with_params(query, list(filtered_dict.values()))

    def close(self):
        self.db.commit()
        self.db.close()


if __name__ == "__main__":
    x = db_conn("test.db")
    x.create_table("test_table", {"x": "text", "y": "Integer"})
    x.insert("test_table", {"x": "test", "y": 1, "z": 4})
