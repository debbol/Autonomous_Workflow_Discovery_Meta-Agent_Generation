# create_sample_db.py
import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_database():
    conn = sqlite3.connect('test_data.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        app_name TEXT,
        window_title TEXT,
        event TEXT,
        url TEXT,
        clipboard_content TEXT,
        id_employee TEXT,
        x_coord INTEGER,
        y_coord INTEGER,
        typed_text TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS captures (
        id INTEGER PRIMARY KEY,
        event_id INTEGER,
        timestamp TEXT,
        image_path TEXT,
        id_employee TEXT,
        FOREIGN KEY (event_id) REFERENCES events (id)
    )
    ''')
    
    # Insert sample data
    employees = ['EMP-0025', 'EMP-0028', 'EMP-0053']
    events = ['Click', 'Type', 'Copy', 'Paste', 'App Switch', 'Navigate']
    
    for emp in employees:
        for day in range(4):
            for hour in range(9, 17):
                timestamp = datetime(2026, 2, 23 + day, hour, random.randint(0, 59))
                
                # Create events
                for _ in range(random.randint(3, 8)):
                    event_type = random.choice(events)
                    cursor.execute('''
                    INSERT INTO events (timestamp, app_name, window_title, event, id_employee, x_coord, y_coord, typed_text, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        timestamp.isoformat(),
                        random.choice(['Chrome', 'Excel', 'Word', 'Slack']),
                        'Sample Window',
                        event_type,
                        emp,
                        random.randint(100, 1000),
                        random.randint(100, 800),
                        'sample text' if event_type == 'Type' else None,
                        'https://example.com' if event_type == 'Navigate' else None
                    ))
                    
                    event_id = cursor.lastrowid
                    
                    # Create capture for this event
                    cursor.execute('''
                    INSERT INTO captures (event_id, timestamp, image_path, id_employee)
                    VALUES (?, ?, ?, ?)
                    ''', (
                        event_id,
                        timestamp.isoformat(),
                        f'screenshots/{emp}_{timestamp.isoformat()}.png',
                        emp
                    ))
                    
                    timestamp += timedelta(minutes=random.randint(1, 5))
    
    conn.commit()
    conn.close()
    print("Sample database created successfully!")

if __name__ == '__main__':
    create_sample_database()
