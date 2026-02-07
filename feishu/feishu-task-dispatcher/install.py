#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书任务自动分发技能 - 一键安装脚本
"""

import os
import sys
import json
import shutil
from pathlib import Path

# 设置 UTF-8 编码输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_step(step_num, title):
    """打印步骤标题"""
    print(f"\n{'='*60}")
    print(f"步骤 {step_num}: {title}")
    print('='*60)

def check_claude_config():
    """检查 Claude Code 配置"""
    print_step(1, "检查 Claude Code 配置")

    home = Path.home()
    config_file = home / ".claude.json"

    if not config_file.exists():
        print("❌ Claude Code 配置文件不存在")
        print(f"   期望位置: {config_file}")
        print("\n请先安装 Claude Code:")
        print("   npm install -g @anthropic-ai/claude-code")
        return False

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if "mcpServers" not in config:
        print("❌ 未配置 MCP 服务器")
        print("\n请在 ~/.claude.json 中添加飞书 MCP 配置:")
        print(json.dumps({
            "mcpServers": {
                "feishu": {
                    "command": "cmd",
                    "args": ["/c", "npx", "-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "YOUR_APP_ID", "-s", "YOUR_APP_SECRET"],
                    "type": "stdio"
                }
            }
        }, indent=2, ensure_ascii=False))
        return False

    if "feishu" not in config.get("mcpServers", {}):
        print("⚠️  未配置飞书 MCP 服务器")
        print("\n请参考 INSTALL.md 配置飞书 MCP")
        return False

    print("✅ Claude Code 配置正常")
    print(f"   配置文件: {config_file}")
    return True

def check_feishu_login():
    """检查飞书登录状态"""
    print_step(2, "检查飞书登录状态")

    import subprocess
    try:
        result = subprocess.run(
            ["npx", "-y", "@larksuiteoapi/lark-mcp", "whoami"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("✅ 飞书账户已登录")
            print(f"   用户信息: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  飞书账户未登录")
            print("\n请运行以下命令登录:")
            print("   npx -y @larksuiteoapi/lark-mcp login")
            return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        print("\n请确保已安装 Node.js 和 npx")
        return False

def setup_skill_files():
    """设置技能文件"""
    print_step(3, "设置技能文件")

    # 获取当前脚本目录
    script_dir = Path(__file__).parent
    target_dir = Path.cwd()

    print(f"技能目录: {script_dir}")
    print(f"目标目录: {target_dir}")

    # 检查必要文件
    required_files = [
        "SKILL.md",
        "scripts/assign_task.py",
        "scripts/intelligent_scheduler.py",
        "references/team_members.json",
        "references/designers.json"
    ]

    missing_files = []
    for file in required_files:
        if not (script_dir / file).exists():
            missing_files.append(file)

    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ 所有必要文件存在")

    # 检查团队配置
    team_config = script_dir / "references" / "team_members.json"
    with open(team_config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    member_count = len(config.get("members", []))
    print(f"✅ 团队配置: {member_count} 名成员")

    return True

def check_python_environment():
    """检查 Python 环境"""
    print_step(4, "检查 Python 环境")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 版本过低: {sys.version}")
        print("   需要 Python 3.7 或更高版本")
        return False

    print(f"✅ Python 版本: {sys.version.split()[0]}")

    # 检查依赖
    required_packages = ["pandas", "json"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("⚠️  缺少 Python 包:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n请运行: pip install pandas openpyxl")
        return False

    print("✅ Python 依赖已安装")
    return True

def generate_summary():
    """生成安装摘要"""
    print_step(5, "安装摘要")

    print("\n✅ 所有检查通过！技能已准备就绪。")
    print("\n📋 下一步:")
    print("1. 在 Claude Code 中打开项目")
    print("2. 使用自然语言分配任务，例如:")
    print("   '分配一个UI设计任务给团队'")
    print("3. 查看更多示例:")
    print("   cat feishu-task-dispatcher/QUICKSTART.md")

    print("\n🔗 常用命令:")
    print("   查看团队成员: 显示所有团队成员")
    print("   分配任务: 分配一个[任务类型]任务")
    print("   智能排期: 我需要[任务描述]，截止[日期]")

    return True

def main():
    """主函数"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        飞书任务自动分发技能 - 一键安装程序                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

    checks = [
        ("Python 环境", check_python_environment),
        ("Claude Code 配置", check_claude_config),
        ("飞书登录状态", check_feishu_login),
        ("技能文件", setup_skill_files),
    ]

    failed_checks = []
    for name, check_func in checks:
        try:
            if not check_func():
                failed_checks.append(name)
        except Exception as e:
            print(f"❌ {name} 检查失败: {e}")
            failed_checks.append(name)

    if failed_checks:
        print(f"\n❌ 安装失败，以下检查未通过:")
        for check in failed_checks:
            print(f"   - {check}")
        print("\n请解决问题后重新运行此脚本")
        return 1

    return generate_summary()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  安装已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
