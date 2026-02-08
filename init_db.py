#!/usr/bin/env python3
"""
Database initialization script for Pay for Tools
Creates the database with the required schema
"""

import sqlite3
import os

def init_database():
    db_path = os.path.join(os.path.dirname(__file__), 'expenses.db')
    
    # Check if database already exists
    if os.path.exists(db_path):
        response = input(f"Database {db_path} already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Initialization cancelled.")
            return
        os.remove(db_path)
    
    # Create database and tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized successfully: {db_path}")
    print("📋 Tables created: expenses")

if __name__ == '__main__':
    init_database()
