"""
Database utilities for storing student progress
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join('data', 'student_data.db')

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL UNIQUE,
            mastery_levels TEXT NOT NULL,
            learning_style TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

def save_student_progress(student_name, mastery_levels, learning_style=None):
    """Save student progress to database"""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    mastery_json = json.dumps(mastery_levels)
    
    cursor.execute("""
        INSERT OR REPLACE INTO student_progress 
        (student_name, mastery_levels, learning_style, last_updated)
        VALUES (?, ?, ?, ?)
    """, (student_name, mastery_json, learning_style, datetime.now()))
    
    conn.commit()
    conn.close()

def load_student_progress(student_name):
    """Load student progress from database"""
    if not os.path.exists(DB_PATH):
        return None
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT mastery_levels, learning_style
        FROM student_progress
        WHERE student_name = ?
    """, (student_name,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'mastery_levels': json.loads(result[0]),
            'learning_style': result[1]
        }
    return None
