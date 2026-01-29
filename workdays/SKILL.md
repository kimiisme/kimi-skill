---
name: workdays
description: This skill should be used when the user asks about counting workdays (工作日) between dates, specifically in the context of Chinese holidays. It calculates the number of workdays from today to a specified date, excluding weekends and legal holidays while including make-up workdays (补班). Use this skill for queries like "离几月几号还有几个工作日" (how many workdays until a certain date).
---

# 中国工作日计算

This skill provides functionality to calculate the number of workdays between dates, accounting for Chinese national holidays, weekends, and make-up workdays (补班).

## When to Use This Skill

Use this skill when the user asks questions about:
- 离某个日期还有多少个工作日 (How many workdays until a certain date)
- 计算两个日期之间的工作日数量 (Calculate workdays between two dates)
- 排除假期和周末的工作日计算 (Workday calculation excluding holidays and weekends)

Common query patterns:
- "离12月31号还有几个工作日"
- "到下周五还有多少工作日"
- "计算从现在到春节还有多少工作日"

## How It Works

The skill uses the [ChinaHolidayAPI](https://holiday.dreace.top) to determine whether a specific date is a workday or holiday. It accounts for:
- **周末** (Weekends) - Not workdays
- **法定假期** (Legal holidays) - Not workdays (e.g., 元旦, 春节, 国庆节)
- **补班工作日** (Make-up workdays) - Count as workdays
- **普通工作日** (Regular workdays) - Count as workdays

Data is cached locally after the first API request for a given year, improving performance for subsequent queries.

## Usage

Execute the workdays calculation script to count workdays:

```bash
# Calculate workdays from today to a target date
python scripts/workdays.py <target_date>

# Calculate workdays with detailed holiday/makeup information
python scripts/workdays.py <target_date> --detail

# Calculate workdays between two specific dates
python scripts/workdays.py <target_date> <start_date>

# List all holidays and makeup days for a year
python scripts/workdays.py --list [year]
```

### Date Format Support

The script supports multiple date formats:
- `2024-12-31` or `2024/12/31` - Full date with year
- `12-31` or `12/31` - Month and day only (assumes current year)
- `12月31日` - Chinese format

### Examples

```bash
# Workdays from today to December 31st
python scripts/workdays.py 12-31

# Workdays with detailed holiday and makeup information
python scripts/workdays.py 3-31 --detail

# Workdays from December 1st to December 31st, 2024
python scripts/workdays.py 2024-12-31 2024-12-01

# Workdays from today to a specific future date
python scripts/workdays.py 2025-01-01

# List all holidays and makeup days for 2026
python scripts/workdays.py --list 2026
```

## Script Output

### Simple Mode (default)

The script returns a single number representing the count of workdays:
- If the result is positive, it shows the number of workdays until the target date
- If the result is negative, it indicates how many workdays have passed since the target date

### Detail Mode (--detail flag)

When the `--detail` flag is used, the script outputs:
1. The count of workdays
2. A list of holidays in the date range
3. A list of makeup workdays in the date range

Example output with `--detail`:
```
39

节假日 (9天):
  2026-02-15 - 春节
  2026-02-16 - 春节
  ...

补班 (2天):
  2026-02-14 - 补班工作日
  2026-02-28 - 补班工作日
```

## Implementation Notes

- Workday calculation starts from the day **after** the start date (today by default)
- The target date is included if it is a workday
- Holiday data is cached in `scripts/cache/holiday_cache.json` for efficiency
- The API supports years 2023-2026

## Troubleshooting

If the script fails to fetch data from the API:
1. Check internet connectivity
2. Verify the API endpoint (https://holiday.dreace.top) is accessible
3. Cached data will be used if available for the queried year
