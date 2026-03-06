# src/task1_workflow_extractor/data_loader.py
import sqlite3
import pandas as pd
from datetime import datetime, date
from typing import List, Optional, Tuple
from pathlib import Path
from ..models.event_models import Event, Capture

class DataLoader:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def get_employees(self) -> List[str]:
        """Get all employee IDs"""
        query = "SELECT DISTINCT id_employee FROM captures"
        df = pd.read_sql_query(query, self.conn)
        return df['id_employee'].tolist()
    
    def get_date_range(self, employee_id: str) -> Tuple[date, date]:
        """Get min and max date for employee"""
        query = """
        SELECT MIN(DATE(timestamp)) as min_date, 
               MAX(DATE(timestamp)) as max_date
        FROM captures
        WHERE id_employee = ?
        """
        df = pd.read_sql_query(query, self.conn, params=(employee_id,))
        min_date = datetime.strptime(df['min_date'].iloc[0], '%Y-%m-%d').date()
        max_date = datetime.strptime(df['max_date'].iloc[0], '%Y-%m-%d').date()
        return min_date, max_date
    
    def load_captures_with_events(self, employee_id: str, 
                                   start_date: Optional[date] = None,
                                   end_date: Optional[date] = None) -> List[Capture]:
        """Load captures and join with events (capture-first approach)"""
        query = """
        SELECT 
            c.id as capture_id,
            c.event_id as capture_event_id,
            c.timestamp as capture_timestamp,
            c.image_path,
            c.id_employee,
            e.id as event_id,
            e.timestamp as event_timestamp,
            e.app_name,
            e.window_title,
            e.event as event_type,
            e.url,
            e.clipboard_content,
            e.x_coord,
            e.y_coord,
            e.typed_text
        FROM captures c
        LEFT JOIN events e ON c.event_id = e.id
        WHERE c.id_employee = ?
        """
        
        params = [employee_id]
        
        if start_date and end_date:
            query += " AND DATE(c.timestamp) BETWEEN ? AND ?"
            params.extend([start_date.isoformat(), end_date.isoformat()])
            
        query += " ORDER BY c.timestamp"
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        captures = []
        for _, row in df.iterrows():
            # Create Event object if event data exists
            event = None
            if pd.notna(row['event_id']):
                event = Event(
                    id=int(row['event_id']),
                    timestamp=datetime.fromisoformat(row['event_timestamp']),
                    app_name=row['app_name'],
                    window_title=row['window_title'],
                    event_type=row['event_type'],
                    url=row['url'] if pd.notna(row['url']) else None,
                    clipboard_content=row['clipboard_content'] if pd.notna(row['clipboard_content']) else None,
                    id_employee=row['id_employee'],
                    x_coord=int(row['x_coord']) if pd.notna(row['x_coord']) else None,
                    y_coord=int(row['y_coord']) if pd.notna(row['y_coord']) else None,
                    typed_text=row['typed_text'] if pd.notna(row['typed_text']) else None
                )
            
            capture = Capture(
                id=int(row['capture_id']),
                event_id=int(row['capture_event_id']) if pd.notna(row['capture_event_id']) else None,
                timestamp=datetime.fromisoformat(row['capture_timestamp']),
                image_path=row['image_path'],
                id_employee=row['id_employee'],
                event=event
            )
            captures.append(capture)
            
        return captures
