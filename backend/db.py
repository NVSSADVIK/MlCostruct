"""
Database initialization and management
"""
import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite3')


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with tables"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            current_price REAL NOT NULL,
            stock_level REAL NOT NULL,
            daily_usage REAL NOT NULL,
            buy_decision TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            worker_plan TEXT NOT NULL,
            reorder_suggestion TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_efficiency REAL NOT NULL,
            num_workers INTEGER NOT NULL,
            project_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def save_price_history(price):
    """Save price to history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO price_history (price) VALUES (?)', (price,))
    conn.commit()
    conn.close()


def get_recent_prices(days=30):
    """Get recent price history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT price FROM price_history 
        ORDER BY date DESC LIMIT ?
    ''', (days,))
    
    prices = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return prices[::-1]  # Return in ascending order


def save_recommendation(recommendation_data):
    """Save recommendation to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO recommendations 
        (current_price, stock_level, daily_usage, buy_decision, risk_level, 
         worker_plan, reorder_suggestion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        recommendation_data['current_price'],
        recommendation_data['stock_level'],
        recommendation_data['daily_usage'],
        recommendation_data['buy_decision'],
        recommendation_data['risk_level'],
        recommendation_data['worker_plan'],
        recommendation_data['reorder_suggestion']
    ))
    
    conn.commit()
    conn.close()


def get_recommendation_history(limit=10):
    """Get recent recommendations"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM recommendations 
        ORDER BY created_at DESC LIMIT ?
    ''', (limit,))
    
    recommendations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return recommendations


def save_metrics(worker_efficiency, num_workers, project_status):
    """Save project metrics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO project_metrics 
        (worker_efficiency, num_workers, project_status)
        VALUES (?, ?, ?)
    ''', (worker_efficiency, num_workers, project_status))
    
    conn.commit()
    conn.close()


def get_latest_metrics():
    """Get latest project metrics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM project_metrics ORDER BY created_at DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None
