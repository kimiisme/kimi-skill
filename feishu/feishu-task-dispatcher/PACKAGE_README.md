# 飞书任务自动分发技能 - 快速部署包

## 📦 这是什么？

这是一个完整的飞书任务自动分发技能包，可以在5分钟内部署到任何电脑上。

**功能特性：**
- 🤖 智能任务分配 - 根据技能自动匹配团队成员
- 📅 智能排期系统 - 考虑紧急程度、任务复杂度
- ⚠️ 超期预警 - 自动检测任务是否会超期
- 👥 团队资源管理 - 设计师技能、经验、可用性
- 🔗 飞书深度集成 - 使用官方 MCP，无缝协作

---

## 🚀 快速开始（3种方式）

### 方式1：使用打包脚本（推荐）

**在当前电脑上打包：**

```bash
# Mac/Linux
bash create_package.sh

# Windows
create_package.bat
```

**在新电脑上安装：**

1. 解压生成的 `.zip` 文件
2. 运行 `quick_install.sh` (Mac/Linux) 或 `quick_install.bat` (Windows)
3. 按照 `INSTALL.md` 配置飞书 MCP
4. 运行 `npx -y @larksuiteoapi/lark-mcp login` 登录
5. 开始使用！

### 方式2：手动复制文件

```bash
# 1. 复制整个文件夹到项目目录
cp -r feishu-task-dispatcher /path/to/your/project/

# 2. 配置飞书 MCP（参考 INSTALL.md）

# 3. 登录飞书
npx -y @larksuiteoapi/lark-mcp login
```

### 方式3：使用安装检查脚本

```bash
cd feishu-task-dispatcher
python install.py
```

脚本会自动检查：
- ✅ Python 环境
- ✅ Claude Code 配置
- ✅ 飞书登录状态
- ✅ 技能文件完整性

---

## 📋 文件结构

```
feishu-task-dispatcher/
├── 📄 SKILL.md                          # 技能定义（必需）
├── 📖 README.md                         # 项目说明
├── 🚀 QUICKSTART.md                     # 快速开始
├── ⚙️ INSTALL.md                        # 完整安装指南
├── 🔧 install.py                        # 自动安装检查脚本
├── 📝 TEAM_CONFIG.md                    # 团队配置说明
├── 📦 config_template.json              # MCP 配置模板
│
├── 📂 scripts/                          # 核心脚本
│   ├── assign_task.py                 # 任务分配逻辑
│   └── intelligent_scheduler.py       # 智能排期系统
│
└── 📂 references/                       # 配置文件
    ├── team_members.json              # 团队成员模板
    └── designers.json                 # 设计师配置示例
```

---

## ⚙️ 系统要求

### 必需软件

1. **Claude Code**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Python 3.7+**
   ```bash
   python --version  # 检查版本
   ```

3. **Node.js** (用于飞书 MCP)
   ```bash
   node --version
   npx --version
   ```

### Python 依赖

```bash
pip install pandas openpyxl
```

---

## 🔧 配置步骤

### 1. 飞书应用配置

**如果还没有飞书应用：**

1. 访问 https://open.feishu.cn/app
2. 创建自建应用
3. 获取 App ID 和 App Secret
4. 配置权限：
   - `docs:doc` - 创建文档
   - `drive:drive` - 云空间访问
   - `bitable:app` - 多维表格操作
5. 配置 OAuth 重定向 URI：`http://localhost:3000/callback`

### 2. 配置 Claude Code MCP

编辑 `~/.claude.json` (Mac/Linux) 或 `%USERPROFILE%\.claude.json` (Windows)：

```json
{
  "mcpServers": {
    "feishu": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "cli_a90dfd71ecf85bc4", "-s", "fXABWDZrptOPDkEZk7DkRdufS5rsMoz8"],
      "type": "stdio"
    }
  }
}
```

**注意：** 将 `cli_a90dfd71ecf85bc4` 和 `fXABWDZrptOPDkEZk7DkRdufS5rsMoz8` 替换为您自己的 App ID 和 App Secret。

### 3. 登录飞书

```bash
npx -y @larksuiteoapi/lark-mcp login
```

浏览器会自动打开，完成 OAuth 授权。

### 4. 配置团队成员

编辑 `references/team_members.json`：

```json
{
  "members": [
    {
      "name": "设计师姓名",
      "department": "设计部",
      "skills": ["UI设计", "Figma"],
      "specialties": ["B端设计", "移动端设计"],
      "experience_level": "高级",
      "tags": ["design", "ui"],
      "workload": 0,
      "availability": null
    }
  ]
}
```

---

## ✅ 验证安装

### 1. 检查 MCP 连接

在 Claude Code 中运行：
```
/mcp
```

应该显示：`feishu · ✓ connected`

### 2. 测试技能

```
显示所有团队成员
```

应该看到团队成员列表和技能信息。

### 3. 测试任务分配

```
分配一个UI设计任务给团队
```

应该自动分配任务并显示推荐结果。

---

## 🎯 使用示例

### 示例1：简单任务分配

```
分配一个插画任务给团队
```

### 示例2：带截止时间的任务

```
分配一个B端Dashboard设计任务，截止2月25日，需要数据可视化能力
```

### 示例3：智能排期

```
我需要一个移动端APP设计，截止3月1日，任务比较复杂，请推荐最合适的设计师和排期方案
```

---

## 🔍 故障排查

### Q1: MCP 连接失败

**检查：**
```bash
cat ~/.claude.json | grep -A 10 "mcpServers"
npx -y @larksuiteoapi/lark-mcp whoami
```

### Q2: 没有权限创建记录

**解决：**
```bash
npx -y @larksuiteoapi/lark-mcp login
```

### Q3: 找不到团队成员

**检查：**
```bash
cat feishu-task-dispatcher/references/team_members.json
```

### Q4: Python 脚本报错

**检查：**
```bash
python --version  # 需要 3.7+
pip install pandas openpyxl
```

---

## 📚 相关文档

- **[INSTALL.md](feishu-task-dispatcher/INSTALL.md)** - 完整安装指南
- **[QUICKSTART.md](feishu-task-dispatcher/QUICKSTART.md)** - 快速开始
- **[TEAM_CONFIG.md](feishu-task-dispatcher/TEAM_CONFIG.md)** - 团队配置说明
- **[SKILL.md](feishu-task-dispatcher/SKILL.md)** - 技能定义

---

## 🌟 核心优势

| 特性 | 说明 |
|------|------|
| 🤖 **智能匹配** | 根据技能自动匹配最合适的团队成员 |
| ⚖️ **负载均衡** | 考虑工作负载，选择任务最少的成员 |
| 📅 **智能排期** | 自动计算工期，生成排期方案 |
| ⚠️ **风险预警** | 自动检测超期风险 |
| 🔗 **飞书集成** | 使用官方 MCP，无缝集成 |
| 🚀 **简单易用** | 自然语言交互，无需学习复杂命令 |

---

## 🎉 开始使用

安装完成后，直接用自然语言描述需求：

```
分配一个设计任务：制作产品宣传海报，截止2月25日
```

系统会自动：
1. 分析任务类型
2. 匹配合适的设计师
3. 生成排期方案
4. 创建飞书记录

**🎯 准备好了吗？开始使用智能任务管理吧！**
