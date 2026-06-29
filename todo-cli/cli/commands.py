"""
各子命令的实现函数
"""
import datetime

from core import models
from core.utils import parse_date
from cli.formatters import (
    print_todo_table,
    print_week_view,
    print_stats,
    print_course_table,
    print_semester_table,
    print_success,
    print_error,
    print_info,
    console,
)


def cmd_init():
    """初始化数据库。"""
    created = models.todo_list.__module__  # force import
    from core.database import init_db
    is_new = init_db()
    if is_new:
        print_success("数据库已创建！现在可以开始管理你的待办事项了 🎉")
        print_info('先创建一个学期: todo semester start "2025-2026学年第二学期"')
    else:
        print_info("数据库已存在，无需重复初始化。")


def cmd_add(args):
    """添加待办事项。"""
    # 解析课程
    course_id = None
    if args.course:
        course = models.course_get_by_name(args.course)
        if not course:
            # 自动创建课程
            print_info(f"课程 '{args.course}' 不存在，自动创建...")
            course_id = models.course_create(name=args.course)
            print_success(f"课程 '{args.course}' 已创建")
        else:
            course_id = course["id"]

    # 解析日期
    due_date = ""
    if args.due:
        parsed = parse_date(args.due)
        if parsed:
            due_date = parsed
        else:
            print_error(f"无法解析日期 '{args.due}'，已忽略。支持格式: 2026-07-03, 7.3, tomorrow, 周一, +3")

    tid = models.todo_create(
        title=args.title,
        description=args.desc or "",
        course_id=course_id,
        category=args.cat or "个人",
        priority=args.priority or "中",
        due_date=due_date,
    )
    print_success(f"已添加待办 #{tid}: {args.title}")
    if due_date:
        print_info(f"截止日期: {due_date}")


def cmd_list(args):
    """列出待办事项。"""
    kwargs = {}

    if hasattr(args, "done") and args.done:
        kwargs["status"] = "done"
    if hasattr(args, "cat") and args.cat:
        kwargs["category"] = args.cat
    if hasattr(args, "course") and args.course:
        course = models.course_get_by_name(args.course)
        if course:
            kwargs["course_id"] = course["id"]
        else:
            print_error(f"课程 '{args.course}' 不存在")
            return
    if hasattr(args, "priority") and args.priority:
        kwargs["priority"] = args.priority
    if hasattr(args, "overdue") and args.overdue:
        kwargs["overdue_only"] = True
    if hasattr(args, "week") and args.week:
        kwargs["week_only"] = True
    if not hasattr(args, "all") or not args.all:
        kwargs["active_semester_only"] = True

    todos = models.todo_list(**kwargs)

    # 根据筛选条件决定标题
    title_parts = ["📋"]
    if kwargs.get("category"):
        title_parts.append(kwargs["category"])
    if kwargs.get("overdue_only"):
        title_parts.append("已逾期")
    if kwargs.get("week_only"):
        title_parts.append("本周")
    title = " ".join(title_parts) if len(title_parts) > 1 else "📋 待办列表"

    print_todo_table(todos, title)
    console.print(f"  [dim]共 {len(todos)} 条[/]")


def cmd_done(args):
    """标记事项为已完成。"""
    todo = models.todo_get(args.id)
    if not todo:
        print_error(f"待办 #{args.id} 不存在")
        return
    if todo["status"] == "done":
        print_info(f"待办 #{args.id} 已经是完成状态")
        return
    models.todo_mark(args.id, "done")
    print_success(f"已完成: {todo['title']}  🎉")


def cmd_undo(args):
    """恢复事项为未完成。"""
    todo = models.todo_get(args.id)
    if not todo:
        print_error(f"待办 #{args.id} 不存在")
        return
    if todo["status"] == "pending":
        print_info(f"待办 #{args.id} 已经是待完成状态")
        return
    models.todo_mark(args.id, "pending")
    print_success(f"已恢复: {todo['title']}")


def cmd_edit(args):
    """编辑待办事项。"""
    todo = models.todo_get(args.id)
    if not todo:
        print_error(f"待办 #{args.id} 不存在")
        return

    updates = {}
    if args.title:
        updates["title"] = args.title
    if args.desc:
        updates["description"] = args.desc
    if args.course:
        course = models.course_get_by_name(args.course)
        if course:
            updates["course_id"] = course["id"]
        else:
            course_id = models.course_create(name=args.course)
            updates["course_id"] = course_id
            print_info(f"已自动创建课程 '{args.course}'")
    if args.due:
        parsed = parse_date(args.due)
        if parsed:
            updates["due_date"] = parsed
        else:
            print_error(f"无法解析日期 '{args.due}'，已忽略")
    if args.priority:
        updates["priority"] = args.priority
    if args.cat:
        updates["category"] = args.cat

    if not updates:
        print_info("没有需要更新的字段")
        return

    models.todo_update(args.id, **updates)
    print_success(f"已更新待办 #{args.id}")
    # 显示更新后的内容
    for k, v in updates.items():
        field_names = {"title": "标题", "description": "描述", "course_id": "课程",
                       "due_date": "截止日期", "priority": "优先级", "category": "分类"}
        console.print(f"  [dim]{field_names.get(k, k)}:[/] {v}")


def cmd_delete(args):
    """删除待办事项（需确认）。"""
    todo = models.todo_get(args.id)
    if not todo:
        print_error(f"待办 #{args.id} 不存在")
        return
    # 无交互模式下直接删除
    if args.force:
        models.todo_delete(args.id)
        print_success(f"已删除: {todo['title']}")
        return
    # 交互确认
    console.print(f"  ⚠ 确认删除 [bold]'{todo['title']}'[/]? (y/N): ", end="")
    try:
        answer = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        print_info("已取消")
        return
    if answer in ("y", "yes", "是"):
        models.todo_delete(args.id)
        print_success(f"已删除: {todo['title']}")
    else:
        print_info("已取消")


def cmd_search(args):
    """搜索待办事项。"""
    todos = models.todo_list(search=args.keyword, status=None)
    # 也搜索已完成的
    todos_done = models.todo_list(search=args.keyword, status="done")
    all_todos = todos + todos_done
    if not all_todos:
        console.print(f"\n  🔍 未找到包含 '[bold]{args.keyword}[/]' 的事项\n")
        return
    console.print(f"\n  🔍 搜索 '[bold]{args.keyword}[/]' 找到 {len(all_todos)} 条结果:")
    print_todo_table(all_todos, f"🔍 搜索结果: {args.keyword}")


def cmd_week(args):
    """显示本周视图。"""
    from core.utils import get_week_range
    monday, sunday = get_week_range()
    todos = models.todo_list(
        status=None,
        overdue_only=False,
    )
    # 筛选本周+逾期
    today = datetime.date.today().isoformat()
    filtered = [
        t for t in todos
        if t.get("status") != "done"
        and (
            not t.get("due_date")
            or t["due_date"] <= sunday.isoformat()
        )
    ]
    print_week_view(filtered)


def cmd_stats(args):
    """显示统计面板。"""
    stats = models.todo_stats()
    print_stats(stats)


# ---- Course Commands ----


def cmd_course_add(args):
    """添加课程。"""
    cid = models.course_create(
        name=args.name,
        instructor=args.instructor or "",
        color=args.color or "white",
    )
    print_success(f"已添加课程: {args.name} (ID: {cid})")


def cmd_course_list(args):
    """列出课程。"""
    courses = models.course_list()
    print_course_table(courses)


def cmd_course_delete(args):
    """删除课程。"""
    course = models.course_get_by_id(args.id)
    if not course:
        print_error(f"课程 #{args.id} 不存在")
        return
    models.course_delete(args.id)
    print_success(f"已删除课程: {course['name']}（关联事项的课程信息已清除）")


# ---- Semester Commands ----


def cmd_semester_start(args):
    """开始新学期。"""
    sid = models.semester_create(name=args.name)
    models.semester_set_active(sid)
    print_success(f"新学期已开始: {args.name}")
    print_info("现在可以用 todo course add 添加本学期课程了")


def cmd_semester_end(args):
    """结束当前学期。"""
    active = models.semester_get_active()
    if not active:
        print_info("当前没有活跃的学期")
        return
    models.semester_set_active(0)  # 清除所有活跃
    # 直接用 SQL 清除
    from core.database import get_connection
    conn = get_connection()
    conn.execute("UPDATE semesters SET is_active = 0")
    conn.commit()
    conn.close()
    print_success(f"学期已结束: {active['name']}")


def cmd_semester_list(args):
    """列出所有学期。"""
    semesters = models.semester_list_all()
    print_semester_table(semesters)
