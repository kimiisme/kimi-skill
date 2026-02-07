# 🚀 飞书任务自动分发技能 - 快速开始

## ✅ 前置条件（已完成！）

你已经成功配置了：
- ✅ 飞书 MCP 服务器（已连接）
- ✅ OAuth 用户登录（已完成）
- ✅ 飞书应用权限（已配置）

## 📋 5分钟快速配置

### 第 1 步：配置团队成员（1分钟）

编辑 `references/team_members.json`，添加你的团队成员：

```json
{
  "members": [
    {
      "name": "张三",
      "department": "Engineering",
      "skills": ["Python", "Backend", "API"],
      "tags": ["backend", "后端", "开发"],
      "workload": 0
    },
    {
      "name": "李四",
      "department": "Engineering",
      "skills": ["React", "Frontend", "TypeScript"],
      "tags": ["frontend", "前端", "开发"],
      "workload": 0
    },
    {
      "name": "王五",
      "department": "Engineering",
      "skills": ["Python", "React", "Fullstack"],
      "tags": ["fullstack", "全栈", "后端", "前端"],
      "workload": 0
    }
  ]
}
```

**字段说明：**
- `name` - 成员姓名
- `skills` - 技能列表（用于匹配任务类型）
- `tags` - 标签列表（支持中文，用于灵活匹配）
- `workload` - 当前任务数量（用于负载均衡）

### 第 2 步：验证 MCP 连接（10秒）

在 Claude Code 中输入：
```bash
/mcp
```

应该看到：
```
feishu · ✓ connected
```

### 第 3 步：开始使用！（即刻生效）

现在就可以用自然语言使用了！

## 💬 使用示例

### 示例 1：简单任务分配

**你：**
> 分配一个后端任务：优化数据库查询

**Claude：**
> 我来帮你分配这个任务...
>
> 任务分析：
> - 类型：backend（后端）
> - 匹配成员：张三、王五
> - 选择：张三（当前工作负载最低）
>
> 已分配给：张三
>
> 要记录到飞书表格吗？

### 示例 2：详细任务 + 记录到飞书

**你：**
> 分配一个前端任务给团队：实现用户登录页面UI，使用React，并记录到飞书表格

**Claude：**
> 任务已分配给李四（匹配 React 技能）
>
> 正在记录到飞书表格...
> ✅ 记录已创建！

### 示例 3：批量任务分配

**你：**
> 我需要完成以下任务：
> 1. API性能优化
> 2. 添加用户认证功能
> 3. 修复前端登录bug
>
> 请帮我分配给团队并记录到飞书

**Claude：**
> 正在分配任务...
>
> 1. API性能优化 → 张三（backend，workload: 1）
> 2. 添加用户认证 → 张三（backend，workload: 2）
> 3. 修复前端登录bug → 李四（frontend，workload: 1）
>
> 正在记录到飞书表格...
> ✅ 3条记录已创建

## 🎯 核心功能

### 1. 智能匹配

根据任务类型自动匹配最合适的团队成员：
- **技能匹配**：Python, React, Java 等
- **标签匹配**：backend, frontend, 全栈 等
- **负载均衡**：选择任务最少的成员

### 2. 自动记录到飞书

分配任务后，可选择自动记录到飞书多维表格

### 3. 工作负载管理

自动跟踪和管理每个成员的任务数量

## 📊 支持的任务类型

技能/标签示例：
- **后端**：backend, 后端, python, java, go, api
- **前端**：frontend, 前端, react, vue, angular
- **全栈**：fullstack, 全栈
- **设计**：design, 设计, ui, ux
- **运维**：devops, 运维, docker, k8s

## 🔧 高级配置

### 自定义匹配规则

编辑 `team_members.json`：
- 添加更多技能和标签
- 设置初始工作负载
- 调整部门信息

### 飞书表格配置

**你的表格地址**：
```
https://jcnf1u9k7wpv.feishu.cn/wiki/QCDfwSD95i7bA4kUOCzcMylanpb?table=tbl2d4LJF0oZ2xLm
```

**当前字段**：- 文本（文本类型）

**建议添加的完整字段**：
- 任务名称
- 任务描述
- 任务类型
- 分配成员
- 任务状态
- 优先级
- 创建时间

## ❓ 常见问题

### Q: MCP 没有连接怎么办？

**A**: 运行 `/mcp` 检查连接状态，如果未连接：
1. 检查 `~/.claude.json` 配置
2. 确认 OAuth 登录状态：`npx -y @larksuiteoapi/lark-mcp whoami`
3. 重启 Claude Code

### Q: 如何添加更多团队成员？

**A**: 编辑 `references/team_members.json`，按现有格式添加新的成员对象

### Q: 工作负载如何更新？

**A**: 任务成功分配后，成员的 workload 会自动 +1。任务完成后，手动编辑 JSON 文件减去对应数量

### Q: 可以记录到不同的表格吗？

**A**: 可以！在使用时指定表格地址，或者更新默认配置

## 🎉 完成！

配置完成后，你可以：
- ✅ 用自然语言分配任务
- ✅ 自动匹配合适的成员
- ✅ 记录到飞书多维表格
- ✅ 查看分配历史和统计

**现在就开始使用吧！** 🚀

---

**需要帮助？** 查看：
- [README.md](README.md) - 完整使用说明
- [EXAMPLES.md](EXAMPLES.md) - 详细示例
