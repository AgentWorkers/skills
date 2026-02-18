---
name: claude-usage
description: 要检查 Claude Max 计划的使用限制，请启动 Claude Code 并运行 `/usage` 命令。当用户询问 Claude 计划的使用情况、剩余配额、速率限制，或发送 `/claude_usage` 请求时，可以使用此方法。
---
# Claude 使用方法

您可以通过交互式方式运行 Claude Code 来查看您的 Claude Max 订阅使用情况。

## 前提条件

- 必须安装 `expect` 工具（在 macOS 上，该工具通常位于 `/usr/bin/expect` 路径下）。
- 必须安装并登录 Claude Code 的命令行界面（CLI）。

## 操作步骤

使用 `expect` 来自动化交互式用户界面（TUI）的操作：

1. 运行 `expect` 脚本以启动 Claude Code，并执行 `/usage` 命令：
   ```bash
   expect -c '
   spawn claude
   expect "Welcome"
   send "/usage\r"
   expect "Show plan usage"
   sleep 1
   send "\r"
   expect "Resets"
   '
   ```

2. 分析输出以获取以下信息：
   - **当前会话**：查找包含使用百分比和重置时间的 “Current session” 行。
   - **当前周（所有模型）**：查找包含使用百分比和重置日期的 “Current week (all models)” 行。
   - **当前周（仅 Sonnet 模型）**：查找包含使用百分比的 “Current week (Sonnet only)” 行。
   - **额外使用量**：查找 “Extra usage” 行。

3. 在解析输出之前，先去除其中的 ANSI 转义码。

4. 将解析后的数据格式化后呈现给用户。

## 示例输出

`expect` 脚本的输出可能如下所示：
```
Current session     ██████████░░░░░░░░░░░░░░░░░ 21% used    Resets 5:59pm (America/Los_Angeles)

Current week (all models)
████████████████████████░░░░░░░░░░░░░ 28% used    Resets Feb 21 at 6am (America/Los_Angeles)

Current week (Sonnet only)
█████████████████████████░░░░░░░░░░░░ 29% used    Resets Feb 21 at 7am (America/Los_Angeles)

Extra usage
Extra usage not enabled • /extra-usage to enable

$50 free extra usage · /extra-usage to enable
```

## 备用方案

如果 `expect` 无法使用，可以采取以下替代方案：
1. 运行 `claude auth status` 命令，以查看您的订阅类型（Max/Pro）。
2. 查看 `~/.claude/stats-cache.json` 文件，以获取本地会话令牌的数量（数据有限）。