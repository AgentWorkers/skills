---
name: browsh
description: 一款现代的基于文本的浏览器。它通过使用无头版的 Firefox 在终端中渲染网页。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["browsh","firefox"]}}}
---

# Browsh

这是一个完全现代化的基于文本的浏览器。它可以渲染故事和视频、过滤广告，并节省带宽。

## 先决条件
- `browsh` 可执行文件必须位于 `PATH` 环境变量中。
- `firefox` 可执行文件也必须位于 `PATH` 环境变量中（Browsh 使用它作为无头后端）。

**本地安装（如果安装在 `~/apps` 目录下）：**
确保您的 `PATH` 环境变量包含了以下目录：
```bash
export PATH=$HOME/apps:$HOME/apps/firefox:$PATH
```

## 使用方法

启动 Browsh：
```bash
browsh
```

打开特定的 URL：
```bash
browsh --startup-url https://google.com
```

**注意：** Browsh 是一个图形用户界面（TUI）应用程序。请在终端会话（PTY）中运行它（例如，使用 `tmux` 或带有 `pty=true` 参数的 `process` 工具）。