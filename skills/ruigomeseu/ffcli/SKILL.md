---
name: ffcli
description: 查询 Fireflies.ai 的会议数据。适用于搜索会议、查看会议记录、阅读 AI 摘要、提取待办事项，或查找会议中讨论的内容。该功能可通过以下关键词触发：`meeting notes`（会议记录）、`transcript`（会议记录文本）、`action items from meeting`（会议中的待办事项）、`what was discussed`（会议讨论内容）、`fireflies`（Fireflies AI 相关内容）、`meeting summary`（会议总结）。
metadata: {"openclaw":{"requires":{"bins":["ffcli"],"env":["FIREFLIES_API_KEY"]},"primaryEnv":"FIREFLIES_API_KEY","install":[{"id":"brew","kind":"brew","formula":"ruigomeseu/tap/ffcli","bins":["ffcli"],"label":"Install ffcli (Homebrew tap)"},{"id":"npm","kind":"node","package":"@ruigomeseu/ffcli","bins":["ffcli"],"label":"Install ffcli (npm)"}]}}
---
# ffcli — Fireflies.ai 命令行工具

用于查询 Fireflies.ai 的会议记录、会议文字记录以及 AI 生成的会议摘要。

## 设置

通过 Homebrew 或 npm 安装：

```bash
brew install ruigomeseu/tap/ffcli
# or
npm install -g @ruigomeseu/ffcli
```

使用您的 Fireflies API 密钥进行身份验证（请从 [设置 → 开发者设置](https://app.fireflies.ai/settings) 获取）：

```bash
ffcli auth <your-api-key>    # Store key locally (~/.config/ffcli/)
ffcli auth --check           # Verify it works
```

或者，您可以设置 `FIREFLIES_API_KEY` 环境变量（该变量优先于本地配置文件中的设置）。在 OpenClaw 中，您可以通过 `openclaw.json` 文件中的 `skills.entries.ffcli.apiKey` 来配置此密钥。

**注意：** `ffcli` 是由 @ruigomeseu 开发的第三方命令行工具（可通过 Homebrew 或 npm 安装）。在安装前，请核实其来源：查看 [npm 包页](https://www.npmjs.com/package/@ruigomeseu/ffcli) 或 [Homebrew 仓库](https://github.com/ruigomeseu/homebrew-tap)，以了解代码审查和发布历史。

## 命令

### 列出所有会议
```bash
ffcli list --limit 10 --md                           # Recent meetings
ffcli list --from 2026-02-01 --to 2026-02-12 --md    # Date range
ffcli list --participant vinney@opennode.com --md     # By participant
ffcli list --search "standup" --md                    # By title keyword
ffcli list --limit 5 --include-summaries              # With AI summaries (JSON)
```

### 显示会议详情
```bash
ffcli show <id> --md                    # Full detail (markdown)
ffcli show <id> --summary-only --md     # Just AI summary
ffcli show <id> --transcript-only --md  # Just transcript
ffcli show <id> --include-transcript --md  # Detail + transcript
```

### 查看用户信息
```bash
ffcli me --md                           # Account info, transcript count
```

### 脚本模式
```bash
# Action items from recent meetings
ffcli list --limit 10 --include-summaries | jq '.[].summary.action_items'

# All meeting IDs from a date range
ffcli list --from 2026-02-01 --to 2026-02-07 | jq -r '.[].id'

# Export a summary to file
ffcli show <id> --summary-only --md > meeting-summary.md
```

## 注意事项
- 默认输出格式为 JSON。若需可读性更强的输出格式，可使用 `--md` 选项。
- 使用 `--include-summaries` 选项时，会包含 AI 生成的会议摘要（但会增加响应数据量）。
- 使用 `show` 命令时需要会议 ID，该 ID 可通过 `list` 命令获取。
- JSON 输出中的日期采用 UTC 格式。