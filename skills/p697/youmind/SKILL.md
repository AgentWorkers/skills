---
name: youmind
description: 使用此技能通过 HTTP API 来操作 Youmind。浏览器仅用于登录、页面刷新以及查看板面（board）、材料（material）和聊天（chat）内容；这些操作均需通过 API 来完成。
---
# Youmind API 技能

Youmind 的所有操作均基于 API，适用于本地 AI 代理。

## 核心规则

- 所有业务操作 **仅** 通过 API 进行。
- 浏览器自动化仅用于身份验证的初始化/刷新。

## 身份验证

```bash
python scripts/run.py auth_manager.py status
python scripts/run.py auth_manager.py validate
python scripts/run.py auth_manager.py setup
```

## 板块 API

```bash
# List boards
python scripts/run.py board_manager.py list

# Find boards by name/id keyword
python scripts/run.py board_manager.py find --query "roadmap"

# Get board detail
python scripts/run.py board_manager.py get --id <board-id>

# Create board
python scripts/run.py board_manager.py create --name "My Board"
python scripts/run.py board_manager.py create --name "My Board" --prompt "Initialize this board for AI coding agent research"
```

## 材料 API

```bash
# Add link to board
python scripts/run.py material_manager.py add-link --board-id <board-id> --url "https://example.com"

# Upload local file to board
python scripts/run.py material_manager.py upload-file --board-id <board-id> --file /path/to/file.pdf

# Get snips by IDs
python scripts/run.py material_manager.py get-snips --ids "<snip-id-1>,<snip-id-2>"

# List picks (if available)
python scripts/run.py material_manager.py list-picks --board-id <board-id>
```

## 聊天 API

```bash
# Create new chat with first message
python scripts/run.py chat_manager.py create --board-id <board-id> --message "Summarize key ideas"

# Send to existing chat
python scripts/run.py chat_manager.py send --board-id <board-id> --chat-id <chat-id> --message "Give next steps"

# Chat history/detail
python scripts/run.py chat_manager.py history --board-id <board-id>
python scripts/run.py chat_manager.py detail --chat-id <chat-id>
python scripts/run.py chat_manager.py detail-by-origin --board-id <board-id>

# Generation via chat
python scripts/run.py chat_manager.py generate-image --board-id <board-id> --prompt "Minimal blue AI poster"
python scripts/run.py chat_manager.py generate-slides --board-id <board-id> --prompt "6-page AI coding agent roadmap"
```

## 兼容性封装层

```bash
python scripts/run.py ask_question.py --board-id <board-id> --question "..."
python scripts/run.py ask_question.py --board-id <board-id> --chat-id <chat-id> --question "..."
```

## 数据

本地身份验证状态：

```text
data/
├── auth_info.json
└── browser_state/
    └── state.json
```

请勿对 `data/` 目录进行任何修改。