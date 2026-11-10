import sqlite3
import os
import pandas as pd


# Database location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "dqdash.db")


def get_connection():
    """Create database connection"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_activity_db():
    """Create activity tables"""

    conn = get_connection()
    cursor = conn.cursor()

    # Preventive Mode Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preventive_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        business_description TEXT,
        generated_report TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Corrective Mode Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corrective_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        dataset_name TEXT,
        rows INTEGER,
        columns INTEGER,
        quality_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ML Mode Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ml_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        dataset_name TEXT,
        target_column TEXT,
        best_model TEXT,
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ---------------- PREVENTIVE MODE ---------------- #

def save_preventive_report(username, description, report):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO preventive_reports (username, business_description, generated_report)
    VALUES (?, ?, ?)
    """, (username, description, report))

    conn.commit()
    conn.close()


def get_preventive_history():

    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM preventive_reports ORDER BY created_at DESC",
        conn
    )
    conn.close()

    return df


# ---------------- CORRECTIVE MODE ---------------- #

def save_corrective_activity(username, dataset, rows, columns, score):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO corrective_reports (username, dataset_name, rows, columns, quality_score)
    VALUES (?, ?, ?, ?, ?)
    """, (username, dataset, rows, columns, score))

    conn.commit()
    conn.close()


def get_corrective_history():

    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM corrective_reports ORDER BY created_at DESC",
        conn
    )
    conn.close()

    return df


# ---------------- ML MODE ---------------- #

def save_ml_result(username, dataset, target, model, score):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ml_results (username, dataset_name, target_column, best_model, score)
    VALUES (?, ?, ?, ?, ?)
    """, (username, dataset, target, model, score))

    conn.commit()
    conn.close()


def get_ml_history():

    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM ml_results ORDER BY created_at DESC",
        conn
    )
    conn.close()

    return df

def get_system_stats():

    conn = get_connection()
    cursor = conn.cursor()

    # Preventive reports count
    cursor.execute("SELECT COUNT(*) FROM preventive_reports")
    preventive_count = cursor.fetchone()[0]

    # Corrective reports count
    cursor.execute("SELECT COUNT(*) FROM corrective_reports")
    corrective_count = cursor.fetchone()[0]

    # ML experiments count
    cursor.execute("SELECT COUNT(*) FROM ml_results")
    ml_count = cursor.fetchone()[0]

    conn.close()

    return {
        "preventive": preventive_count,
        "corrective": corrective_count,
        "ml": ml_count
    }