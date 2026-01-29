#!/usr/bin/env python3
"""
中国工作日计算脚本
使用 https://holiday.dreace.top API 查询假期和补班信息
"""

import requests
import sys
from datetime import datetime, timedelta
from typing import Dict, Set, Tuple
import json
import os

# 缓存文件路径
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "holiday_cache.json")


def get_holiday_data(year: int) -> Dict:
    """
    获取指定年份的假期数据
    使用本地缓存优先，缓存不存在时从 API 获取
    """
    # 确保缓存目录存在
    os.makedirs(CACHE_DIR, exist_ok=True)

    # 加载缓存
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except:
            cache = {}

    # 检查缓存
    if str(year) in cache:
        return cache[str(year)]

    # 从 API 获取数据
    url = "https://holiday.dreace.top"
    data = {}

    # 获取整年的数据
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        try:
            response = requests.get(url, params={"date": date_str}, timeout=10)
            if response.status_code == 200:
                result = response.json()
                # 判断是否为工作日
                # note 为 "普通工作日" 或 "补班工作日" 时是工作日
                # note 为 "周末" 或假期名称时是假期
                is_workday = result.get("note") in ["普通工作日", "补班工作日"]
                data[date_str] = {
                    "is_workday": is_workday,
                    "note": result.get("note"),
                    "type": result.get("type")
                }
        except Exception as e:
            print(f"Warning: Failed to fetch data for {date_str}: {e}", file=sys.stderr)
        current_date += timedelta(days=1)

    # 更新缓存
    cache[str(year)] = data
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}", file=sys.stderr)

    return data


def is_workday(date: datetime) -> bool:
    """判断指定日期是否为工作日"""
    data = get_holiday_data(date.year)
    date_str = date.strftime("%Y-%m-%d")

    if date_str in data:
        return data[date_str]["is_workday"]

    # 默认逻辑：周末不是工作日
    return date.weekday() < 5


def count_workdays(start_date: datetime, end_date: datetime) -> int:
    """
    计算从 start_date 到 end_date 之间的工作日数量
    不包括 start_date，包括 end_date（如果 end_date 是工作日）
    """
    count = 0
    current_date = start_date + timedelta(days=1)

    while current_date <= end_date:
        if is_workday(current_date):
            count += 1
        current_date += timedelta(days=1)

    return count


def parse_date(date_str: str) -> datetime:
    """解析日期字符串，支持多种格式"""
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m-%d",
        "%m/%d",
        "%m月%d日",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            # 如果只有月日，补全年份
            if parsed.year == 1900:  # strptime 的默认年份
                parsed = parsed.replace(year=datetime.now().year)
                # 如果目标日期已过，则假设是明年
                if parsed < datetime.now():
                    parsed = parsed.replace(year=datetime.now().year + 1)
            return parsed
        except ValueError:
            continue

    raise ValueError(f"无法解析日期: {date_str}")


def get_special_dates(start_date: datetime, end_date: datetime) -> tuple:
    """获取日期范围内的节假日和补班"""
    data = get_holiday_data(start_date.year)
    if end_date.year != start_date.year:
        data.update(get_holiday_data(end_date.year))

    holidays = []
    makeup_days = []

    current_date = start_date + timedelta(days=1)
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str in data:
            info = data[date_str]
            note = info["note"]
            # 收集节假日（排除普通周末）
            if note not in ["普通工作日", "补班工作日", "周末"]:
                holidays.append((date_str, note))
            # 收集补班
            elif note == "补班工作日":
                makeup_days.append((date_str, note))
        current_date += timedelta(days=1)

    return holidays, makeup_days


def add_workdays(start_date: datetime, workdays: int) -> datetime:
    """
    从 start_date 开始，计算 workdays 个工作日后的日期
    从明天开始计算
    """
    current_date = start_date + timedelta(days=1)  # 从明天开始
    count = 0

    while count < workdays:
        if is_workday(current_date):
            count += 1
            if count == workdays:
                return current_date
        current_date += timedelta(days=1)

    return current_date


def list_holidays(year: int):
    """列出指定年份的节假日和补班"""
    data = get_holiday_data(year)

    holidays = []
    makeup_days = []

    for date_str, info in data.items():
        note = info["note"]
        # 收集节假日（排除普通周末）
        if note != "普通工作日" and note != "补班工作日" and note != "周末":
            holidays.append((date_str, note))
        # 收集补班
        elif note == "补班工作日":
            makeup_days.append((date_str, note))

    # 按日期排序
    holidays.sort()
    makeup_days.sort()

    # 输出节假日
    print(f"# {year}年 节假日")
    for date, note in holidays:
        print(f"{date} - {note}")

    print()

    # 输出补班
    print(f"# {year}年 补班")
    for date, note in makeup_days:
        print(f"{date} - {note}")


def main():
    if len(sys.argv) < 2:
        print("Usage: workdays.py <date> [start_date] [--detail]")
        print("       workdays.py <N>个工作日 [start_date] [--detail]")
        print("       workdays.py --list [year]")
        print()
        print("Examples:")
        print("  workdays.py 12-31           # 计算到12月31日的工作日")
        print("  workdays.py 12-31 --detail  # 计算工作日并显示节假日和补班")
        print("  workdays.py 23个工作日       # 计算从今天起23个工作日后是哪天")
        print("  workdays.py 2024-12-31 2024-12-01  # 计算两个日期间的工作日")
        print("  workdays.py --list          # 列出今年的节假日和补班")
        print("  workdays.py --list 2025     # 列出2025年的节假日和补班")
        sys.exit(1)

    # 处理 --list 参数
    if sys.argv[1] in ["--list", "-l"]:
        if len(sys.argv) >= 3:
            year = int(sys.argv[2])
        else:
            year = datetime.now().year
        list_holidays(year)
        return

    try:
        # 检查是否是 "N个工作日" 格式
        if "个工作日" in sys.argv[1]:
            workdays_num = int(sys.argv[1].replace("个工作日", ""))

            # 确定开始日期
            if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
                start_date = parse_date(sys.argv[2])
                detail_flag = len(sys.argv) >= 4 and "--detail" in sys.argv[3:]
            else:
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                detail_flag = len(sys.argv) >= 3 and "--detail" in sys.argv[2:]

            # 计算目标日期
            target_date = add_workdays(start_date, workdays_num)

            # 输出结果
            print(f"{target_date.strftime('%Y-%m-%d')}")

            # 如果需要详细信息，显示经过的节假日和补班
            if detail_flag:
                holidays, makeup_days = get_special_dates(start_date, target_date)

                if holidays or makeup_days:
                    print()
                    if holidays:
                        print(f"节假日 ({len(holidays)}天):")
                        for date, note in holidays:
                            print(f"  {date} - {note}")

                    if makeup_days:
                        if holidays:
                            print()
                        print(f"补班 ({len(makeup_days)}天):")
                        for date, note in makeup_days:
                            print(f"  {date} - {note}")
            return

        # 原有的日期查询逻辑
        target_date = parse_date(sys.argv[1])

        # 如果指定了开始日期，使用指定的；否则从今天开始
        if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
            start_date = parse_date(sys.argv[2])
            detail_flag = len(sys.argv) >= 4 and "--detail" in sys.argv[3:]
        else:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            detail_flag = len(sys.argv) >= 3 and "--detail" in sys.argv[2:]

        # 计算工作日
        workdays = count_workdays(start_date, target_date)

        # 输出结果
        if workdays < 0:
            print(f"从 {start_date.strftime('%Y-%m-%d')} 到 {target_date.strftime('%Y-%m-%d')} 已经过了 {-workdays} 个工作日")
        else:
            print(f"{workdays}")

        # 如果需要详细信息
        if detail_flag:
            holidays, makeup_days = get_special_dates(start_date, target_date)

            if holidays or makeup_days:
                print()
                if holidays:
                    print(f"节假日 ({len(holidays)}天):")
                    for date, note in holidays:
                        print(f"  {date} - {note}")

                if makeup_days:
                    if holidays:
                        print()
                    print(f"补班 ({len(makeup_days)}天):")
                    for date, note in makeup_days:
                        print(f"  {date} - {note}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
