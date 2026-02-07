---
name: feishu-task-dispatcher
description: This skill should be used when the user needs to automatically distribute tasks to team members based on skills/roles and update Feishu (Lark) bitable. It works together with the Feishu MCP server (@larksuiteoapi/lark-mcp) - the skill handles intelligent task assignment logic while MCP handles Feishu API interactions.
---

# Feishu Task Dispatcher Skill

This skill automates intelligent task distribution to team members and updates Feishu (Lark) multidimensional tables. It works seamlessly with the Feishu MCP server to provide a complete task management solution.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Code     │────▶│  This Skill       │────▶│  Feishu MCP      │
│  (User Interface) │     │  (Task Logic)     │     │  (API Handler)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                  │
                                  ▼
                           ┌─────────────────┐
                           │  Feishu API      │
                           │  - Bitable       │
                           │  - Documents     │
                           │  - Messages      │
                           └─────────────────┘
```

## When to Use This Skill

Use this skill when:
- User needs to assign tasks to team members based on their skills or roles
- Tasks need to be recorded in a Feishu bitable table
- Workload needs to be balanced across team members
- User requests automatic task distribution with intelligent matching

## Core Workflow

### 1. Task Assignment Process

When a task assignment request is received:

1. **Parse Task Information**
   - Extract task name (required)
   - Extract task description
   - Extract task type/tags for skill matching

2. **Match Team Members**
   - Load team member profiles from `references/team_members.json`
   - Filter members with matching skills/tags
   - Apply workload balancing algorithm

3. **Assign Task**
   - Select the most suitable team member
   - Present assignment decision to user

4. **Update Feishu Table** (via MCP)
   - Use Feishu MCP tools to create record
   - Return record confirmation

### 2. Integration with Feishu MCP

This skill uses Feishu MCP for all API interactions:

**Available MCP Tools:**
- `mcp__feishu__bitable_v1_appTableRecord_create` - Create table records
- `mcp__feishu__bitable_v1_appTableRecord_search` - Search records
- `mcp__feishu__docx_builtin_import` - Create documents
- And many more...

**Important:** Always use `useUAT: true` parameter to use user identity for operations.

## Configuration

### Prerequisites

1. **Feishu MCP Server** - Must be configured and connected
   - Verify with `/mcp` command in Claude Code
   - Should show: `feishu · ✓ connected`

2. **Feishu Application Permissions**
   - OAuth login completed: `npx -y @larksuiteoapi/lark-mcp login`
   - Required permissions: `docs:doc`, `drive:drive`, `bitable:app`

3. **Team Member Configuration**
   - Edit `references/team_members.json` with your team info

### Team Member Configuration

Team member profiles in `references/team_members.json`:

```json
{
  "members": [
    {
      "name": "张三",
      "department": "Engineering",
      "skills": ["Python", "Backend", "API"],
      "tags": ["backend", "后端", "开发"],
      "workload": 2
    }
  ]
}
```

**Field Descriptions:**
- `name` - Member's name
- `department` - Department/team
- `skills` - Technical skills (for matching task types)
- `tags` - Additional tags (for flexible matching)
- `workload` - Current number of assigned tasks (for load balancing)

## Usage Examples

### Example 1: Simple Task Assignment

**User:**
> 分配一个后端任务：优化数据库查询性能

**Workflow:**
1. Parse task: type="backend", name="优化数据库查询性能"
2. Match members with "backend" skills
3. Select member with lowest workload
4. Ask user: "Should I record this in Feishu table?"
5. If yes, use MCP to create record

### Example 2: Detailed Task with Description

**User:**
> 分配一个新任务给前端团队：实现用户登录页面UI，使用React，优先级高

**Workflow:**
1. Parse: type="frontend", name="实现用户登录页面UI", priority="高"
2. Match frontend developers (React skill)
3. Assign to member with lowest workload
4. Create record with all details via MCP

### Example 3: Batch Task Assignment

**User:**
> 我需要完成以下任务：
> 1. API性能优化
> 2. 添加用户认证
> 3. 修复登录bug
>
> 请帮我分配并记录到飞书表格

**Workflow:**
1. Parse all tasks
2. Assign each task optimally
3. Create multiple records via MCP
4. Present summary

## Best Practices

1. **Verify MCP Connection** - Always check Feishu MCP is connected before operations
2. **Use User Identity** - Always set `useUAT: true` for MCP calls
3. **Provide Feedback** - Show assignment reasoning (why this member was chosen)
4. **Handle No Matches** - If no member matches, ask user to specify or assign manually
5. **Update Workload** - Increment workload after successful assignment

## Error Handling

- **No matching member**: Suggest adding skills/tags or manual assignment
- **MCP not connected**: Prompt user to check MCP configuration
- **Record creation failed**: Retry with simpler field values or report detailed error
- **Permission errors**: Remind user to complete OAuth login

## Scripts Reference

### `scripts/assign_task.py`

Task assignment script with skill-based matching logic.

**Usage:**
```bash
python scripts/assign_task.py --task-type "backend" --name "API Optimization"
```

**Output:** Assignment result with member info and workload

## File Structure

```
feishu-task-dispatcher/
├── SKILL.md                    # This file
├── README.md                   # User guide
├── INSTALL.md                  # Setup instructions
├── QUICKSTART.md              # Quick start guide
├── scripts/
│   └── assign_task.py         # Task assignment logic
├── references/
│   ├── team_members.json      # Team configuration
│   └── team_members.md        # Team docs (optional)
└── examples/
    └── usage_examples.md      # Usage examples
```

## Quick Start

1. **Ensure Feishu MCP is configured and connected**
   ```bash
   /mcp  # Should show: feishu · ✓ connected
   ```

2. **Configure your team members**
   - Edit `references/team_members.json`

3. **Start using the skill**
   - Simply describe your task assignment needs in natural language

## Example Commands

Once configured, you can use natural language:

- "分配一个前端任务，使用React实现用户管理页面"
- "帮我分配这个后端任务给最合适的团队成员：优化数据库查询"
- "将以下任务分配给团队并记录到飞书：1. 添加用户认证 2. 修复登录bug"
