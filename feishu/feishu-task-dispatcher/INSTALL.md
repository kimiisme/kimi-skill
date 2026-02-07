# 飞书任务自动分发技能 - 安装指南

## 📦 一键安装包

本安装包包含飞书任务自动分发技能的所有必要文件，可在5分钟内完成部署。

---

## 🚀 快速安装（3步完成）

### 第1步：复制技能文件

将 `feishu-task-dispatcher` 文件夹复制到您的项目目录：

```bash
# 例如复制到您的项目根目录
cp -r feishu-task-dispatcher /path/to/your/project/
```

### 第2步：配置飞书 MCP

确认飞书 MCP 已配置（~/.claude.json 中应包含）：

```json
{
  "mcpServers": {
    "feishu": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "YOUR_APP_ID", "-s", "YOUR_APP_SECRET"],
      "type": "stdio"
    }
  }
}
```

### 第3步：登录飞书账户

```bash
npx -y @larksuiteoapi/lark-mcp login
```

✅ **安装完成！** 现在可以使用自然语言分配任务了。

---

## 📋 文件结构

```
feishu-task-dispatcher/
├── SKILL.md                          # 技能定义（必需）
├── README.md                         # 项目说明
├── QUICKSTART.md                     # 快速开始
├── TEAM_CONFIG.md                    # 团队配置说明
├── INSTALL.md                        # 本安装文档
│
├── scripts/                          # 核心脚本（必需）
│   ├── assign_task.py               # 任务分配
│   └── intelligent_scheduler.py     # 智能排期
│
└── references/                       # 配置文件（必需）
    ├── team_members.json            # 团队成员模板
    └── designers.json               # 设计师配置示例
```

---

## ⚙️ 详细配置

### 1. 飞书应用配置

如果您还没有飞书应用：

1. **创建飞书应用**
   - 访问：https://open.feishu.cn/app
   - 创建应用并获取 App ID 和 App Secret

2. **配置权限**

   **应用身份权限（Tenant Access Token）：**
   - `bitable:app` - 查看多维表格
   - `bitable:app:readonly` - 只读访问

   **用户身份权限（User Access Token）：**
   - `docs:doc` - 创建文档
   - `drive:drive` - 云空间访问
   - `bitable:app` - 多维表格操作

3. **配置 OAuth**
   - 设置重定向 URI：`http://localhost:3000/callback`

### 2. 团队成员配置

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

### 3. 飞书表格字段

访问表格后确认以下字段存在：

**基础字段：**
- 任务名称（文本）
- 任务描述（文本）
- 品牌（文本）
- 需求方（单选）
- 需求方稿件截止时间（日期）

**策划字段：**
- 策划人员（单选）
- 策划初稿时间（日期）
- 策划终稿时间（日期）

**设计师字段：**
- 设计师（多选）⚠️ 重要
- 设计师开始时间（日期）
- 初稿时间（日期）
- 终稿时间（日期）

**状态字段：**
- 任务状态（单选）
- 超期预警（文本）
- 当前排期紧急程度（单选）
- 优先级（单选）
- 创建时间（日期，自动填充）

---

## 🎯 使用示例

### 示例1：简单任务分配

```
分配一个UI设计任务给团队
```

### 示例2：详细任务分配

```
分配一个B端Dashboard设计任务，截止2月25日，需要数据可视化能力
```

### 示例3：查看团队配置

```
显示所有团队成员及其技能
```

---

## 🔍 故障排查

### Q1: MCP 连接失败

**检查：**
```bash
# 验证 MCP 配置
cat ~/.claude.json | grep -A 10 "mcpServers"

# 测试 MCP 连接
npx -y @larksuiteoapi/lark-mcp whoami
```

### Q2: 没有权限创建记录

**解决：**
```bash
# 重新登录飞书账户
npx -y @larksuiteoapi/lark-mcp login

# 确认权限
npx -y @larksuiteoapi/lark-mcp permissions
```

### Q3: 找不到团队成员

**检查：**
```bash
# 查看团队成员配置
cat feishu-task-dispatcher/references/team_members.json
```

### Q4: 脚本运行出错

**检查 Python 环境：**
```bash
python --version  # 需要 Python 3.7+

# 安装依赖
pip install pandas openpyxl
```

---

## 📦 离线安装包

### 创建离线包

```bash
# 在当前电脑上打包
cd "h:\Cloude code\feishu"
zip -r feishu-task-dispatcher.zip feishu-task-dispatcher/ -x "*.pyc" "__pycache__/*"
```

### 在新电脑上安装

1. **解压文件**
   ```bash
   unzip feishu-task-dispatcher.zip
   cd feishu-task-dispatcher
   ```

2. **配置 Claude Code**
   - 复制到项目目录
   - 配置 MCP（参考上面的"配置飞书 MCP"部分）

3. **登录飞书**
   ```bash
   npx -y @larksuiteoapi/lark-mcp login
   ```

---

## 🌐 完整部署流程

### 在新电脑上从零开始

**步骤1：安装 Claude Code**
```bash
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code
```

**步骤2：配置飞书 MCP**
```bash
# 编辑配置文件
# Windows: %USERPROFILE%\.claude.json
# Mac/Linux: ~/.claude.json

# 添加飞书 MCP 服务器配置
```

**步骤3：复制技能文件**
```bash
# 将 feishu-task-dispatcher 复制到项目目录
cp -r feishu-task-dispatcher /path/to/project/
```

**步骤4：配置团队信息**
```bash
# 编辑团队成员配置
vim feishu-task-dispatcher/references/team_members.json
```

**步骤5：登录飞书**
```bash
npx -y @larksuiteoapi/lark-mcp login
```

**步骤6：验证安装**
```bash
# 在 Claude Code 中测试
/mcp  # 应显示 feishu · ✓ connected
```

---

## 🎓 进阶配置

### 自定义匹配规则

编辑 `scripts/assign_task.py` 中的 `matches_task` 方法。

### 调整工期估算

编辑 `scripts/intelligent_scheduler.py` 中的 `estimate_task_duration` 方法。

### 添加新的设计师

编辑 `references/team_members.json`，添加新的成员对象。

---

## 📞 技术支持

**检查清单：**
- ✅ Claude Code 已安装
- ✅ 飞书 MCP 已配置并连接
- ✅ 飞书账户已登录
- ✅ 技能文件已复制到项目目录
- ✅ 团队成员已配置
- ✅ 飞书表格字段已创建

**常见错误代码：**
- `1254045` - 字段未找到，检查字段名称
- `91403` - 权限不足，确认已登录飞书
- `99991663` - OAuth 未完成，运行 `npx @larksuiteoapi/lark-mcp login`

---

## ✅ 安装验证

安装完成后，在 Claude Code 中测试：

```
显示所有团队成员
```

应该看到团队成员列表和技能信息。

**🎉 安装成功！开始使用智能任务分配吧！**
