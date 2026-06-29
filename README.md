# 📋 Todo — 大学生命令行待办管理工具

## 项目简介

一款专为大学生设计的命令行待办事项管理工具，支持增删改查四大基本操作，并融入学期管理、课程关联、周视图、统计面板等贴合学生使用场景的功能。基于 Python 3.12 开发，数据本地存储，仅需 `rich` 一个外部库做终端美化。

---

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install rich
```

### 启动

```bash
cd "F:\学校活动\双创周\mission2\todo-cli"
python todo.py
```

首次运行自动初始化数据库，无需手动操作。

---

## 功能概览

### 1. 增删改查（CRUD）

```bash
python todo.py add "完成实验报告"           # 添加待办
python todo.py list                        # 查看所有待办
python todo.py edit 1 --title "新标题"      # 编辑待办
python todo.py delete 1                    # 删除（需确认）
python todo.py delete 1 -f                 # 强制删除（跳过确认）
python todo.py search "实验"               # 模糊搜索
```

### 2. 状态管理

```bash
python todo.py done 1                      # 标记已完成
python todo.py undo 1                      # 恢复为未完成
```

### 3. 待办详情

添加时支持完整参数：

```bash
python todo.py add "标题" \
  -d "详细描述" \
  -c 课程名 \
  --due 截止日期 \
  -p 优先级 \
  --cat 分类
```

示例：

```bash
python todo.py add "完成第三章作业" -c 高等数学 --due 2026-07-03 -p 高 --cat 作业
```

### 4. 筛选查看

```bash
python todo.py list --cat 作业             # 按分类筛选
python todo.py list --course 高等数学       # 按课程筛选
python todo.py list --overdue              # 只看已逾期
python todo.py list --week                 # 只看本周
python todo.py list --done                 # 查看已完成
python todo.py list -p 高                  # 按优先级筛选
python todo.py list --all                  # 跨学期查看
```

### 5. 周视图（默认命令）

```bash
python todo.py                             # 无参数默认显示周视图
python todo.py week                        # 同上
```

展示：已逾期事项 → 今日截止 → 本周待办 → 无截止日期事项

### 6. 学期管理

```bash
python todo.py semester start "2025-2026学年第二学期"
python todo.py semester end                # 结束当前学期
python todo.py semester list               # 列出所有学期
```

学期之间课程数据隔离，个人事项不受影响。

### 7. 课程管理

```bash
python todo.py course add 高等数学 --instructor "张老师"
python todo.py course add 线性代数 --instructor "李老师" --color cyan
python todo.py course list
python todo.py course delete 2
```

添加待办时引用不存在的课程名会自动创建。

### 8. 统计面板

```bash
python todo.py stats
```

显示：总事项数、完成率、逾期数、按分类分布、按课程分布。

---

## 命令速查表

| 命令 | 说明 |
|------|------|
| `todo` | 默认周视图 |
| `todo add <标题> [-d] [-c] [--due] [-p] [--cat]` | 添加待办 |
| `todo list [筛选条件]` | 列出待办 |
| `todo done <ID>` | 标记完成 |
| `todo undo <ID>` | 恢复未完成 |
| `todo edit <ID> [字段...]` | 编辑待办 |
| `todo delete <ID> [-f]` | 删除待办 |
| `todo search <关键词>` | 搜索 |
| `todo week` | 周视图 |
| `todo stats` | 统计面板 |
| `todo course add/list/delete` | 课程管理 |
| `todo semester start/end/list` | 学期管理 |

---

## 支持的日期格式

| 格式 | 示例 |
|------|------|
| 标准 ISO | `2026-07-03`、`2026/07/03` |
| 简短格式 | `7.3`、`7-3`（自动补全年份） |
| 英文 | `today`、`tomorrow`、`yesterday`、`next monday` |
| 中文 | `今天`、`明天`、`后天`、`周一`、`下周五`、`周日` |
| 相对日期 | `+3`（三天后）、`-1`（昨天） |

---

## 分类与优先级

| 分类 | 图标 | 场景 |
|------|------|------|
| 作业 | 📝 | 日常作业、实验报告 |
| 考试 | 📚 | 期中/期末/测验复习 |
| 阅读 | 📖 | 论文、教材预习 |
| 项目 | 💻 | 课程设计、大作业 |
| 个人 | 📌 | 洗衣、购物、社团 |

| 优先级 | 含义 |
|--------|------|
| 高 🔴 | 明日截止、考试相关 |
| 中 🟡 | 本周截止、常规任务 |
| 低 🟢 | 无硬 deadline、可选 |

---

## 项目结构

```
todo-cli/
├── todo.py              # 程序入口
├── README.md            # 本文件
├── cli/
│   ├── __init__.py
│   ├── main.py          # argparse 命令注册与路由
│   ├── commands.py      # 各子命令业务逻辑
│   └── formatters.py    # Rich 表格/彩色/面板输出
├── core/
│   ├── __init__.py
│   ├── database.py      # SQLite 数据库初始化与连接
│   ├── models.py        # Todo/Course/Semester CRUD
│   └── utils.py         # 日期智能解析、逾期判断
└── data/
    └── todo.db          # SQLite 数据库（自动生成）
```

---

## 技术栈

| 模块 | 选型 | 说明 |
|------|------|------|
| 语言 | Python 3.12 | |
| CLI | argparse（标准库） | 零额外依赖 |
| 存储 | SQLite3（标准库） | 单文件，支持复杂查询 |
| 美化 | rich | 彩色终端输出 |
| 日期 | datetime（标准库） | ISO 日期处理 |

---

## 设计亮点

- **无需网络**：全部数据本地存储，宿舍断网也能用
- **日期智能解析**：支持中英文自然语言日期，输入体验友好
- **逾期高亮**：过期事项在列表和周视图中红色标注，防止遗漏
- **自动适配**：添加待办时课程名不存在自动创建，降低使用门槛
- **学期隔离**：新学期课程数据独立，历史数据保留可查
- **默认周视图**：无参数直接显示本周/逾期/今日概览，一目了然
