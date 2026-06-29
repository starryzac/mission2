#!/usr/bin/env python3
"""
Todo - 大学生命令行待办管理工具

用法:
    python todo.py                  # 查看本周待办
    python todo.py add "标题"        # 添加待办
    python todo.py list             # 查看列表
    python todo.py done <ID>        # 标记完成
    python todo.py --help           # 查看所有命令

首次使用自动创建数据库，无需手动初始化。
"""
import sys
import io

# 修复 Windows GBK 编码下的 emoji 输出问题
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from cli.main import main

if __name__ == "__main__":
    main()
