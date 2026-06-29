"""
日期解析、验证等工具函数
"""
from datetime import datetime, date, timedelta
import re
from typing import Optional, Tuple


# 中文数字与星期映射
_WEEKDAY_CN = {
    "星期一": 0, "星期二": 1, "星期三": 2, "星期四": 3,
    "星期五": 4, "星期六": 5, "星期日": 6, "星期天": 6,
    "周一": 0, "周二": 1, "周三": 2, "周四": 3,
    "周五": 4, "周六": 5, "周日": 6, "周天": 6,
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
    "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
}


def parse_date(text: str) -> Optional[str]:
    """
    将各种日期格式解析为 ISO 格式 (YYYY-MM-DD)。
    支持:
    - 标准格式: 2026-07-03, 2026/07/03
    - 简短格式: 7.3, 7-3 (自动补全年份)
    - 自然语言: today, tomorrow, next monday, 周一, 明天
    - 相对天数: +3, +7
    解析失败返回 None。
    """
    if not text or not text.strip():
        return None

    text = text.strip().lower()

    today = date.today()

    # 相对日期
    if text == "today" or text == "今天":
        return today.isoformat()
    if text == "tomorrow" or text == "明天":
        return (today + timedelta(days=1)).isoformat()
    if text == "后天":
        return (today + timedelta(days=2)).isoformat()
    if text == "昨天" or text == "yesterday":
        return (today - timedelta(days=1)).isoformat()

    # +N / -N
    match = re.match(r"^([+-])(\d+)$", text)
    if match:
        sign = 1 if match.group(1) == "+" else -1
        days = int(match.group(2)) * sign
        return (today + timedelta(days=days)).isoformat()

    # next <weekday>
    for name, wd in _WEEKDAY_CN.items():
        if text == f"next {name}":
            days_ahead = wd - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).isoformat()
        if text == name or text == f"this {name}":
            days_ahead = wd - today.weekday()
            if days_ahead < 0:
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).isoformat()

    # 下周一 / 下周二 ...
    cn_weekday_map = {
        "下周一": 0, "下星期二": 1, "下周三": 2, "下周四": 3,
        "下周五": 4, "下周六": 5, "下周日": 6, "下星期天": 6,
        "周一": 0, "周二": 1, "周三": 2, "周四": 3,
        "周五": 4, "周六": 5, "周日": 6, "周天": 6,
    }
    if text in cn_weekday_map:
        wd = cn_weekday_map[text]
        days_ahead = wd - today.weekday()
        if text.startswith("下"):
            days_ahead += 7
        elif days_ahead < 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).isoformat()

    # 标准 ISO: YYYY-MM-DD 或 YYYY/MM/DD
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue

    # 简短格式: M.D 或 M-D (自动补全当前年份)
    match = re.match(r"^(\d{1,2})[-.](\d{1,2})$", text)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        try:
            d = date(today.year, month, day)
            # 如果日期已过，推到下一年
            if d < today:
                d = date(today.year + 1, month, day)
            return d.isoformat()
        except ValueError:
            return None

    return None


def get_week_range(ref_date: Optional[date] = None) -> Tuple[date, date]:
    """返回给定日期所在周的周一和周日。默认今天。"""
    today = ref_date or date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def is_overdue(due_date_str: str) -> bool:
    """判断截止日期是否已过期（未到当天不算逾期）。"""
    if not due_date_str:
        return False
    try:
        due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        return due < date.today()
    except ValueError:
        return False


def is_today(due_date_str: str) -> bool:
    """判断截止日期是否为今天。"""
    if not due_date_str:
        return False
    try:
        due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        return due == date.today()
    except ValueError:
        return False
