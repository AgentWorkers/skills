---
name: xmtp-cli
description: >
  Run and script the XMTP CLI for testing, debugging, and interacting with XMTP conversations, groups, and messages.
  Use when the user needs init, send, list, groups, debug, sync, permissions, or content commands from the CLI.
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP 命令行界面（CLI）

使用 `xmtp` 命令可以从命令行测试、调试以及与 XMTP 对话、组和消息进行交互。这是基础技能；如需执行特定的 CLI 操作，请使用以下子技能。

## 适用场景

- 从命令行测试或调试 XMTP 功能
- 发送消息或创建/管理组
- 列出或查找对话、成员及消息
- 同步对话和消息
- 管理组权限
- 展示内容类型（文本、Markdown、附件、交易信息、深度链接、迷你应用）

## 子技能

| 子技能 | 适用场景 |
|---------|---------|
| **setup** | 初始化 CLI 并配置环境（使用 `init` 命令及环境变量） |
| **groups** | 创建私信或组，更新组元数据 |
| **send** | 向指定地址或组发送消息 |
| **list** | 列出对话、成员及消息；按地址或收件箱查找 |
| **debug** | 获取信息、解析地址、查看收件箱内容 |
| **sync** | 同步对话或所有数据 |
| **permissions** | 查看/修改组权限 |
| **content** | 展示文本、Markdown、附件、交易信息、深度链接、迷你应用等内容 |
| **debugging** | 启用 CLI 调试日志（通过设置 `XMTP_FORCE_DEBUG` 环境变量）

## 使用方法

1. 选择与所需任务匹配的子技能（例如：发送消息 → 使用 **send** 子技能）。
2. 阅读该子技能对应的 `SKILL.md` 文件及其 `rules/` 文件以获取详细操作步骤。

## 安装

```bash
npm install -g @xmtp/cli
# or
pnpm add -g @xmtp/cli
# or
yarn global add @xmtp/cli
```

## 无需安装即可使用

```bash
npx @xmtp/cli <command> <arguments>
# or pnpx / yarn dlx
```

## 帮助文档

```bash
xmtp --help
xmtp <command> --help
```

完整文档：[docs.xmtp.org](https://docs.xmtp.org)