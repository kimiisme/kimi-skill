# Team Members Configuration

This file contains team member profiles including their skills, roles, and current workload.

## Member Profiles

### 张三
- **Department:** Engineering
- **Skills:** Python, Backend, API Development, Database
- **Tags:** backend, 后端, 开发, python
- **Workload:** 2 current tasks
- **Best for:** Backend development, API development, database work

### 李四
- **Department:** Engineering
- **Skills:** React, Frontend, TypeScript, UI/UX
- **Tags:** frontend, 前端, 开发, react
- **Workload:** 1 current task
- **Best for:** Frontend development, React applications, UI implementation

### 王五
- **Department:** Engineering
- **Skills:** Python, React, Fullstack, DevOps
- **Tags:** fullstack, 全栈, backend, frontend
- **Workload:** 3 current tasks
- **Best for:** Fullstack projects, DevOps tasks, end-to-end features

### 赵六
- **Department:** Design
- **Skills:** UI Design, Figma, User Research, Prototyping
- **Tags:** design, 设计, ui, ux
- **Workload:** 0 current tasks
- **Best for:** UI/UX design, user research, prototyping

### 钱七
- **Department:** Engineering
- **Skills:** Java, Spring, Microservices, Backend
- **Tags:** backend, 后端, java, 微服务
- **Workload:** 2 current tasks
- **Best for:** Java backend, microservices, Spring applications

## How to Update

### Option 1: Edit JSON File

Edit `references/team_members.json` directly:

```json
{
  "members": [
    {
      "name": "Member Name",
      "department": "Department",
      "skills": ["skill1", "skill2"],
      "tags": ["tag1", "tag2"],
      "workload": 0
    }
  ]
}
```

### Option 2: Edit This Markdown File

Maintain the format above. The script will parse this file automatically.

## Task Matching Logic

When assigning tasks, the system:

1. **Task Type Matching:** Searches for task type in member skills and tags
2. **Tag Matching:** Checks if task tags match member tags
3. **Workload Balancing:** Among matching members, selects the one with lowest current workload

### Example Task Assignments

| Task | Type | Assigned To | Reason |
|------|------|-------------|--------|
| API Optimization | Backend | 张三 | Has backend skills, workload 2 |
| UI Component | Frontend | 李四 | Has frontend skills, workload 1 (lowest) |
| Database Migration | Backend | 钱七 | Backend skills, same workload as 张三 |

## Workload Management

- **Initial workload:** Set based on current active tasks
- **Auto-increment:** Workload increases by 1 when a task is assigned
- **Manual updates:** Edit workload numbers when tasks are completed
- **Recommendation:** Review and update weekly to reflect actual task completion

## Adding New Members

1. Add member entry to this file or `team_members.json`
2. Include relevant skills and tags for matching
3. Set initial workload to 0
4. Test assignment with `--list-members` flag

## Skill Categories

### Development Skills
- **Backend:** Python, Java, Go, Node.js, API, Database
- **Frontend:** React, Vue, Angular, TypeScript, HTML/CSS
- **Fullstack:** Multiple frontend and backend skills

### Design Skills
- **UI Design:** Figma, Sketch, Adobe XD
- **UX Design:** User Research, Prototyping, Wireframing

### DevOps Skills
- **Infrastructure:** Docker, Kubernetes, CI/CD
- **Cloud:** AWS, Azure, GCP

## Customization Tips

1. **Be specific with skills:** Use concrete technology names (e.g., "React" instead of "web development")
2. **Include bilingual tags:** Both English and Chinese for better matching
3. **Update workloads regularly:** Keep workload numbers accurate for fair distribution
4. **Review matching results:** Check if assignments make sense and adjust skills/tags as needed
