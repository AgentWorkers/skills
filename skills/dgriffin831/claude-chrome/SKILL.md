---
name: claude-chrome
description: 您可以使用 Chrome 浏览器的扩展程序“Claude Code”来进行网页浏览和自动化任务。这是 OpenClaw 内置浏览器工具的替代方案。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"anyBins":["claude"]}}}
---

# Claude Chrome — 通过 Claude Code 实现浏览器自动化

利用 Claude Code 的 Chrome 集成功能，您可以浏览网页、与页面交互以及自动化执行浏览器任务。这是 OpenClaw 内置浏览器工具（Chrome Relay、OpenClaw Profile）的替代方案。

## 先决条件

1. 在节点上安装了 **Claude Code**（例如：`/opt/homebrew/bin/claude`）。
2. 在 Chrome 中安装并启用了 **Claude Code Chrome 扩展程序**。
3. 节点上正在运行 **Chrome** 浏览器。

## 工作原理

Claude Code 可以通过其内置的浏览器扩展程序（MCP 服务器）连接到 Chrome。启用该扩展后，Claude Code 将获得浏览器功能，例如：导航页面、点击元素、填写表单、读取内容等。

## 第一步：检查 Chrome 扩展程序是否处于活动状态

查看系统中的原生主机进程以确认 Chrome 扩展程序是否正在运行：

```bash
nodes.run node=<your-node-id> command='["bash", "-lc", "pgrep -f \"claude --chrome-native-host\""]'
```

如果返回了进程 ID（PID），则表示 Chrome 扩展程序已激活并可用。

## 第二步：使用 Claude Code 与 Chrome 一起运行

使用 `nodes.run` 命令在节点上执行浏览器任务：

```bash
nodes.run node=<your-node-id> commandTimeoutMs=120000 command='["bash", "-lc", "claude --dangerously-skip-permissions --chrome -p \"Go to example.com and read the headline\""]'
```

**常用参数：**
- `--dangerously-skip-permissions` — 自动批准所有操作（自动化任务必需）
- `--chrome` — 启用 Chrome 浏览器集成
- `-p` / `--print` — 非交互式输出模式（自动化任务必需）
- `bash -lc` — 以登录 shell 运行命令，确保环境变量 PATH 被正确加载

**超时设置：** 请参考以下基准测试建议：
- **简单任务（单页内容读取）**：`commandTimeoutMs=30000`（30 秒）
- **中等复杂度任务（多步骤导航）**：`commandTimeoutMs=120000`（2 分钟）
- **复杂任务（多页浏览 + 数据汇总）**：`commandTimeoutMs=180000`（3 分钟）

## 性能基准测试

| 任务类型 | 示例 | 执行时间 | 推荐超时时间 |
|---------|---------|----------|---------------------|
| **简单** | 在 Google 上读取按钮文本 | 13 秒 | 30 秒（30000 毫秒） |
| **中等** | 在 Wikipedia 上搜索、导航并汇总内容 | 76 秒 | 2 分钟（120000 毫秒） |
| **复杂** | 多页浏览 + 处理外部链接 | 约 90 秒以上 | 3 分钟（180000 毫秒） |

**注意：** OpenClaw 的网关超时设置为 10 秒，如果超时命令会立即失败，但会继续在后台运行。结果会在任务完成后通过系统消息显示。

## 限制因素

- **域名权限**：Claude Code 的 Chrome 扩展程序可能需要对新域名请求用户授权（此时无法自动化操作）。
- **网关超时**：初始连接超时为 10 秒，但命令会继续在后台执行。
- **系统要求**：仅支持配备桌面环境、安装了 Chrome 且扩展程序处于激活状态的节点。

## 使用建议

- 在自动化操作时务必使用 `--dangerously-skip-permissions` 参数。
- 非交互式输出时请使用 `-p` 或 `--print` 参数。
- 为确保环境变量 PATH 正确加载，请使用 `bash -lc` 参数以登录 shell。
- 设置较长的超时时间，因为命令可能在网关超时后仍会在后台继续执行。
- Claude Code 可在同一会话中同时进行编程和浏览操作。
- 在执行浏览器任务前，请先检查系统中的原生主机进程是否正常运行。
- 对于简单的数据抓取任务，建议使用 `web_fetch` 功能（速度更快，无需处理域名权限问题）。