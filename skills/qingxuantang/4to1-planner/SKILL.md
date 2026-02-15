---
name: 4to1-planner
description: AI规划助手，采用4To1方法™——将四年期的愿景转化为每日可执行的行动计划。该工具可连接到Notion、Todoist、Google Calendar或本地Markdown文件。适用于用户需要规划目标、进行每周回顾、跟踪项目或建立规划系统的场景。
user-invocable: true
homepage: https://4to1planner.com
metadata: {"openclaw":{"emoji":"🎯","requires":{"anyBins":["curl","python3"]},"homepage":"https://4to1planner.com"}}
---

# 4To1 Planner — 人工智能规划助手

> **“从愿景到行动：4To1”**

这是一个基于人工智能的规划工具，它能将您的四年愿景转化为当下的实际行动——通过对话而非固定模板来实现。

## 4To1 方法™

这是一个四层级的战略规划系统，每一层都帮助您弥合愿景与执行之间的差距：

```
4 YEARS  →  Strategic Vision     (Where am I going?)
3 MONTHS →  Project Milestones   (Quarterly Gantt Log)
2 WEEKS  →  Action Execution     (1 Day in a Week sprints)
1 DAY    →  Daily Tasks          (Today's to-do list)
```

此外，还有两个辅助层：
- **“禁止做的事情”（Not-To-Do Projects）：您明确表示拒绝做的事情
- **时间浪费（Time Wasters）**：您正在改进的日常习惯

**核心原则：** 每一项日常任务都与一个两周的冲刺计划相关联，该冲刺计划又与一个三个月的里程碑相关联，最终实现您的四年愿景。**没有任何任务会被忽视。**

## 快速入门

当用户说出以下任何一句话时，该工具就会启动：
- “帮我建立一个规划系统”
- “我想规划我的未来四年”
- “我想进行每周的回顾”
- “我今天应该关注什么？”
- “设置 4To1 规划器”

## 设置：连接您的后端系统

规划器需要一个存储计划的地方。请询问用户他们偏好的后端系统：

### 选项 1：Notion（推荐）

```bash
# 1. Create a Notion integration at https://www.notion.so/my-integrations
# 2. Copy the API key (starts with ntn_)
# 3. Store it:
mkdir -p ~/.config/4to1
echo "BACKEND=notion" > ~/.config/4to1/config
echo "NOTION_API_KEY=ntn_your_key_here" >> ~/.config/4to1/config
```

分享一个包含集成功能的 Notion 父页面（点击 → “连接” → 选择您的集成服务）。

**在 Notion 中创建规划工作区：**

```bash
NOTION_KEY=$(grep NOTION_API_KEY ~/.config/4to1/config | cut -d= -f2)
PARENT_PAGE=$(grep NOTION_PARENT_PAGE ~/.config/4to1/config | cut -d= -f2)

# Create the 4To1 Planning Hub page
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"page_id\": \"$PARENT_PAGE\"},
    \"properties\": {\"title\": {\"title\": [{\"text\": {\"content\": \"🎯 4To1 Planning Hub\"}}]}},
    \"children\": [
      {\"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"text\": {\"content\": \"🔭 4-Year Vision\"}}]}},
      {\"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"Your strategic direction. Updated annually.\"}}]}},
      {\"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"text\": {\"content\": \"📊 3-Month Milestones\"}}]}},
      {\"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"Quarterly Gantt Log — project milestones for this quarter.\"}}]}},
      {\"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"text\": {\"content\": \"🏃 2-Week Sprint\"}}]}},
      {\"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"1 Day in a Week — action execution in 2-week cycles.\"}}]}},
      {\"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"text\": {\"content\": \"🚫 Not-To-Do List\"}}]}},
      {\"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"Projects and commitments you are explicitly saying NO to.\"}}]}},
      {\"type\": \"heading_1\", \"heading_1\": {\"rich_text\": [{\"text\": {\"content\": \"⏰ Time Wasters\"}}]}},
      {\"type\": \"paragraph\", \"paragraph\": {\"rich_text\": [{\"text\": {\"content\": \"Daily habits you are eliminating.\"}}]}}
    ]
  }"

# Create Projects database (tracks items across all 4 layers)
curl -s -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"page_id\": \"$PARENT_PAGE\"},
    \"title\": [{\"text\": {\"content\": \"📋 4To1 Projects\"}}],
    \"properties\": {
      \"Name\": {\"title\": {}},
      \"Status\": {\"select\": {\"options\": [
        {\"name\": \"Active\", \"color\": \"green\"},
        {\"name\": \"Planned\", \"color\": \"blue\"},
        {\"name\": \"On Hold\", \"color\": \"yellow\"},
        {\"name\": \"Done\", \"color\": \"gray\"},
        {\"name\": \"Not-To-Do\", \"color\": \"red\"}
      ]}},
      \"Layer\": {\"select\": {\"options\": [
        {\"name\": \"4-Year Vision\", \"color\": \"blue\"},
        {\"name\": \"3-Month Milestone\", \"color\": \"green\"},
        {\"name\": \"2-Week Sprint\", \"color\": \"orange\"},
        {\"name\": \"1-Day Task\", \"color\": \"red\"}
      ]}},
      \"Priority\": {\"select\": {\"options\": [
        {\"name\": \"Primary\", \"color\": \"red\"},
        {\"name\": \"Secondary\", \"color\": \"orange\"},
        {\"name\": \"Nice-to-have\", \"color\": \"gray\"}
      ]}},
      \"Parent Project\": {\"rich_text\": {}},
      \"Start Date\": {\"date\": {}},
      \"End Date\": {\"date\": {}},
      \"Progress\": {\"number\": {\"format\": \"percent\"}},
      \"Notes\": {\"rich_text\": {}}
    }
  }"

# Create Sprint Log database (2-week tracking cycles)
curl -s -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"page_id\": \"$PARENT_PAGE\"},
    \"title\": [{\"text\": {\"content\": \"📅 Sprint Log\"}}],
    \"properties\": {
      \"Sprint\": {\"title\": {}},
      \"Focus Areas\": {\"rich_text\": {}},
      \"Completed\": {\"number\": {}},
      \"Planned\": {\"number\": {}},
      \"Completion Rate\": {\"formula\": {\"expression\": \"if(prop(\\\"Planned\\\") > 0, round(prop(\\\"Completed\\\") / prop(\\\"Planned\\\") * 100), 0)\"}},
      \"Reflection\": {\"rich_text\": {}},
      \"Energy Level\": {\"select\": {\"options\": [
        {\"name\": \"🔥 High\", \"color\": \"green\"},
        {\"name\": \"😊 Normal\", \"color\": \"blue\"},
        {\"name\": \"😴 Low\", \"color\": \"yellow\"},
        {\"name\": \"💀 Burnt Out\", \"color\": \"red\"}
      ]}}
    }
  }"
```

### 选项 2：Todoist

```bash
# 1. Get API token from https://app.todoist.com/app/settings/integrations/developer
echo "BACKEND=todoist" > ~/.config/4to1/config
echo "TODOIST_API_KEY=your_token_here" >> ~/.config/4to1/config
```

**创建 4To1 规划结构：**

```bash
TODOIST_KEY=$(grep TODOIST_API_KEY ~/.config/4to1/config | cut -d= -f2)

for project in "🔭 4-Year Vision" "📊 3-Month Milestones" "🏃 2-Week Sprint" "✅ Daily Tasks" "🚫 Not-To-Do"; do
  curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
    -H "Authorization: Bearer $TODOIST_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$project\"}"
done
```

### 选项 3：Google 日历 + 任务（Google Calendar + Tasks）

```bash
echo "BACKEND=gcal" > ~/.config/4to1/config
# Requires Google OAuth — run the setup script:
python3 {baseDir}/scripts/gcal_setup.py
```

### 选项 4：本地 Markdown（无需账号）

```bash
echo "BACKEND=local" > ~/.config/4to1/config
echo "LOCAL_DIR=~/4to1-plans" >> ~/.config/4to1/config
mkdir -p ~/4to1-plans/{vision,milestones,sprints,daily,not-to-do}
```

## 核心命令

### 1. 入门 — “设置我的规划系统”

引导用户完成以下步骤：
**步骤 1：选择后端系统**（参见上述设置）

**步骤 2：制定四年愿景**（5-10 分钟的对话）
逐一提问：
1. “如果四年后您可以在任何地方——无论是职业、生活还是技能方面——那会是什么样子？”
2. “您希望在哪些方面实现最大的改变？”（职业、健康、人际关系、技能、财务）
3. “对于每个方面，四年后的成功标准是什么？请具体说明。”
4. “为了达到这个目标，您愿意放弃什么？” → 生成“禁止做的事情”列表
5. “有哪些日常习惯正在浪费您的时间？” → 生成“时间浪费”列表

对话结束后，创建以下内容：
- 包含用户答案的四年愿景文档（层级：四年愿景）
- 2-5 个具体成功的愿景领域
- 初始的“禁止做的事情”列表 + “时间浪费”列表

**步骤 3：制定三个月的里程碑**（5 分钟）
1. “在您的愿景领域中，哪1-2个领域在接下来的三个月里最需要取得进展？”
2. “哪些具体的里程碑才能代表真正的进步？”
3. “将每个目标分解为可衡量的任务。”

创建与愿景领域相关联的三个-month里程碑任务。

**步骤 4：制定两周的冲刺计划**（3 分钟）
1. “对于您的季度目标，您在接下来的两周内能完成什么？”
2. “选择 2 个主要项目和最多 5 个次要项目。”
3. “每个项目的‘完成’标准是什么？”

创建与两周冲刺计划相关联的任务。

**步骤 5：今日任务**（1 分钟）
1. “今天最重要的三项任务是什么？”
2. “每个任务服务于哪个冲刺项目？”
将所有任务记录到所选的后端系统中。

### 2. 每周回顾 — “进行每周回顾”

每周日晚上或周一早上执行回顾。请参考 {baseDir}/scripts/weekly_review.md 中的完整模板。

**回顾要点：**  
保持回顾时间在 10 分钟以内。扮演指导者的角色，而不仅仅是填写表格。

### 3. 每两周进行一次冲刺回顾

```
READ: Current 2-week sprint tasks and progress
REVIEW: What got done? What carries over? Any sprint goal changes?
PLAN: Next 2-week sprint — new primary/secondary projects
CHECK: Are sprints still aligned with 3-month milestones?
```

### 4. 每季度进行一次全面回顾

```
READ: All projects and sprint logs for the quarter
REPORT: Projects completed/stalled/abandoned, completion trend, top win, biggest blocker
ASK: Which projects continue? Which get cut? New projects? Update Not-To-Do?
WRITE: Quarterly report + next quarter's milestones
```

### 5. 每日检查 — “我今天应该关注什么？”

```
READ: Current sprint tasks + project priorities
RESPOND:
  "Based on your 2-week sprint, today's focus:
   1. [Task] → serves [3-month milestone]
   2. [Task] → serves [milestone]
   3. [Task]

   ⚠️ [Project X] hasn't had progress in a week.
   🚫 Not-To-Do reminder: You said NO to [thing]."
```

### 6. 快速添加任务 — “将 [任务] 添加到我的计划中”

解析用户输入的任务，询问它服务于哪个项目/冲刺计划。然后将其添加到后端系统中，并确保任务层级正确。

### 7. 进度检查 — “我的进展如何？”

```
READ: All data
SHOW:
  🔭 4-Year Vision: [areas and direction]
  📊 Q[X] Milestones: [X/Y complete]
  🏃 Current Sprint: [X/Y tasks done, Z% rate]
  📈 Sprint streak: X consecutive reviews
  🚫 Not-To-Do violations: [any this week?]
```

## Notion API 参考

```bash
NOTION_KEY=$(grep NOTION_API_KEY ~/.config/4to1/config | cut -d= -f2)

# Search planning pages
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "4To1"}'

# Query projects by layer
curl -s -X POST "https://api.notion.com/v1/databases/{db_id}/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"and": [
    {"property": "Status", "select": {"equals": "Active"}},
    {"property": "Layer", "select": {"equals": "2-Week Sprint"}}
  ]}}'

# Update progress
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Progress": {"number": 0.75}, "Status": {"select": {"name": "Active"}}}}'

# Create sprint log entry
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "{sprint_log_db_id}"},
    "properties": {
      "Sprint": {"title": [{"text": {"content": "2026-W07 Sprint Review"}}]},
      "Completed": {"number": 8},
      "Planned": {"number": 10},
      "Reflection": {"rich_text": [{"text": {"content": "Good sprint. Hit main milestones."}}]},
      "Energy Level": {"select": {"name": "😊 Normal"}}
    }
  }'
```

## Todoist API 参考

```bash
TODOIST_KEY=$(grep TODOIST_API_KEY ~/.config/4to1/config | cut -d= -f2)

# Get all projects
curl -s "https://api.todoist.com/rest/v2/projects" -H "Authorization: Bearer $TODOIST_KEY"

# Get active tasks in a project
curl -s "https://api.todoist.com/rest/v2/tasks?project_id={id}" -H "Authorization: Bearer $TODOIST_KEY"

# Create task linked to sprint
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_KEY" -H "Content-Type: application/json" \
  -d '{"content": "Task name", "project_id": "xxx", "priority": 4, "due_string": "next monday", "description": "Sprint: 2-Week Sprint | Milestone: Q1 Goal"}'

# Complete task
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/{id}/close" -H "Authorization: Bearer $TODOIST_KEY"
```

## 本地 Markdown 后端

```
~/4to1-plans/
├── vision.md            # 4-year vision document
├── not-to-do.md         # Not-To-Do projects + Time Wasters
├── milestones/
│   └── 2026-Q1.md       # 3-month milestone plan
├── sprints/
│   ├── 2026-W07.md      # 2-week sprint plan
│   └── 2026-W09.md
├── daily/
│   └── 2026-02-10.md    # Daily task list
└── reviews/
    ├── sprint-2026-W07.md  # Sprint review log
    └── quarterly-2026-Q1.md
```

使用 YAML 格式来组织数据：

```markdown
---
project: Launch MVP
layer: 3-month-milestone
status: active
priority: primary
progress: 45
start: 2026-01-01
end: 2026-03-31
parent_vision: "Build a profitable SaaS"
---
# Launch MVP
## Tasks (2-week sprint)
- [x] Define feature scope
- [x] Build prototype
- [ ] User testing round 1
- [ ] Iterate on feedback
```

## 自动化（Heartbeat/Cron）

对于使用 OpenClaw 并启用了 Heartbeat 或 Cron 功能的用户：
- **每周回顾提醒（周日晚上 8 点）：**
```
"Run 4to1 weekly review: read sprint progress, generate summary, ask for next week's priorities"
```

- **每日提醒（工作日早上 8 点）：**
```
"Check 4to1 plan, suggest today's top 3 focus tasks based on current 2-week sprint"
```

- **进度停滞检测（每 3 天一次）：**
```
"Check if any active 4to1 sprint project hasn't been updated in 1+ week. Alert if stalled."
```

## 规划原则

1. **遵循 4-3-2-1 的层级结构** — 每项任务都通过冲刺计划、里程碑最终连接到愿景
2. **保护“禁止做的事情”列表** — 如果用户添加了与现有计划冲突的内容，提醒他们当初为什么拒绝该任务
3. **绝不夸大进展** — 只报告实际记录的进度
4. **保持流程简洁** — 每周回顾时间不超过 5-10 分钟，每日检查时间不超过 1 分钟
5. **给予鼓励但保持诚实** — 庆祝进步，友善地指出停滞的情况
6. **以两周为周期进行规划** — 断裂是执行的核心节奏

## 更多信息

- 官网：https://4to1planner.com
- 免费入门套件：https://4to1planner.com/free-download.html
- 模板：https://4to1planner.com/shop.html
- YouTube 频道：https://www.youtube.com/@markzhou5213
- Twitter 账号：https://twitter.com/xiucat