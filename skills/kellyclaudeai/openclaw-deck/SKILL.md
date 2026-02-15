---
name: openclaw-deck
description: OpenClaw代理的多列聊天界面：通过启动一个本地Web界面，可以同时管理和与多个代理进行聊天。
user-invocable: true
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["node","npm"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Deck

启动 OpenClaw Deck——这是一个多列式的 Web 用户界面，用于同时与多个 OpenClaw 代理进行交互。

## 该技能的功能

当被调用时，该技能会安装所需的依赖项（如果需要的话），并启动用于展示 Deck 用户界面的 Vite 开发服务器。该界面会通过 WebSocket 代理连接到本地的 OpenClaw Gateway。

## 使用说明

1. 检查技能的根目录下是否存在 `node_modules` 文件夹。如果不存在，请在 `{baseDir}` 目录中运行 `npm install` 命令进行安装。
2. 在 `{baseDir}` 目录中运行 `npm run dev` 命令以启动开发服务器。
3. 告知用户可以通过 **http://localhost:5173** 访问该界面。
4. 介绍可用的键盘快捷键：
   - **Tab** / **Shift+Tab** — 在代理输入框之间切换焦点
   - **Cmd+1–9** — 根据数字跳转到指定的列
   - **Cmd+K** — 打开“添加代理”（Add Agent）对话框

## 使用要求

- OpenClaw Gateway 必须运行在 `ws://127.0.0.1:18789`（默认地址）上；否则用户需要通过 `.env` 文件设置 `VITE_GATEWAY_URL`。
- 确保系统中已安装 Node.js 和 npm。