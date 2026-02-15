---
name: codex-monitor
description: 您可以浏览存储在 `~/.codex/sessions` 目录中的 OpenAI Codex 会话日志。这些日志可以通过位于 `~/Developer/CodexMonitor` 的本地 Swift 项目进行查看、列表展示或实时监控。
---

# codex-monitor

使用此技能可以在Oliver的机器上查询Codex会话信息。

## 工作原理
该技能会从本地项目中的Swift可执行文件运行程序：
- 命令行工具（CLI）：`swift run CodexMonitor-CLI ...`
- 应用程序：`swift run CodexMonitor-App`

## 命令

### 列出所有会话
- 按日期：`python3 skills/codex-monitor/codex_monitor.py list 2026/01/08`
- 按日期（JSON格式）：`python3 skills/codex-monitor/codex_monitor.py list --json 2026/01/08`
- 按月份：`python3 skills/codex-monitor/codex_monitor.py list 2026/01`
- 按年份：`python3 skills/codex-monitor/codex_monitor.py list 2026`

### 显示特定会话
- 按会话ID显示：`python3 skills/codex-monitor/codex_monitor.py show <session-id>`
- 显示指定范围内的会话：`python3 skills/codex-monitor/codex_monitor.py show <session-id> --ranges 1...3,26...28`
  - 无范围限制：`--ranges 5...`（从第5个会话开始显示）
  - 显示指定范围内的会话：`--ranges ...10`（从第一个会话显示到第10个会话）

### 显示会话信息（JSON格式）
- `python3 skills/codex-monitor/codex_monitor.py show <session-id> --json`

### 监控会话变化
- 监控所有会话的变化：`python3 skills/codex-monitor/codex_monitor.py watch`
- 监控特定会话的变化：`python3 skills/codex-monitor/codex_monitor.py watch --session <session-id>`

### 通过菜单栏监控会话
- 启动菜单栏监控功能：`python3 skills/codex-monitor/codex_monitor.py monitor`

## 注意事项
- 底层的CLI工具可能会更新；此封装层会传递额外的参数。
- 如果Swift编译过程较慢，建议先编译一次（`swift build`），然后再运行编译后的二进制文件。