# src/utils/db_utils.py
import sqlite3
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

class DBUtils:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Get column information for a table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
        return [
            {
                'cid': col[0],
                'name': col[1],
                'type': col[2],
                'notnull': col[3],
                'default': col[4],
                'pk': col[5]
            }
            for col in columns
        ]
        
    def execute_query(self, query: str, params: tuple = ()) -> pd.DataFrame:
        """Execute a query and return results as DataFrame"""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=params)
            
    def backup_database(self, backup_path: str):
        """Create a backup of the database"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
