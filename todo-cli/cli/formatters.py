"""
Rich 格式化输出：表格、彩色文本、周视图、统计面板
"""
from datetime import date, timedelta
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from core.utils import is_overdue, is_today, get_week_range


console = Console()

PRIORITY_STYLE = {
    "高": "bold red",
    "中": "yellow",
    "低": "dim",
}

CATEGORY_ICONS = {
    "作业": "📝",
    "考试": "📚",
    "阅读": "📖",
    "项目": "💻",
    "个人": "📌",
}

STATUS_ICONS = {
    "pending": "⬜",
    "done": "✅",
}


def _priority_text(p: str) -> Text:
    """根据优先级返回格式化文本。"""
    style = PRIORITY_STYLE.get(p, "white")
    return Text(p, style=style)


def _format_due_date(due_date_str: str) -> Text:
    """格式化截止日期，逾期标红。"""
    if not due_date_str:
        return Text("—", style="dim")
    if is_overdue(due_date_str):
        return Text(f"⚠ {due_date_str}", style="bold red")
    if is_today(due_date_str):
        return Text(f"📌 {due_date_str}", style="bold yellow")
    return Text(due_date_str)


def print_todo_table(todos: list[dict], title: str = "📋 待办列表"):
    """以 Rich 表格展示待办事项列表。"""
    if not todos:
        console.print(f"\n[dim]{title}[/dim]\n  ✨ 暂无待办事项\n")
        return

    table = Table(title=title, box=box.ROUNDED, highlight=True)
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("状态", width=4)
    table.add_column("标题", min_width=25)
    table.add_column("课程", width=12)
    table.add_column("分类", width=8)
    table.add_column("优先级", width=6)
    table.add_column("截止日期", width=14)

    for t in todos:
        status_icon = STATUS_ICONS.get(t.get("status", "pending"), "⬜")
        title_text = Text(t["title"])
        if t.get("status") == "done":
            title_text.stylize("dim strike")

        course_name = t.get("course_name", "—") or "—"
        course_color = t.get("course_color", "white") or "white"

        table.add_row(
            str(t["id"]),
            status_icon,
            title_text,
            Text(course_name, style=course_color),
            CATEGORY_ICONS.get(t["category"], "") + " " + t["category"],
            _priority_text(t["priority"]),
            _format_due_date(t.get("due_date", "")),
        )

    console.print(table)


def print_week_view(todos: list[dict]):
    """打印本周视图，分区展示逾期/今天/本周/已完成。"""
    monday, sunday = get_week_range()
    Weekday_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    monday_cn = Weekday_CN[monday.weekday()]
    sunday_cn = Weekday_CN[sunday.weekday()]

    iso_week = date.today().isocalendar()[1]
    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]📅 第{iso_week}周[/] ({monday.strftime('%m月%d日')} {monday_cn} — {sunday.strftime('%m月%d日')} {sunday_cn})",
        )
    )

    today_str = date.today().isoformat()
    overdue = [t for t in todos if is_overdue(t.get("due_date", ""))]
    today = [t for t in todos if t.get("due_date") == today_str]
    this_week = [
        t for t in todos
        if t.get("due_date")
        and t["due_date"] > today_str
        and monday.isoformat() <= t["due_date"] <= sunday.isoformat()
    ]
    no_due = [t for t in todos if not t.get("due_date")]

    section = [
        ("🔴 已逾期", "bold red", overdue),
        ("📌 今天截止", "bold yellow", today),
        ("📅 本周待办", "cyan", this_week),
        ("📋 无截止日期", "dim", no_due),
    ]

    for label, color, items in section:
        if items:
            console.print(f"\n[{color}]{label} ({len(items)})[/]")
            for t in items:
                course_info = f" | [dim]{t.get('course_name', '')}[/]" if t.get("course_name") else ""
                done = " [dim]✅[/]" if t.get("status") == "done" else ""
                cat_icon = CATEGORY_ICONS.get(t["category"], "")
                console.print(
                    f"  {cat_icon} [{color}][{t['id']}][/] {t['title']}{done}"
                    f"{course_info}"
                    f" | {_priority_text(t['priority'])}"
                    f" | {_format_due_date(t.get('due_date', ''))}"
                )

    if not any(items for _, _, items in section):
        console.print("\n  ✨ 本周暂无待办，享受你的时间吧！\n")


def print_stats(stats: dict):
    """打印统计面板。"""
    total = stats["total"]
    done = stats["done"]
    pending = stats["pending"]
    overdue = stats["overdue"]
    pct = round(done / total * 100) if total > 0 else 0

    panel_content = f"""
[bold]总事项:[/]      {total}
[bold]已完成:[/]      {done} [dim]({pct}%)[/]
[bold]待完成:[/]      {pending}
[bold]已逾期:[/]      [bold red]{overdue}[/]
"""

    if stats["by_category"]:
        panel_content += "\n[bold]按分类:[/]\n"
        parts = []
        for cat, cnt in stats["by_category"].items():
            parts.append(f"  {CATEGORY_ICONS.get(cat, '')} {cat}: {cnt}")
        panel_content += "\n".join(parts)

    if stats["by_course"]:
        panel_content += "\n\n[bold]按课程:[/]\n"
        parts = []
        for course, cnt in stats["by_course"].items():
            parts.append(f"  📘 {course}: {cnt}")
        panel_content += "\n".join(parts)

    console.print(Panel(panel_content.strip(), title="📊 统计概览", border_style="cyan"))


def print_course_table(courses: list[dict]):
    """打印课程列表。"""
    if not courses:
        console.print("\n  📭 暂无课程，用 [bold]todo course add[/] 添加\n")
        return

    table = Table(title="📘 课程列表", box=box.ROUNDED)
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("课程名", style="bold")
    table.add_column("教师", width=15)
    table.add_column("学期", width=20)
    table.add_column("颜色", width=8)

    for c in courses:
        table.add_row(
            str(c["id"]),
            c["name"],
            c.get("instructor", "—") or "—",
            c.get("semester_name", "—") or "—",
            f"[{c.get('color', 'white')}]■[/] {c.get('color', 'white')}",
        )
    console.print(table)


def print_semester_table(semesters: list[dict]):
    """打印学期列表。"""
    if not semesters:
        console.print("\n  📭 暂无学期，用 [bold]todo semester start[/] 创建\n")
        return

    table = Table(title="🏫 学期列表", box=box.ROUNDED)
    table.add_column("ID", style="dim", width=5, justify="right")
    table.add_column("学期名称", style="bold")
    table.add_column("开始", width=12)
    table.add_column("结束", width=12)
    table.add_column("状态", width=8)

    for s in semesters:
        status = "[bold green]● 当前[/]" if s["is_active"] else "[dim]○[/]"
        table.add_row(
            str(s["id"]),
            s["name"],
            s.get("start_date", "—") or "—",
            s.get("end_date", "—") or "—",
            status,
        )
    console.print(table)


def print_success(msg: str):
    console.print(f"  [green]✓[/] {msg}")


def print_error(msg: str):
    console.print(f"  [red]✗[/] {msg}")


def print_info(msg: str):
    console.print(f"  [cyan]ℹ[/] {msg}")
