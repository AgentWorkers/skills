---
name: beeper
description: 搜索并浏览本地的 Beeper 聊天记录（包括主题、消息以及支持全文搜索功能）。
homepage: https://github.com/krausefx/beeper-cli
metadata: {"clawdbot":{"emoji":"🛰️","os":["darwin","linux"],"requires":{"bins":["beeper-cli"]},"install":[{"id":"go","kind":"go","pkg":"github.com/krausefx/beeper-cli/cmd/beeper-cli","bins":["beeper-cli"],"label":"Install beeper-cli (go install)"}]}}
---

# Beeper CLI

[Beeper](https://www.beeper.com/) 是一款通用的聊天应用，可以将来自 WhatsApp、Telegram、Signal、iMessage、Discord 等平台的消息统一显示在一个收件箱中。

此技能提供了对您本地 Beeper 聊天记录的**只读访问**权限。您可以浏览聊天记录、搜索消息并提取对话数据。

## 必备条件
- 安装了 Beeper 桌面应用程序（该应用程序会生成 SQLite 数据库）
- `beeper-cli` 命令行工具已在系统的 PATH 环境变量中

## 数据库路径
CLI 会自动检测以下路径：
- `~/Library/Application Support/BeeperTexts/index.db`（macOS）
- `~/Library/Application Support/Beeper/index.db`（macOS）

您也可以通过以下参数自定义数据库路径：
- `--db /path/to/index.db`
- `BEEPER_DB=/path/to/index.db`

## 命令

### 列出所有聊天记录
```bash
beeper-cli threads list --days 7 --limit 50 --json
```

### 查看聊天记录详情
```bash
beeper-cli threads show --id "!abc123:beeper.local" --json
```

### 显示聊天记录中的所有消息
```bash
beeper-cli messages list --thread "!abc123:beeper.local" --limit 50 --json
```

### 搜索消息（全文本）
```bash
# Simple search
beeper-cli search 'invoice' --limit 20 --json

# Phrase search
beeper-cli search '"christmas party"' --limit 20 --json

# Proximity search
beeper-cli search 'party NEAR/5 christmas' --limit 20 --json

# With context window (messages before/after match)
beeper-cli search 'meeting' --context 6 --window 60m --json
```

### 查看数据库信息
```bash
beeper-cli db info --json
```

## 注意事项
- **仅限读取**：此工具不会发送任何消息。
- **JSON 输出**：请务必使用 `--json` 选项以获得结构化输出，以便其他工具能够解析数据。
- **FTS5 搜索**：利用 Beeper 内置的全文索引（FTS5）进行快速搜索。
- **私信名称解析**：可以选择通过外部数据库解析私信发送者的名称（使用 `--no-bridge` 选项可禁用此功能）。

## 安装方法

### 方法 1：使用 Go 语言进行安装（推荐）
```bash
go install github.com/krausefx/beeper-cli/cmd/beeper-cli@latest
```

### 方法 2：从源代码编译安装
```bash
git clone https://github.com/krausefx/beeper-cli.git
cd beeper-cli
go build ./cmd/beeper-cli
# Move beeper-cli to PATH, e.g., /usr/local/bin
```

## 使用示例

- 搜索上周与工作相关的消息：
```bash
beeper-cli threads list --days 7 --json | jq '.threads[] | select(.name | contains("work"))'
beeper-cli search 'project deadline' --limit 10 --json
```

- 查找包含具体上下文的发票相关消息：
```bash
beeper-cli search 'invoice' --context 3 --json
```