#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能排期系统 - Intelligent Scheduler
根据任务紧急程度、设计师技能、工作负载和可用性自动推荐最佳排期
"""

import sys
import io
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from assign_task import TaskAssigner, TeamMember


class IntelligentScheduler:
    """智能排期系统"""

    def __init__(self, members_file: str = None):
        self.assigner = TaskAssigner(members_file)
        self.urgency_levels = {
            "S": {"days": 3, "description": "紧急（3天内）"},
            "A": {"days": 7, "description": "高（1周内）"},
            "B": {"days": 14, "description": "中（2周内）"},
            "C": {"days": 30, "description": "低（1月内）"}
        }

    def calculate_urgency(self, deadline_str: str) -> str:
        """
        根据截止时间计算紧急程度

        Args:
            deadline_str: 截止时间字符串 (YYYY-MM-DD)

        Returns:
            紧急程度 (S/A/B/C)
        """
        try:
            deadline = datetime.fromisoformat(deadline_str)
            now = datetime.now()
            days_left = (deadline - now).days

            if days_left <= 3:
                return "S"
            elif days_left <= 7:
                return "A"
            elif days_left <= 14:
                return "B"
            else:
                return "C"
        except:
            return "C"  # 默认为低紧急程度

    def estimate_task_duration(self, task_type: str, complexity: str = "中等") -> int:
        """
        估算任务所需天数

        Args:
            task_type: 任务类型
            complexity: 复杂度（简单/中等/复杂）

        Returns:
            预估天数
        """
        base_duration = {
            "ui": 3,
            "ux": 5,
            "插画": 7,
            "动效": 4,
            "品牌": 10,
            "b端": 5,
            "移动端": 4,
            "web": 3
        }

        complexity_multiplier = {
            "简单": 0.7,
            "中等": 1.0,
            "复杂": 1.5
        }

        # 查找匹配的任务类型
        task_type_lower = task_type.lower()
        base_days = 5  # 默认值

        for key, days in base_duration.items():
            if key in task_type_lower:
                base_days = days
                break

        return int(base_days * complexity_multiplier.get(complexity, 1.0))

    def recommend_designer(
        self,
        task_name: str,
        task_type: str,
        deadline: str,
        complexity: str = "中等",
        urgency: str = None
    ) -> Dict:
        """
        推荐最合适的设计师和排期方案

        Args:
            task_name: 任务名称
            task_type: 任务类型
            deadline: 截止时间 (YYYY-MM-DD)
            complexity: 复杂度
            urgency: 紧急程度 (可选，如果不提供则自动计算)

        Returns:
            推荐结果字典
        """
        # 计算紧急程度
        if not urgency:
            urgency = self.calculate_urgency(deadline)

        # 估算任务时长
        estimated_days = self.estimate_task_duration(task_type, complexity)

        # 查找匹配的设计师
        matching_members = [
            m for m in self.assigner.members
            if m.matches_task(task_type) and m.is_available()
        ]

        if not matching_members:
            return {
                "success": False,
                "error": "未找到匹配的设计师",
                "task_name": task_name,
                "task_type": task_type
            }

        # 按工作负载和经验等级排序
        def score_member(member):
            # 负载权重 60%，经验权重 40%
            workload_score = 1 / (member.workload + 1)  # 负载越少分数越高
            experience_score = {"初级": 1, "中级": 2, "高级": 3}.get(member.experience_level, 2)
            return workload_score * 0.6 + experience_score * 0.4

        matching_members.sort(key=score_member, reverse=True)

        recommended = matching_members[0]

        # 计算时间安排
        deadline_date = datetime.fromisoformat(deadline)
        start_date = datetime.now() + timedelta(days=1)
        draft_date = start_date + timedelta(days=int(estimated_days * 0.6))
        final_date = start_date + timedelta(days=estimated_days)

        # 检查是否会超期
        will_overdue = final_date > deadline_date

        return {
            "success": True,
            "task": {
                "name": task_name,
                "type": task_type,
                "deadline": deadline,
                "urgency": urgency,
                "complexity": complexity,
                "estimated_days": estimated_days
            },
            "recommended_designer": {
                "name": recommended.name,
                "skills": recommended.skills,
                "specialties": recommended.specialties,
                "experience_level": recommended.experience_level,
                "current_workload": recommended.workload,
                "availability": recommended.availability
            },
            "schedule": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "draft_date": draft_date.strftime("%Y-%m-%d"),
                "final_date": final_date.strftime("%Y-%m-%d"),
                "will_overdue": will_overdue
            },
            "alternatives": [
                {
                    "name": m.name,
                    "workload": m.workload,
                    "experience": m.experience_level
                }
                for m in matching_members[1:4]
            ]
        }

    def check_overdue_risk(self, final_date: str, deadline: str) -> Dict:
        """
        检查超期风险

        Args:
            final_date: 终稿时间
            deadline: 需求方截止时间

        Returns:
            风险信息
        """
        try:
            final = datetime.fromisoformat(final_date)
            deadline_dt = datetime.fromisoformat(deadline)
            days_diff = (final - deadline_dt).days

            if days_diff > 0:
                return {
                    "is_overdue": True,
                    "days_overdue": days_diff,
                    "warning": f"⚠️ 超期 {days_diff} 天",
                    "level": "critical"
                }
            elif days_diff >= -1:
                return {
                    "is_overdue": False,
                    "days_overdue": 0,
                    "warning": "⚡ 时间紧张，建议加快进度",
                    "level": "warning"
                }
            else:
                return {
                    "is_overdue": False,
                    "days_overdue": 0,
                    "warning": f"✅ 安全，剩余 {-days_diff} 天",
                    "level": "safe"
                }
        except:
            return {
                "is_overdue": False,
                "days_overdue": 0,
                "warning": "❓ 无法计算",
                "level": "unknown"
            }


def main():
    """测试智能排期系统"""
    import sys

    # 使用设计师配置
    script_dir = Path(__file__).parent.parent
    designers_file = str(script_dir / "references" / "designers.json")

    scheduler = IntelligentScheduler(members_file=designers_file)

    # 测试案例
    test_cases = [
        {
            "task_name": "B端系统首页UI设计",
            "task_type": "B端设计",
            "deadline": "2026-02-15",
            "complexity": "复杂"
        },
        {
            "task_name": "移动端登录页面设计",
            "task_type": "移动端设计",
            "deadline": "2026-02-20",
            "complexity": "简单"
        },
        {
            "task_name": "产品宣传插画创作",
            "task_type": "插画",
            "deadline": "2026-02-25",
            "complexity": "中等"
        }
    ]

    print("=" * 80)
    print("🎯 智能排期系统测试")
    print("=" * 80)

    for i, test in enumerate(test_cases, 1):
        print(f"\n📋 测试案例 {i}")
        print("-" * 80)

        result = scheduler.recommend_designer(
            task_name=test["task_name"],
            task_type=test["task_type"],
            deadline=test["deadline"],
            complexity=test["complexity"]
        )

        if result["success"]:
            task = result["task"]
            designer = result["recommended_designer"]
            schedule = result["schedule"]

            print(f"任务: {task['name']}")
            print(f"类型: {task['type']}")
            print(f"截止: {task['deadline']}")
            print(f"紧急程度: {task['urgency']} - {scheduler.urgency_levels[task['urgency']]['description']}")
            print(f"复杂度: {task['complexity']}")
            print(f"预估工期: {task['estimated_days']} 天")

            print(f"\n👤 推荐设计师: {designer['name']}")
            print(f"   经验等级: {designer['experience_level']}")
            print(f"   当前负载: {designer['current_workload']} 个任务")
            print(f"   技能: {', '.join(designer['skills'][:3])}")

            print(f"\n📅 排期方案:")
            print(f"   开始时间: {schedule['start_date']}")
            print(f"   初稿时间: {schedule['draft_date']}")
            print(f"   终稿时间: {schedule['final_date']}")

            # 超期风险检查
            risk = scheduler.check_overdue_risk(schedule['final_date'], task['deadline'])
            print(f"   风险评估: {risk['warning']}")

            if result.get("alternatives"):
                print(f"\n🔄 备选设计师:")
                for alt in result["alternatives"][:2]:
                    print(f"   - {alt['name']} (负载: {alt['workload']}, 经验: {alt['experience']})")
        else:
            print(f"❌ {result.get('error', '未知错误')}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
