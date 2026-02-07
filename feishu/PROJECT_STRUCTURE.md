# 飞书任务自动分发技能 - 项目结构

## 📦 项目目录

```
h:\Cloude code\feishu\
├── 📂 feishu-task-dispatcher/        # 主技能包
│   ├── 📄 SKILL.md                    # 技能定义
│   ├── 📖 README.md                   # 项目说明
│   ├── 🚀 QUICKSTART.md               # 快速开始
│   ├── ⚙️ INSTALL.md                  # 安装指南
│   ├── 🔧 install.py                  # 安装检查脚本
│   ├── 📋 TEAM_CONFIG.md              # 团队配置说明
│   ├── 📦 config_template.json        # MCP配置模板
│   ├── 📦 PACKAGE_README.md           # 打包说明
│   │
│   ├── 📂 scripts/                    # 核心脚本
│   │   ├── assign_task.py            # 任务分配
│   │   └── intelligent_scheduler.py  # 智能排期
│   │
│   └── 📂 references/                 # 配置文件
│       ├── team_members.json         # 团队成员模板
│       ├── team_members.md           # 配置说明
│       └── designers.json            # 设计师配置
│
├── 📂 docs/                          # 参考文档
│   └── 设计任务管理系统字段方案.md
│
├── 📜 create_package.sh              # 打包脚本（Mac/Linux）
├── 📜 create_package.bat             # 打包脚本（Windows）
└── 📗 跨境项目排期.xlsx              # 原始数据
```

---

## 📝 文件说明

### 核心技能文件

| 文件 | 说明 | 用途 |
|------|------|------|
| **SKILL.md** | 技能定义 | Claude Code识别技能的入口文件 |
| **README.md** | 项目说明 | 功能介绍、架构说明 |
| **QUICKSTART.md** | 快速开始 | 5分钟快速配置指南 |
| **INSTALL.md** | 安装指南 | 完整安装步骤和故障排查 |
| **install.py** | 安装脚本 | 自动检查环境配置 |
| **TEAM_CONFIG.md** | 团队配置 | 团队成员配置说明 |

### 核心脚本

| 文件 | 说明 |
|------|------|
| **assign_task.py** | 任务分配逻辑，支持技能匹配和负载均衡 |
| **intelligent_scheduler.py** | 智能排期系统，自动计算工期和风险 |

### 配置文件

| 文件 | 说明 |
|------|------|
| **team_members.json** | 团队成员模板（通用） |
| **designers.json** | 设计师配置示例 |
| **config_template.json** | MCP配置模板 |

### 参考文档

| 文件 | 说明 |
|------|------|
| **设计任务管理系统字段方案.md** | 字段设计和ID映射参考 |

### 打包工具

| 文件 | 说明 |
|------|------|
| **create_package.sh** | Mac/Linux打包脚本 |
| **create_package.bat** | Windows打包脚本 |

---

## 🚀 快速开始

### 在当前电脑使用

技能已经配置完成，可以直接使用：

```
分配一个UI设计任务给团队
```

### 在其他电脑部署

**方式1：使用打包脚本**

```bash
# Windows
create_package.bat

# Mac/Linux
bash create_package.sh
```

**方式2：手动复制**

```bash
# 复制整个技能包
cp -r feishu-task-dispatcher /path/to/project/

# 在新电脑上运行
cd feishu-task-dispatcher
python install.py
```

---

## 📋 文件清单

### 必需文件（核心功能）

- ✅ SKILL.md
- ✅ scripts/assign_task.py
- ✅ scripts/intelligent_scheduler.py
- ✅ references/team_members.json

### 文档文件（参考）

- ✅ README.md
- ✅ QUICKSTART.md
- ✅ INSTALL.md
- ✅ TEAM_CONFIG.md

### 工具文件（辅助）

- ✅ install.py（安装检查）
- ✅ create_package.sh/.bat（打包）
- ✅ config_template.json（配置模板）

---

## ✨ 特性

- 🤖 智能任务分配
- 📅 智能排期系统
- ⚠️ 超期风险预警
- 👥 团队资源管理
- 🔗 飞书深度集成

---

**🎯 项目已整理完成，随时可以部署！**
