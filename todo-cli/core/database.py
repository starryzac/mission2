"""
数据库初始化与连接管理
"""
import sqlite3
import os


DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "todo.db")


def get_connection() -> sqlite3.Connection:
    """获取数据库连接，自动创建 data 目录。"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> bool:
    """初始化数据库表结构。已存在则跳过，返回 True 表示首次创建。"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"
    )
    exists = cursor.fetchone() is not None

    if not exists:
        conn.executescript("""
            CREATE TABLE semesters (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                start_date  TEXT DEFAULT '',
                end_date    TEXT DEFAULT '',
                is_active   INTEGER DEFAULT 0
            );

            CREATE TABLE courses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                instructor  TEXT DEFAULT '',
                semester_id INTEGER,
                color       TEXT DEFAULT 'white',
                FOREIGN KEY (semester_id) REFERENCES semesters(id) ON DELETE SET NULL
            );

            CREATE TABLE todos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT DEFAULT '',
                course_id   INTEGER,
                category    TEXT DEFAULT '个人',
                priority    TEXT DEFAULT '中',
                due_date    TEXT DEFAULT '',
                status      TEXT DEFAULT 'pending',
                created_at  TEXT DEFAULT (datetime('now','localtime')),
                updated_at  TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
            );

            CREATE INDEX idx_todos_status ON todos(status);
            CREATE INDEX idx_todos_due_date ON todos(due_date);
            CREATE INDEX idx_todos_course ON todos(course_id);
            CREATE INDEX idx_courses_semester ON courses(semester_id);
        """)
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False
