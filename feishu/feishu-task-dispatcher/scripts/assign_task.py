#!/usr/bin/env python3
"""
Task Assignment Script
Assigns tasks to team members based on skill matching and workload balancing
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TeamMember:
    """Represents a team member with skills and workload"""

    def __init__(
        self,
        name: str,
        department: str,
        skills: List[str],
        tags: List[str],
        workload: int = 0,
        specialties: List[str] = None,
        experience_level: str = "中级",
        availability: Dict = None
    ):
        self.name = name
        self.department = department
        self.skills = [s.lower() for s in skills]
        self.tags = [t.lower() for t in tags]
        self.workload = workload
        self.specialties = specialties or []
        self.experience_level = experience_level
        self.availability = availability

    def is_available(self) -> bool:
        """Check if member is currently available"""
        if not self.availability:
            return True

        from datetime import datetime
        now = datetime.now().date()
        from_date = datetime.fromisoformat(self.availability.get("from", "2000-01-01")).date()
        to_date = datetime.fromisoformat(self.availability.get("to", "2099-12-31")).date()

        # If current date is within unavailability range, return False
        return not (from_date <= now <= to_date)

    def matches_task(self, task_type: str, task_tags: List[str] = None) -> bool:
        """
        Check if member matches the task requirements

        Args:
            task_type: Primary task type/category
            task_tags: Additional task tags for matching

        Returns:
            True if member has matching skills/tags
        """
        task_type = task_type.lower()
        task_tags = [t.lower() for t in (task_tags or [])]

        # Check primary skills
        if any(skill in task_type or task_type in skill for skill in self.skills):
            return True

        # Check specialties (for designers)
        if self.specialties:
            specialties_lower = [s.lower() for s in self.specialties]
            if any(spec in task_type or task_type in spec for spec in specialties_lower):
                return True

        # Check tags
        if task_tags:
            for tag in task_tags:
                if any(member_tag in tag or tag in member_tag for member_tag in self.tags):
                    return True

        return False

    def __repr__(self):
        return f"TeamMember(name={self.name}, workload={self.workload}, skills={self.skills})"


class TaskAssigner:
    """Handles task assignment logic"""

    def __init__(self, members_file: str = None):
        self.members: List[TeamMember] = []
        self.members_file = members_file or self._default_members_file()
        self._load_members()

    def _default_members_file(self) -> str:
        """Get default path to team members configuration"""
        script_dir = Path(__file__).parent.parent
        return str(script_dir / "references" / "team_members.json")

    def _load_members(self):
        """Load team members from configuration file"""
        # Try JSON first
        if os.path.exists(self.members_file):
            with open(self.members_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for member_data in data.get("members", []):
                    member = TeamMember(
                        name=member_data["name"],
                        department=member_data.get("department", ""),
                        skills=member_data.get("skills", []),
                        tags=member_data.get("tags", []),
                        workload=member_data.get("workload", 0),
                        specialties=member_data.get("specialties"),
                        experience_level=member_data.get("experience_level", "中级"),
                        availability=member_data.get("availability")
                    )
                    self.members.append(member)
            return

        # Try markdown file
        md_file = self.members_file.replace('.json', '.md')
        if os.path.exists(md_file):
            self._parse_members_from_markdown(md_file)
            return

        # Use default example members if no file found
        self._load_default_members()

    def _parse_members_from_markdown(self, file_path: str):
        """Parse team members from markdown format"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse members using regex
        member_pattern = r'##\s+(\S+)\s*\n(.*?)(?=##|\Z)'
        matches = re.findall(member_pattern, content, re.DOTALL)

        for name, details in matches:
            department = ""
            skills = []
            tags = []
            workload = 0

            # Extract fields
            dept_match = re.search(r'-?\s*Department:\s*(.+)', details)
            if dept_match:
                department = dept_match.group(1).strip()

            skills_match = re.search(r'-?\s*Skills:\s*(.+)', details)
            if skills_match:
                skills = [s.strip() for s in skills_match.group(1).split(',')]

            tags_match = re.search(r'-?\s*Tags:\s*(.+)', details)
            if tags_match:
                tags = [t.strip() for t in tags_match.group(1).split(',')]

            workload_match = re.search(r'-?\s*Workload:\s*(\d+)', details)
            if workload_match:
                workload = int(workload_match.group(1))

            member = TeamMember(
                name=name.strip(),
                department=department,
                skills=skills,
                tags=tags,
                workload=workload
            )
            self.members.append(member)

    def _load_default_members(self):
        """Load default example team members"""
        default_members = [
            {
                "name": "张三",
                "department": "Engineering",
                "skills": ["Python", "Backend", "API"],
                "tags": ["backend", "后端", "开发"],
                "workload": 2
            },
            {
                "name": "李四",
                "department": "Engineering",
                "skills": ["React", "Frontend", "TypeScript"],
                "tags": ["frontend", "前端", "开发"],
                "workload": 1
            },
            {
                "name": "王五",
                "department": "Engineering",
                "skills": ["Python", "React", "Fullstack"],
                "tags": ["fullstack", "全栈", "backend", "frontend"],
                "workload": 3
            }
        ]

        for member_data in default_members:
            member = TeamMember(**member_data)
            self.members.append(member)

    def assign_task(
        self,
        task_name: str,
        task_type: str,
        task_description: str = "",
        task_tags: List[str] = None
    ) -> Tuple[Optional[TeamMember], List[TeamMember]]:
        """
        Assign task to the most suitable team member

        Args:
            task_name: Name of the task
            task_type: Type/category of the task
            task_description: Optional detailed description
            task_tags: Optional tags for skill matching

        Returns:
            Tuple of (assigned_member, all_matching_members)
        """
        # Find matching members
        matching_members = [
            member for member in self.members
            if member.matches_task(task_type, task_tags) and member.is_available()
        ]

        if not matching_members:
            return None, []

        # Sort by workload (ascending) - assign to least busy member
        matching_members.sort(key=lambda m: m.workload)

        # Get the best match (lowest workload)
        assigned_member = matching_members[0]

        # Increment workload for assigned member
        assigned_member.workload += 1

        return assigned_member, matching_members

    def get_member_workload(self, member_name: str) -> int:
        """Get current workload for a specific member"""
        for member in self.members:
            if member.name == member_name:
                return member.workload
        return 0

    def list_all_members(self) -> List[Dict]:
        """List all team members and their info"""
        return [
            {
                "name": m.name,
                "department": m.department,
                "skills": m.skills,
                "tags": m.tags,
                "specialties": m.specialties,
                "experience_level": m.experience_level,
                "availability": m.availability,
                "workload": m.workload
            }
            for m in self.members
        ]


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Assign tasks to team members")
    parser.add_argument("--task-name", required=True, help="Task name")
    parser.add_argument("--task-type", required=True, help="Task type or category")
    parser.add_argument("--task-description", help="Task description")
    parser.add_argument("--task-tags", nargs='*', help="Task tags for skill matching")
    parser.add_argument("--members-file", help="Path to team members configuration file")
    parser.add_argument("--list-members", action="store_true", help="List all team members")
    parser.add_argument("--json-output", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    try:
        # Initialize assigner
        assigner = TaskAssigner(members_file=args.members_file)

        # List members mode
        if args.list_members:
            members = assigner.list_all_members()
            if args.json_output:
                print(json.dumps(members, ensure_ascii=False, indent=2))
            else:
                print("Team Members:")
                print("=" * 60)
                for member in members:
                    print(f"\n{member['name']} ({member['department']})")
                    print(f"  Skills: {', '.join(member['skills'])}")
                    print(f"  Tags: {', '.join(member['tags'])}")
                    if member.get('specialties'):
                        print(f"  Specialties: {', '.join(member['specialties'])}")
                    print(f"  Experience: {member.get('experience_level', 'N/A')}")
                    if member.get('availability'):
                        avail = member['availability']
                        print(f"  Availability: {avail.get('from')} to {avail.get('to')} - {avail.get('notes', 'N/A')}")
                    else:
                        print(f"  Availability: ✅ Available")
                    print(f"  Current Workload: {member['workload']} tasks")
            return 0

        # Assign task mode
        assigned_member, all_matches = assigner.assign_task(
            task_name=args.task_name,
            task_type=args.task_type,
            task_description=args.task_description or "",
            task_tags=args.task_tags
        )

        if not assigned_member:
            print(f"✗ No matching team member found for task type: {args.task_type}")
            print(f"  Please check team member skills or assign manually")
            return 1

        # Output result
        if args.json_output:
            result = {
                "task_name": args.task_name,
                "task_type": args.task_type,
                "assigned_member": {
                    "name": assigned_member.name,
                    "department": assigned_member.department,
                    "workload": assigned_member.workload
                },
                "all_matches": [
                    {
                        "name": m.name,
                        "workload": m.workload
                    }
                    for m in all_matches
                ]
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✓ Task assigned successfully!")
            print(f"\nTask: {args.task_name}")
            print(f"Type: {args.task_type}")
            print(f"\nAssigned to: {assigned_member.name}")
            print(f"Department: {assigned_member.department}")
            print(f"Current workload: {assigned_member.workload} tasks")

            if len(all_matches) > 1:
                print(f"\nOther matching members:")
                for m in all_matches[1:]:
                    print(f"  - {m.name} (workload: {m.workload})")

        return 0

    except Exception as e:
        print(f"✗ Error: {str(e)}", file=__import__('sys').stderr)
        return 1


if __name__ == "__main__":
    exit(main())
