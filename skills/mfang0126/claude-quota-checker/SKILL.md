---
name: claude-quota-checker
description: "查看您剩余的 Claude Max/Claude Pro 订阅额度——而不是您已经花费的金额。大多数使用工具只会记录 API 费用或令牌成本，但这个工具能真正回答您关心的问题：“我的订阅额度是否即将用完？”它会显示会话窗口、每周周期内的剩余使用百分比，以及具体的额度重置时间。该工具通过 tmux 自动执行 Claude Code CLI 的 `/usage` 命令来实现这一功能，无需任何 API 密钥或管理员权限，也不会涉及逆向工程。只需查看您的订阅状态即可。每当有人询问“我还有多少Claude订阅额度？”、“我是否受到了速率限制？”、“我的额度什么时候会重置？”、“我想查看我的使用情况”等问题时，都可以使用这个工具。此外，当用户遇到速率限制或 Claude 运行缓慢的情况时，它也可以作为初步的诊断工具。"
---
# Claude 配额检查器

**你的 Claude 余额还剩多少？**

大多数工具只能告诉你已经使用了多少资源，而这个工具能告诉你还剩下多少资源——这在你担心超出使用限制时才是真正重要的信息。

该工具通过自动执行 `tmux` 的 `/usage` 命令来检查你的 Claude Max/Pro 订阅配额。无需 API 密钥或管理员权限，也无需复杂的设置。

## 工作原理

1. 创建一个包含临时 Git 仓库的 tmux 会话。
2. 启动 Claude Code CLI。
3. 自动处理“信任此文件夹”的提示。
4. 发送 `/usage` 命令。
5. 捕获并解析命令的输出结果。
6. 清理 tmux 会话。

## 使用方法

```bash
bash ./scripts/check-usage.sh
```

> **注意**：请从技能目录中运行该脚本，或者根据安装路径使用完整的路径。脚本会自动检测自己的位置。

## 输出结果

- **计划类型**：Pro 或 Max（例如：“Opus 4.6 — Claude Max”）
- **会话使用情况**：当前会话的使用百分比
- **每周使用情况**：所有模型的使用百分比以及仅使用 Sonnet 模型的使用百分比
- **配额重置时间**：每周配额重置的时间

## 错误处理

| 问题 | 症状 | 解决方法 |
|---------|---------|-----|
| 未安装 tmux | 报错：“command not found: tmux” | 使用 `brew install tmux` 安装 tmux |
| Claude CLI 未添加到 PATH 中 | 会话卡住 | 安装 Claude Code CLI，并确保 `claude` 在 PATH 中 |
- 认证过期 | 输出提示“Please log in” | 手动运行 `claude` 并重新认证 |
- 未安装 git | 脚本在 `git init` 时失败 | 使用 `brew install git` 安装 git |

如果脚本运行超过 15 秒仍未响应，很可能是因为 Claude CLI 无法启动。可以使用以下命令终止会话：`tmux kill-session -t cu-*`

## 系统要求

- macOS 或 Linux 操作系统
- 已安装 tmux
- Claude Code CLI 在 PATH 中
- 活跃的 Claude Pro/Max 订阅
- 已安装 git（用于创建临时 Git 仓库）

## 性能

执行时间约为 8-10 秒（瓶颈在于 Claude Code CLI 的启动时间）。

## 限制

- 仅检查 **订阅** 使用情况（Pro/Max），不支持 API 计费
- 需要一个正在运行的终端环境（在沙箱容器中无法使用）
- 输出解析依赖于 Claude Code CLI 的 `/usage` 格式；如果 Anthropic 更改了输出格式，可能会导致解析错误