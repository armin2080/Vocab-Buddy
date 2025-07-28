import sqlite3

class DatabaseManager:
    def __init__(self, db_name='vocab_buddy.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self,table='users', columns=['telegram_id int NOT NULL', 'username TEXT NOT NULL']):
        prompt = f'CREATE TABLE IF NOT EXISTS {table} ( ID INTEGER PRIMARY KEY AUTOINCREMENT, '
        prompt += ', '.join(columns) + ')'

        with self.conn:
            self.conn.execute(prompt)

    def add_instance(self,table, columns=None,new_vals=None):
        prompt = f'INSERT INTO {table} ('
        if columns:
            prompt += ', '.join(columns) + ') VALUES ('
            prompt += ', '.join(['?' for _ in columns]) + ')'
        
        with self.conn:
            self.conn.execute(prompt, new_vals)

    def edit_instance(self, table, columns, new_vals, where_clause, where_args):
        set_clause = ', '.join([f"{col}=?" for col in columns])
        prompt = f'UPDATE {table} SET {set_clause} WHERE {where_clause}'
        with self.conn:
            self.conn.execute(prompt, new_vals + where_args)

    def delete_instance(self, table, where_clause, where_args):
        prompt = f'DELETE FROM {table} WHERE {where_clause}'
        with self.conn:
            self.conn.execute(prompt, where_args)
    
    def fetch_all(self, table, columns='*', where_clause=None, where_args=None):
        prompt = f'SELECT {columns} FROM {table}'
        if where_clause and where_args:
            prompt += f' WHERE {where_clause}=?'
        
        with self.conn:
            cursor = self.conn.execute(prompt, where_args or [])
            return cursor.fetchall()



if __name__ == "__main__":
    db = DatabaseManager()

    db.create_table('users', ['telegram_id int NOT NULL', 'username TEXT NOT NULL'])
    print(db.fetch_all('users', columns='*', where_clause='ID', where_args=[1]))
    print("Database operations completed successfully.")