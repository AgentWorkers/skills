---
name: codexmonitor
version: 0.2.1
description: >
  List/inspect/watch local OpenAI Codex sessions (CLI + VS Code) using the
  CodexMonitor Homebrew formula. Reads sessions from ~/.codex/sessions by default
  (or via CODEX_SESSIONS_DIR / CODEX_HOME overrides). Requires the cocoanetics/tap
  Homebrew tap.
homepage: https://github.com/Cocoanetics/CodexMonitor
metadata:
  moltbot:
    emoji: "🧾"
    os: ["darwin"]
    requires:
      bins: ["codexmonitor"]
    install:
      - id: brew
        kind: brew
        formula: cocoanetics/tap/codexmonitor
        bins: ["codexmonitor"]
        label: "Install codexmonitor (brew)"
  openclaw:
    requires:
      bins: ["codexmonitor"]
    install:
      - id: brew
        kind: brew
        formula: cocoanetics/tap/codexmonitor
        bins: ["codexmonitor"]
        label: "Install codexmonitor via Homebrew"
---

# codexmonitor

使用 `codexmonitor` 可以浏览本地的 OpenAI Codex 会话。

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 常用命令

- 列出所有会话（按日期）：`codexmonitor list 2026/01/08`
- 列出所有会话（按日期，以 JSON 格式）：`codexmonitor list --json 2026/01/08`
- 显示特定会话：`codexmonitor show <session-id>`
- 显示指定范围内的会话：`codexmonitor show <session-id> --ranges 1...3,26...28`
- 以 JSON 格式显示会话详情：`codexmonitor show <session-id> --json`
- 实时监控所有会话：`codexmonitor watch`
- 实时监控特定会话：`codexmonitor watch --session <session-id>`

## 注意事项
- 默认情况下，会话文件存储在 `~/.codex/sessions/YYYY/MM/DD/` 目录下。
- 如果会话文件存储在其他位置，请设置 `CODEX_SESSIONS_DIR`（推荐）或 `CODEX_HOME`。
- 可以通过会话 ID 通过 Codex 恢复或追加会话内容：`codex exec resume <SESSION_ID> "message"`。