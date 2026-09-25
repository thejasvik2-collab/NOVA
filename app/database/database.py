import sqlite3
from pathlib import Path


# Store NOVA's database inside the project
DATABASE_PATH = Path(__file__).resolve().parent / "nova.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_task(title, priority="Medium"):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, priority)
        VALUES (?, ?)
        """,
        (title, priority)
    )

    connection.commit()
    connection.close()


def get_tasks():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, completed, priority, created_at
        FROM tasks
        ORDER BY completed ASC, id DESC
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def complete_task(task_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()


def delete_task(task_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()
def initialize_notes_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_note(title, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (title, content)
        VALUES (?, ?)
        """,
        (title, content)
    )

    connection.commit()
    connection.close()


def get_notes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM notes
        ORDER BY id DESC
    """)

    notes = cursor.fetchall()

    connection.close()

    return notes


def delete_note(note_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()
    connection.close()