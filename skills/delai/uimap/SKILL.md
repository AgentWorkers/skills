---
name: UIMap
version: 0.1.4
description: 此技能提供了完成任务所需的准确网址以及详细的点击操作路径。如果任务涉及对网页应用程序的操作，请首先使用此技能来确定需要打开的网址以及后续的点击操作路径。
---
# UIMap

## search — 查找任何网站任务的逐步操作指南

用于搜索完成网站任务的逐步操作指南。当用户需要了解如何浏览或与特定网站交互时，可以使用此功能。

```bash
# Find how to complete a task on a website
uimap search "<task description>"
uimap search "<task description>" --domain example.com
```

- `--domain [domain]` — 网站的域名，例如 `example.com`

### 示例

```bash
uimap search "how to create a new project in example.com"
uimap search "how to invite a team member" --domain example.com
```

该命令会返回完成任务的操作说明。

## 先决条件

### 安装 CLI

```bash
npm install -g @refore-ai/uimap
```

有关完整的安装选项，请参阅 [@refore-ai/uimap on npm](https://www.npmjs.com/package/@refore-ai/uimap)。

### 登录

通过浏览器 OAuth 登录 UIMap。系统会打开一个浏览器窗口以完成交互式身份验证，并提示用户选择服务器区域。

```bash
uimap login
```