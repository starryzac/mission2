"""
argparse 主入口：命令注册与路由
"""
import argparse
import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.commands import (
    cmd_init,
    cmd_add,
    cmd_list,
    cmd_done,
    cmd_undo,
    cmd_edit,
    cmd_delete,
    cmd_search,
    cmd_week,
    cmd_stats,
    cmd_course_add,
    cmd_course_list,
    cmd_course_delete,
    cmd_semester_start,
    cmd_semester_end,
    cmd_semester_list,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo: 大学生命令行待办管理工具",
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # ---- init ----
    sub.add_parser("init", help="初始化数据库")

    # ---- add ----
    p_add = sub.add_parser("add", help="添加待办事项")
    p_add.add_argument("title", help="事项标题")
    p_add.add_argument("-d", "--desc", help="详细描述")
    p_add.add_argument("-c", "--course", help="关联课程名")
    p_add.add_argument("--due", help="截止日期 (e.g. 2026-07-03, tomorrow, 7.3, 周一)")
    p_add.add_argument("-p", "--priority", choices=["高", "中", "低"], help="优先级")
    p_add.add_argument("--cat", choices=["作业", "考试", "阅读", "项目", "个人"], help="分类")

    # ---- list ----
    p_list = sub.add_parser("list", help="列出待办事项")
    p_list.add_argument("--cat", choices=["作业", "考试", "阅读", "项目", "个人"], help="按分类筛选")
    p_list.add_argument("--course", help="按课程筛选")
    p_list.add_argument("--week", action="store_true", help="仅显示本周截止")
    p_list.add_argument("--overdue", action="store_true", help="仅显示已逾期")
    p_list.add_argument("--done", action="store_true", help="显示已完成事项")
    p_list.add_argument("-p", "--priority", choices=["高", "中", "低"], help="按优先级筛选")
    p_list.add_argument("--all", action="store_true", help="显示所有学期的事项")

    # ---- done ----
    p_done = sub.add_parser("done", help="标记事项为已完成")
    p_done.add_argument("id", type=int, help="事项 ID")

    # ---- undo ----
    p_undo = sub.add_parser("undo", help="恢复事项为未完成")
    p_undo.add_argument("id", type=int, help="事项 ID")

    # ---- edit ----
    p_edit = sub.add_parser("edit", help="编辑待办事项")
    p_edit.add_argument("id", type=int, help="事项 ID")
    p_edit.add_argument("--title", help="新标题")
    p_edit.add_argument("--desc", help="新描述")
    p_edit.add_argument("--course", help="新关联课程")
    p_edit.add_argument("--due", help="新截止日期")
    p_edit.add_argument("-p", "--priority", choices=["高", "中", "低"], help="新优先级")
    p_edit.add_argument("--cat", choices=["作业", "考试", "阅读", "项目", "个人"], help="新分类")

    # ---- delete ----
    p_del = sub.add_parser("delete", help="删除待办事项")
    p_del.add_argument("id", type=int, help="事项 ID")
    p_del.add_argument("-f", "--force", action="store_true", help="跳过确认，直接删除")

    # ---- search ----
    p_search = sub.add_parser("search", help="搜索待办事项")
    p_search.add_argument("keyword", help="搜索关键词")

    # ---- week ----
    sub.add_parser("week", help="查看本周待办（默认视图）")

    # ---- stats ----
    sub.add_parser("stats", help="显示统计面板")

    # ---- course ----
    p_course = sub.add_parser("course", help="课程管理")
    course_sub = p_course.add_subparsers(dest="course_cmd")
    p_c_add = course_sub.add_parser("add", help="添加课程")
    p_c_add.add_argument("name", help="课程名称")
    p_c_add.add_argument("--instructor", help="任课教师")
    p_c_add.add_argument("--color", help="显示颜色 (e.g. cyan, yellow, magenta)")
    course_sub.add_parser("list", help="列出所有课程")
    p_c_del = course_sub.add_parser("delete", help="删除课程")
    p_c_del.add_argument("id", type=int, help="课程 ID")

    # ---- semester ----
    p_sem = sub.add_parser("semester", help="学期管理")
    sem_sub = p_sem.add_subparsers(dest="semester_cmd")
    p_s_start = sem_sub.add_parser("start", help="开始新学期")
    p_s_start.add_argument("name", help="学期名称 (e.g. 2025-2026学年第二学期)")
    sem_sub.add_parser("end", help="结束当前学期")
    sem_sub.add_parser("list", help="列出所有学期")

    return parser


def main():
    # 首次运行自动初始化
    from core.database import init_db
    init_db()

    parser = build_parser()

    if len(sys.argv) == 1:
        # 默认显示周视图
        cmd_week(None)
        return

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "done":
        cmd_done(args)
    elif args.command == "undo":
        cmd_undo(args)
    elif args.command == "edit":
        cmd_edit(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "week":
        cmd_week(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "course":
        if args.course_cmd == "add":
            cmd_course_add(args)
        elif args.course_cmd == "list":
            cmd_course_list(args)
        elif args.course_cmd == "delete":
            cmd_course_delete(args)
        else:
            parser.parse_args(["course", "--help"])
    elif args.command == "semester":
        if args.semester_cmd == "start":
            cmd_semester_start(args)
        elif args.semester_cmd == "end":
            cmd_semester_end(args)
        elif args.semester_cmd == "list":
            cmd_semester_list(args)
        else:
            parser.parse_args(["semester", "--help"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
