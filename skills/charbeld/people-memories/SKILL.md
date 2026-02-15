---
name: people-memories
description: 记录关于你所提到的人的简短个人笔记，将这些笔记存储在一个轻量级的数据库中。以后当你需要了解这些人的相关信息时，可以随时查阅这些记录。这种功能特别适用于需要记住某人的偏好设置、提醒事项，或是某个人的相关背景信息的情况，而无需翻阅之前的聊天记录。
---

# 人物记忆功能

## 目的
该功能用于存储与您交流过的人的相关信息，这些信息具有短暂的有效期且可被搜索，以便您的助手能够立即回忆起后续需要处理的事项。该功能支持以下操作：
- 通过语音或文本指令执行 `remember` 命令，以保存备注、偏好设置及相关上下文信息。
- 生成并导出个人的信息摘要（即“个人资料卡”）。
- 提供搜索、回忆和列表功能，便于快速查找相关信息。
- 可选地，当您说出“remember …”时，系统会自动触发该命令。

## 结构与存储方式
当前，`~/.clawdbot/people-memory.json` 文件用于存储数据：
```
{
  "people": {
    "alex": {
      "displayName": "Alex",
      "notes": [
        {
          "timestamp": "2026-01-29T12:05:00Z",
          "note": "Likes cats and doing late-night music practice",
          "source": "voice",
          "tags": ["pets", "music"]
        }
      ]
    }
  },
  "index": {
    "music": ["alex"],
    "cats": ["alex"]
  }
}
```
- 名字被统一处理为小写格式（作为键值对的键），但实际存储的是显示名称。
- 每条记录包含 `timestamp`（时间戳）、`note`（备注内容）、`source`（信息来源）和 `tags`（标签）。
- 一个 `index` 映射表用于将关键词与对应的人员信息关联起来，以实现超快速搜索。

## 命令行接口（CLI）命令
可以使用提供的脚本来管理数据库：
```
skills/people-memories/scripts/people_memory.py <command> [options]
```
- `remember --person Alex --note "loves chai" --tags drinks, preferences` – 添加一条关于 Alex 的备注。
- `recall --person Alex --limit 3` – 读取 Alex 的最新备注。
- `summarize --person Alex` – 打印 Alex 的个人资料卡，包括备注数量和标签信息。
- `search --query coffee` – 查找备注中包含 “coffee” 关键字的人员。
- `export --person Alex --format md --out ~/Desktop/alex.md` – 将 Alex 的备注内容导出为 Markdown 或 JSON 格式。
- `list` – 列出所有存储的人员及其备注数量。

## 自动捕获功能（语音/聊天）
`extensions/people-memories` 扩展程序会监听 `/voice-chat` 转录内容。当您说出类似 “remember Alex likes cats” 的指令时，系统会自动执行 `remember` 命令并记录备注。索引会在后台更新，除非您明确要求，否则系统不会显示确认信息。

## 提醒与自动化
每当备注中提及生日或纪念日时，系统会附加相应的元数据（事件类型和日期）。一个定时任务（cron job）会每天早上运行 `python3 skills/people-memories/scripts/people_memory.py reminders --days 0 --window 7 --format message` 命令，通过 Telegram 向您发送下周的生日/纪念日提醒。如果您希望调整提醒频率或渠道，可以重新运行该命令或修改任务调度。

## 本版本的改进之处：
1. **智能索引**：通过标签和关键词提取技术，确保索引始终保持最新状态，即使在多次使用相同形容词的情况下也能准确匹配人员信息。
2. **摘要生成与导出**：能够快速生成个人资料卡或可共享的 Markdown/JSON 文件。
3. **语音集成与日志记录**：系统会自动将聊天内容同步到数据库中，无需手动输入命令。
4. **结构化数据**：统一化的键值格式、时间戳以及标签元数据使得其他工具（如定时任务、仪表盘）能够更方便地使用这些存储的数据。

## 下一步计划/附加功能：
- 通过运行时 `api.message` 助手功能，添加可选的确认回复（例如 “已记录，为 Alex 保存”）。
- 将该功能与提醒系统或定时任务集成，以便自动触发针对特定标签（如 “birthday”）的提醒。
- 开发一个简单的用户界面（网页或终端界面），用于预览最新的个人资料卡。

请告诉我您希望优先实现哪些自动化功能（例如优先级筛选、通知机制、跨代理同步等）。