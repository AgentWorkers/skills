---
name: hackathon-manager
description: 跟踪黑客马拉松的截止日期，管理提交任务清单，并监控项目进度。适用于管理多个黑客马拉松时，用于查看即将到期的任务、标记已完成的要求，或从URL中提取黑客马拉松的相关信息以自动填充截止日期和任务内容。
---

# Hackathon Manager

该工具用于管理多个具有截止日期、奖项和提交清单的编程竞赛。它能够自动从URL中提取竞赛详情，并跟踪参赛者的提交进度。

## 快速入门

使用 `manager.py` 脚本运行相关命令：

```bash
python scripts/manager.py <command> [args]
```

## 核心命令

### 添加竞赛

```bash
python scripts/manager.py add "Hackathon Name" "YYYY-MM-DD" "Prize Amount"
```

示例：
```bash
python scripts/manager.py add "Solana Agent Hackathon" "2026-02-12" "$50K"
```

**从URL获取信息：** 当提供竞赛URL时，使用 `web_fetch` 命令提取以下信息：
- 竞赛名称
- 截止日期
- 奖项设置
- 提交要求

然后使用提取的信息调用 `add` 命令，并更新相应的提交清单。

### 列出所有竞赛

```bash
python scripts/manager.py list
```

显示所有已跟踪竞赛的列表，包括名称、截止日期、状态和进度。

### 查看竞赛状态

```bash
python scripts/manager.py status "Hackathon Name"
```

提供详细的竞赛状态信息，包括完整的提交清单和完成情况。

### 标记完成项

```bash
python scripts/manager.py check "Hackathon Name" "Item text or number"
```

可以将清单中的项目标记为已完成。支持以下两种方式：
- 输入项目完整文本：`check "Solana Agent" "Deploy to devnet"`
- 输入项目编号：`check "Solana Agent" "2"`

### 查看即将举行的竞赛

```bash
python scripts/manager.py upcoming [days]
```

显示接下来N天内（默认为7天）即将举行的竞赛，按紧急程度排序，并提供可视化提示。

### 文本日历视图

```bash
python scripts/manager.py calendar [month] [year]
```

以文本形式显示竞赛日程：
- `R` = 注册开放
- `W` = 工作期开始
- `D` = 提交截止日期

## 与Google日历的集成

使用 `gog` CLI将竞赛信息同步到Google日历。需要先安装并登录 [gog](https://github.com/rubiojr/gog)。

### 列出日历事件

```bash
python scripts/manager.py gcal list
```

显示Google日历中所有与竞赛相关的事件。

### 同步到日历

```bash
python scripts/manager.py gcal sync
```

为所有已跟踪的竞赛创建Google日历事件：
- `[REG]` - 注册开放（定时事件）
- `[WORK]` - 工作期（全天事件）
- `[DEADLINE]` - 提交截止日期（定时事件）

### 从日历中删除事件

```bash
python scripts/manager.py gcal remove "Hackathon Name"
```

删除日历中与竞赛名称匹配的所有事件。

**Windows用户注意：** 该工具会自动配置Go时区数据库。如果出现时区相关错误，请确保 `~/.gog/zoneinfo.zip` 文件存在。

## 工作流程

**当用户提及竞赛时：**

1. **从URL添加竞赛：** 如果用户提供竞赛链接：
   - 使用 `web_fetch` 获取竞赛页面信息
   - 提取竞赛名称、截止日期、奖项和提交要求
   - 调用 `add` 命令
   - 根据要求更新提交清单

2. **手动添加竞赛：** 如果用户提供详细信息：
   - 使用提供的信息调用 `add` 命令
   - 询问需要跟踪哪些清单项目

3. **查看竞赛状态：** 当用户询问“哪些竞赛即将截止？”或“有哪些竞赛？”时：
   - 调用 `list` 或 `upcoming` 命令
   - 显示相关信息

4. **管理进度：** 当用户表示已完成某项任务时：
   - 确定对应的竞赛和项目
   - 调用 `check` 命令
   - 确认任务已完成

## 数据存储

竞赛信息存储在 `~/.openclaw/workspace/hackathons.json` 文件中（格式为JSON）：

```json
{
  "hackathons": [
    {
      "name": "Hackathon Name",
      "deadline": "YYYY-MM-DD",
      "prize": "$50K",
      "status": "active",
      "checklist": ["Item 1", "Item 2"],
      "completed": ["Item 1"]
    }
  ]
}
```

## 与HACKATHONS.md文件的集成

如果工作区中存在 `HACKATHONS.md` 文件：
- 读取该文件以发现尚未添加到JSON数据库中的竞赛
- 建议将其导入
- 在添加新竞赛时保持两个文件的同步

## 其他说明：

- 数据存储路径：`~/.openclaw/workspace/hackathons.json`
- 与Google日历的集成需要 [gog CLI](https://github.com/rubiojr/gog)
- 日历事件前缀为 `[REG]`、`[WORK]` 或 `[DEADLINE` 以便于识别
- `gcal remove` 命令会根据事件标题中的竞赛名称删除日历事件