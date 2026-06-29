"""
Todo、Course、Semester 的 CRUD 操作
"""
from datetime import datetime, date
from typing import Optional
from .database import get_connection


# ========== Semester ==========

def semester_create(name: str, start_date: str = "", end_date: str = "") -> int:
    """创建新学期。返回新 ID。"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO semesters (name, start_date, end_date, is_active) VALUES (?, ?, ?, 0)",
        (name, start_date, end_date),
    )
    conn.commit()
    sid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return sid


def semester_set_active(semester_id: int):
    """将指定学期设为活跃，其余为非活跃。"""
    conn = get_connection()
    conn.execute("UPDATE semesters SET is_active = 0")
    conn.execute("UPDATE semesters SET is_active = 1 WHERE id = ?", (semester_id,))
    conn.commit()
    conn.close()


def semester_get_active() -> Optional[dict]:
    """获取当前活跃学期。"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM semesters WHERE is_active = 1").fetchone()
    conn.close()
    return dict(row) if row else None


def semester_list_all() -> list[dict]:
    """列出所有学期。"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM semesters ORDER BY start_date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ========== Courses ==========

def course_create(name: str, instructor: str = "", semester_id: Optional[int] = None, color: str = "white") -> int:
    """创建课程。若未指定学期则自动使用活跃学期。返回新 ID。"""
    if semester_id is None:
        active = semester_get_active()
        if active:
            semester_id = active["id"]
    conn = get_connection()
    conn.execute(
        "INSERT INTO courses (name, instructor, semester_id, color) VALUES (?, ?, ?, ?)",
        (name, instructor, semester_id, color),
    )
    conn.commit()
    cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return cid


def course_list(semester_id: Optional[int] = None) -> list[dict]:
    """列出课程。不指定学期则列出所有（活跃学期优先）。"""
    conn = get_connection()
    if semester_id is not None:
        rows = conn.execute("SELECT * FROM courses WHERE semester_id = ? ORDER BY name", (semester_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT c.*, s.name as semester_name
            FROM courses c
            LEFT JOIN semesters s ON c.semester_id = s.id
            ORDER BY s.is_active DESC, c.name
        """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def course_get_by_name(name: str) -> Optional[dict]:
    """按名称查找课程。"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE name = ?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None


def course_get_by_id(course_id: int) -> Optional[dict]:
    """按 ID 查找课程。"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def course_delete(course_id: int) -> bool:
    """删除课程。关联的待办事项 course_id 置空。"""
    conn = get_connection()
    conn.execute("UPDATE todos SET course_id = NULL WHERE course_id = ?", (course_id,))
    conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()
    return True


# ========== Todos ==========

def todo_create(
    title: str,
    description: str = "",
    course_id: Optional[int] = None,
    category: str = "个人",
    priority: str = "中",
    due_date: str = "",
) -> int:
    """创建待办事项。返回新 ID。"""
    conn = get_connection()
    conn.execute(
        """INSERT INTO todos (title, description, course_id, category, priority, due_date)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, description, course_id, category, priority, due_date),
    )
    conn.commit()
    tid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return tid


def todo_list(
    status: Optional[str] = None,
    category: Optional[str] = None,
    course_id: Optional[int] = None,
    priority: Optional[str] = None,
    overdue_only: bool = False,
    week_only: bool = False,
    search: Optional[str] = None,
    active_semester_only: bool = False,
) -> list[dict]:
    """查询待办列表，支持多种筛选条件。"""
    conn = get_connection()

    query = """
        SELECT t.*, c.name as course_name, c.color as course_color
        FROM todos t
        LEFT JOIN courses c ON t.course_id = c.id
        LEFT JOIN semesters s ON c.semester_id = s.id
        WHERE 1=1
    """
    params: list = []

    if status:
        query += " AND t.status = ?"
        params.append(status)
    else:
        # 默认只显示 pending
        query += " AND t.status = 'pending'"

    if category:
        query += " AND t.category = ?"
        params.append(category)

    if course_id is not None:
        query += " AND t.course_id = ?"
        params.append(course_id)

    if priority:
        query += " AND t.priority = ?"
        params.append(priority)

    if overdue_only:
        today_str = date.today().isoformat()
        query += " AND t.due_date != '' AND t.due_date < ?"
        params.append(today_str)

    if week_only:
        from .utils import get_week_range
        monday, sunday = get_week_range()
        query += " AND t.due_date >= ? AND t.due_date <= ?"
        params.append(monday.isoformat())
        params.append(sunday.isoformat())

    if search:
        query += " AND t.title LIKE ?"
        params.append(f"%{search}%")

    if active_semester_only:
        query += " AND (s.is_active = 1 OR t.course_id IS NULL)"

    query += " ORDER BY t.due_date ASC, t.priority DESC, t.created_at DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        # 转换优先级排序字段为可读值
        results.append(d)
    return results


def todo_get(todo_id: int) -> Optional[dict]:
    """获取单条待办详情。"""
    conn = get_connection()
    row = conn.execute(
        """SELECT t.*, c.name as course_name, c.color as course_color
           FROM todos t
           LEFT JOIN courses c ON t.course_id = c.id
           WHERE t.id = ?""",
        (todo_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def todo_update(todo_id: int, **kwargs):
    """更新待办字段。自动更新 updated_at。"""
    allowed = {"title", "description", "course_id", "category", "priority", "due_date", "status"}
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return

    updates["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [todo_id]

    conn = get_connection()
    conn.execute(f"UPDATE todos SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()


def todo_delete(todo_id: int):
    """删除待办事项。"""
    conn = get_connection()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


def todo_mark(todo_id: int, status: str = "done"):
    """标记待办为 done 或恢复为 pending。"""
    todo_update(todo_id, status=status)


def todo_stats() -> dict:
    """获取统计信息。"""
    conn = get_connection()
    today_str = date.today().isoformat()

    total = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    done = conn.execute("SELECT COUNT(*) FROM todos WHERE status = 'done'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM todos WHERE status = 'pending'").fetchone()[0]
    overdue = conn.execute(
        "SELECT COUNT(*) FROM todos WHERE status = 'pending' AND due_date != '' AND due_date < ?",
        (today_str,),
    ).fetchone()[0]

    # 按分类统计
    cat_rows = conn.execute(
        "SELECT category, COUNT(*) as cnt FROM todos WHERE status = 'pending' GROUP BY category"
    ).fetchall()

    # 按课程统计
    course_rows = conn.execute(
        """SELECT c.name, COUNT(*) as cnt
           FROM todos t JOIN courses c ON t.course_id = c.id
           WHERE t.status = 'pending'
           GROUP BY t.course_id
           ORDER BY cnt DESC"""
    ).fetchall()

    conn.close()

    return {
        "total": total,
        "done": done,
        "pending": pending,
        "overdue": overdue,
        "by_category": {r["category"]: r["cnt"] for r in cat_rows},
        "by_course": {r["name"]: r["cnt"] for r in course_rows},
    }
