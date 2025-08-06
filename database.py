import sqlite3, math, random
from datetime import datetime
import pandas as pd


def compute_score(review_count, last_reviewed, now=None):
    now = now or datetime.now()
    days_since_last = (now - last_reviewed).days + 1  # +1 to avoid division by zero
    time_score = math.log(days_since_last + 1)        # grows slowly over time
    review_score = 1 / (review_count + 1)              # lower count = higher score
    return time_score * review_score

def normalize_scores(words):
    total_score = sum(w['score'] for w in words)
    for w in words:
        w['prob'] = w['score'] / total_score
    return words


def select_words(words, k=5):
    # Ensure we don't try to select more words than available
    k = min(k, len(words))
    
    # Create a list to store selected words
    selected = []
    remaining_words = words.copy()
    
    for _ in range(k):
        if not remaining_words:
            break
            
        # Calculate total probability for remaining words
        total_prob = sum(w['prob'] for w in remaining_words)
        
        # Renormalize probabilities
        for w in remaining_words:
            w['normalized_prob'] = w['prob'] / total_prob
        
        # Select one word based on probability
        rand_val = random.random()
        cumulative_prob = 0
        
        for i, word in enumerate(remaining_words):
            cumulative_prob += word['normalized_prob']
            if rand_val <= cumulative_prob:
                selected.append(word)
                remaining_words.pop(i)
                break
    
    return selected



class DatabaseManager:
    def __init__(self, db_name='vocab_buddy.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.initialize_tables()

    def initialize_tables(self):
        """Initialize all required tables with proper schema"""
        # Create users table with created_at timestamp
        self.create_table('users', [
            'telegram_id INTEGER NOT NULL UNIQUE',
            'username TEXT',
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ])
        
        
        # Create words table
        self.create_table('words', [
            'word TEXT NOT NULL UNIQUE',
            'translation TEXT NOT NULL',
            'cefr_level TEXT NOT NULL',
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ])
        
        # Create words_users junction table
        self.create_table('words_users', [
            'user_id INTEGER NOT NULL',
            'word_id INTEGER NOT NULL',
            'review_count INTEGER DEFAULT 0',
            'last_reviewed TIMESTAMP',
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'FOREIGN KEY (user_id) REFERENCES users (telegram_id)',
            'FOREIGN KEY (word_id) REFERENCES words (id)',
            'UNIQUE(user_id, word_id)'
        ])
        
        # Check and add missing columns for existing databases
        self.upgrade_schema()

    def upgrade_schema(self):
        """Add missing columns to existing tables"""
        try:
            # Check if created_at column exists in users table
            cursor = self.conn.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'created_at' not in columns:
                # Add created_at column to existing users table
                self.conn.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                # Update existing records with current timestamp
                self.conn.execute("UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
                self.conn.commit()
                print("✅ Added created_at column to users table")
                
        except sqlite3.OperationalError as e:
            # Table might not exist yet, which is fine
            pass

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
            # Check if where_clause already contains operators (like = or AND)
            if '=' in where_clause or 'AND' in where_clause or 'OR' in where_clause:
                prompt += f' WHERE {where_clause}'
            else:
                # Legacy behavior for simple column name
                prompt += f' WHERE {where_clause}=?'
        
        with self.conn:
            cursor = self.conn.execute(prompt, where_args or [])
            return cursor.fetchall()
        
    def choose_words(self,user_id, k=5):
        rows = self.fetch_all('words_users',where_clause='user_id', where_args=[user_id])
        
        # Create a dictionary to ensure unique word_ids
        unique_words = {}
        for row in rows:
            word_id = row[2]
            # Only keep the first occurrence of each word_id
            if word_id not in unique_words:
                unique_words[word_id] = {
                    'user_id': row[1],
                    'word_id': word_id,
                    'review_count': row[3],
                    'last_reviewed': datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
                    'active': row[5]
                }
        
        # Convert back to list
        words = list(unique_words.values())

        for w in words:
            w['score'] = compute_score(w['review_count'], w['last_reviewed'], datetime.now())

        normalized = normalize_scores(words)
        selected = select_words(normalized, k=k)
        return pd.DataFrame(selected)
    
    def get_top_words_by_level(self, limit_per_level=10):
        """
        Get top words by total review count for each CEFR level.
        Returns a dictionary with levels as keys and lists of (word, translation, total_reviews) as values.
        """
        # SQL query to get total review count for each word grouped by CEFR level
        query = """
        SELECT w.cefr_level, w.word, w.translation, SUM(wu.review_count) as total_reviews
        FROM words w
        JOIN words_users wu ON w.id = wu.word_id
        GROUP BY w.cefr_level, w.word, w.translation
        ORDER BY w.cefr_level, total_reviews DESC
        """
        
        with self.conn:
            cursor = self.conn.execute(query)
            results = cursor.fetchall()
        
        # Group results by CEFR level
        level_words = {}
        for row in results:
            cefr_level, word, translation, total_reviews = row
            
            if cefr_level not in level_words:
                level_words[cefr_level] = []
            
            # Only add if we haven't reached the limit for this level
            if len(level_words[cefr_level]) < limit_per_level:
                level_words[cefr_level].append((word, translation, total_reviews))
        
        return level_words
    
    def execute_query(self, query, params=None):
        """
        Execute a raw SQL query with optional parameters.
        Returns all fetched results.
        """
        with self.conn:
            cursor = self.conn.execute(query, params or [])
            return cursor.fetchall()









if __name__ == "__main__":
    db = DatabaseManager()

    db.execute_query("ALTER TABLE users ADD COLUMN join_date DATETIME;")    
    db.execute_query("UPDATE users SET join_date = CURRENT_TIMESTAMP WHERE join_date IS NULL;")
    print("Database operations completed successfully.")