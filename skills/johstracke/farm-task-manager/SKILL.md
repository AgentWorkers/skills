# 农场任务管理器

*支持日常、每周及季节性农场工作的任务调度与优先级管理。*

**作者:** IOU (@johstracke)  
**版本:** 1.0.0  
**创建日期:** 2026-02-12  

---

## 关于本工具  

农场任务管理器帮助农民有效地安排日常、每周及季节性的农场工作，包括任务调度、优先级设定和任务跟踪。非常适合以下人群：  
- 小型农场主（1-10英亩土地）  
- 业余农场主  
- 直营农产品的农户  
- 需要同时处理多项农场事务的人  

### 我为何开发此工具  

我开发农场任务管理器的原因是：农场工作繁杂，总是有各种事情需要处理（种植、维护、收割、动物照料、设备维修等）。如果仅依靠记忆来管理，很容易忘记重要任务、错误地安排优先级，从而浪费时间。现在，只需输入 `farm-task add "修复灌溉" --priority high`，之后就可以安心等待任务完成即可。  

---

## 主要功能  

- **任务管理**：可以添加任务，包括任务名称、描述、优先级、截止日期和负责人。  
- **任务过滤**：可根据任务状态、优先级、类别、截止日期或负责人进行筛选。  
- **任务更新**：可以更新任务状态（待处理、进行中、已完成），并添加备注。  
- **重复任务**：支持创建每日、每周、每月或季节性的重复任务。  
- **搜索**：可以按任务名称、描述或类别进行搜索。  
- **导出**：可将任务数据导出为Markdown或JSON格式，便于分享或备份。  

---

## 使用方法  

### 添加任务  

```bash
farm-task add "Check irrigation system" \
  --priority high \
  --category maintenance \
  --due "2026-03-01" \
  --assignee "John"
```  

**选项：**  
- `--name`：任务名称（必填）  
- `--description`：任务描述  
- `--priority`：任务优先级（高、中、低）  
- `--status`：任务状态（待处理、进行中、已完成）  
- `--category`：任务类别（种植、维护、收割、设备、动物、建筑、其他）  
- `--due`：截止日期（YYYY-MM-DD 或 YYYY-MM-DD HH:MM）  
- `--assignee`：任务负责人  

### 列出任务  

```bash
# List all tasks
farm-task list

# Filter by status
farm-task list --status pending

# Filter by priority
farm-task list --priority high

# Filter by category
farm-task list --category planting

# Filter by due date (show overdue first)
farm-task list --sort-due

# Filter by assignee
farm-task list --assignee "John"
```  

### 查看任务详情  

```bash
farm-task show 1
```  

显示任务详情，包括：  
- 任务信息  
- 状态和优先级  
- 截止日期  
- 备注和历史记录  
- 创建时间  

### 更新任务状态  

```bash
# Mark as in-progress
farm-task update 1 --status in-progress

# Mark as complete
farm-task update 1 --status complete

# Add note to task
farm-task update 1 --note "Checked valves, all good"

# Change priority
farm-task update 1 --priority medium
```  

### 添加重复任务  

```bash
# Daily task
farm-task recurring "Check chicken water" \
  --frequency daily \
  --priority medium \
  --category animals

# Weekly task
farm-task recurring "Inspect tractor oil" \
  --frequency weekly \
  --priority high \
  --category equipment

# Monthly task
farm-task recurring "Test fire extinguishers" \
  --frequency monthly \
  --priority medium \
  --category buildings

# Seasonal task (March 1st)
farm-task recurring "Winterize irrigation" \
  --frequency seasonal \
  --season "03-01" \
  --priority high \
  --category maintenance
```  

### 完成任务  

```bash
farm-task complete 1
```  

将任务标记为已完成，并记录完成时间。  

### 删除任务  

```bash
farm-task delete 1
```  

从系统中删除任务。  

### 导出任务  

```bash
# Export all to markdown
farm-task export --file tasks.md

# Export filtered to markdown
farm-task export --file planting-tasks.md --category planting

# Export to JSON
farm-task export --file tasks.json --format json

# Export by date range
farm-task export --file march-tasks.md --after "2026-03-01" --before "2026-04-01"
```  

---

## 安全性  

✅ **安全性验证**：该工具通过路径验证来防止未经授权的文件访问。  
所有文件操作仅限于安全目录：  
- 工作区：`~/.openclaw/workspace/farm-task-manager/`  
- 主目录：`~/`（用户控制）  

**禁止访问的路径：**  
- 系统目录（`/etc`、`/usr`、`/var` 等）  
- 敏感文件（`~/.ssh`、`~/.bashrc` 等）  

无硬编码的敏感信息，也不会执行任意代码。所有操作均经过输入验证。  

---

## 数据存储  

任务数据以JSON格式存储在：  
`~/.openclaw/workspace/farm-task-manager/tasks.json`  
该目录会在首次使用时自动创建。  

---

## 任务类别  

| 类别 | 描述 |  
|----------|-------------|  
| 种植 | 播种、移栽、土壤准备 |  
| 维护 | 一般农场维护、设备修理 |  
| 收获 | 收割活动、收尾工作 |  
| 设备 | 设备维护、修理、存储 |  
| 动物 | 动物照料、喂食、健康检查 |  
| 建筑 | 谷仓、棚屋、温室维护 |  
| 其他 | 其他农场相关任务 |  

---

## 优先级级别  

| 优先级 | 描述 |  
|-----------|-------------|  
| 高 | 紧急，需立即处理（涉及安全或时间敏感的问题） |  
| 中 | 重要，尽快完成（常规任务，具有灵活性） |  
| 低 | 可选，有空时处理（优化或改进事项） |  

---

## 使用示例  

### 日常工作安排  

```bash
# Morning check
farm-task list --sort-due --status pending

# Complete chicken check
farm-task complete 5
farm-task recurring generate 5  # Generate next day's recurring task
```  

### 周期性计划  

```bash
# List high priority tasks
farm-task list --priority high

# Export for planning
farm-task export --file weekly-plan.md --after "today" --before "7 days"
```  

### 季节性工作  

```bash
# Winter preparation
farm-task recurring "Winterize irrigation" \
  --frequency seasonal \
  --season "11-01" \
  --priority high \
  --category maintenance

# Spring planting
farm-task export --file spring-tasks.md --category planting --after "2026-03-01" --before "2026-06-01"
```  

---

## 常见问题解答  

### 问：如何跟踪多个工作人员的工作进度？  
**答：** 在添加任务时使用 `--assignee` 选项。通过筛选负责人来查看每个人的任务进度：  
```bash
farm-task list --assignee "Jane"
```  

### 问：可以更改任务的优先级吗？  
**答：** 可以，使用更新命令来修改优先级：  
```bash
farm-task update 1 --priority high
```  

### 问：重复任务是如何运作的？  
**答：** 重复任务是基于模板创建的。完成任务后，系统会自动生成新的任务实例（包含相同的信息和更新的截止日期）。  

### 问：如何管理项目相关的任务？  
**答：** 可以使用类别来分类相关任务：  
```bash
farm-task add "Build new fence" --category buildings --assignee "John"
farm-task list --category buildings
```  

### 问：如何导出任务数据以供分享？  
**答：** 可将任务数据导出为Markdown或JSON格式：  
```bash
# Markdown (human-readable)
farm-task export --file farm-plan.md

# JSON (for data interchange)
farm-task export --file farm-tasks.json --format json
```  

---

## 版本历史  

- **1.0.0**（2026-02-12）：初始版本  
  - 支持任务的基本管理功能（添加、列出、查看、更新、删除、完成）  
  - 支持按状态、优先级、类别、截止日期或负责人筛选任务  
  - 支持创建每日、每周、每月或季节性的重复任务  
  - 支持全任务搜索  
  - 支持导出为Markdown和JSON格式  

---

## 技术支持  

如遇到问题或需要功能建议，请联系作者：@johstracke（ClawHub）。  
同时，敬请期待IOU团队推出的其他农业相关工具！  

*农场任务管理器——帮助您整理农场工作，减少压力，再也不会忘记任何重要任务！*