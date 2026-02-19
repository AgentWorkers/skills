---
name: claude-usage
description: 检查 Claude 的代码使用情况以及 Claude Max 的使用限制。当用户询问使用量、限制、配额或剩余的 Claude 容量时，执行此操作。
homepage: https://github.com/aligurelli/clawd
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["claude"], "pty": true }
      }
  }
---
# Claude 使用情况检查器

该工具会以交互式方式（通过 PTY 接口）启动 Claude CLI，并读取 `/usage` 命令的输出结果，以显示您的 Claude Code 或 Claude Max 的使用额度。

## 先决条件
- 必须已安装 **Claude CLI**（使用 `npm i -g @anthropic-ai/claude-code` 进行安装），并且需要登录。
- 如果运行 `claude` 时出现 “Missing API key” 的提示，用户需要先手动登录：打开终端，运行 `claude`，然后完成浏览器登录流程。
- 该工具需要一个交互式的 PTY（Terminal Protocol Interface）环境——Claude 会在此环境下启动一个本地进程并读取其输出结果（仅显示使用额度信息）。

## 操作步骤
1. 使用 PTY 启动 `claude`。
2. 等待欢迎界面出现。
3. 输入 `/usage` 并按回车键。
4. 查看输出结果（等待使用数据显示完毕）。
5. 使用 Escape 键关闭终端，然后输入 `/exit` 退出程序。
6. 报告使用情况结果。

## 命令示例
```bash
# Launch claude with PTY
exec pty=true command="claude"

# Wait and check log
process action=poll sessionId=XXX timeout=5000

# Send /usage
process action=send-keys sessionId=XXX literal="/usage"
process action=send-keys sessionId=XXX keys=["Enter"]

# Read output
process action=poll sessionId=XXX timeout=5000

# Exit
process action=send-keys sessionId=XXX keys=["Escape"]
process action=send-keys sessionId=XXX literal="/exit"
process action=send-keys sessionId=XXX keys=["Enter"]
```

## 注意事项
- 如果看到 “Missing API key” 的提示，请告知用户需要登录；基于浏览器的登录方式在无界面上无法使用。
- 在每次请求数据之间请稍等几秒钟——Claude CLI 的启动过程可能较慢。
- “Current week” 表示的是每周的使用情况，而非每日。

## 输出格式
输出结果将以表格形式显示：

| 使用情况 | 重置时间 |
|---------|---------|
| **当前会话** | 使用了 X% | 今天时间：HH:MM（时区） |
| **每周使用情况（所有模型）** | 使用了 X% | 今天时间：HH:MM（时区） |
| **每周使用情况（仅 Sonnet 模型）** | 使用了 X% | 今天时间：HH:MM（时区） |
| **额外使用情况** | 使用了 X% / 花费了 $X（总费用为 $Y） | 日期：HH:MM（时区） |

请始终显示重置时间。CLI 会以 “Resets Xpm” 的格式显示重置时间，请将其转换为 HH:MM 的格式。