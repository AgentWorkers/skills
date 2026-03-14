---
name: clawhub
version: "1.0.1"
description: "从 ClawHub (https://clawhub.ai) 下载并安装相关技能。当用户需要浏览、搜索或从 ClawHub 技能注册表中下载技能时，可以使用这些工具。"
---
# ClawHub 技能管理

从 ClawHub 下载并安装技能——这是一个专为 AI 代理设计的快速技能注册平台。

## 命令

### 搜索技能

通过关键词搜索技能：

```bash
{baseDir}/clawhub-search.sh "<keyword>"
```

该命令会搜索 ClawHub 注册库，并显示匹配的技能，包括其 slug、名称、简介以及下载次数。

### 下载并安装技能

通过 slug 或 ClawHub 的 URL 下载并安装技能：

```bash
# By slug
{baseDir}/clawhub-download.sh <slug>

# By ClawHub URL (e.g., https://clawhub.ai/steipete/github)
{baseDir}/clawhub-download.sh https://clawhub.ai/owner/slug
```

该命令会：
1. 从 ClawHub 下载技能包
2. 将其解压到 `~/.agents/skills/clawhub-skills/<slug>/` 目录中
3. 显示已安装的技能信息

### 列出所有技能

浏览可用的技能（按下载次数排序）：

```bash
{baseDir}/clawhub-search.sh
```

## API 端点

ClawHub 使用以下 API 端点：

- **列出/搜索技能**：`https://wry-manatee-359.convex.site/api/v1/skills`
- **下载技能**：`https://wry-manatee-359.convex.site/api/v1/download?slug=<slug>`

## 示例

用户说：“我想从 ClawHub 下载名为 ‘github’ 的技能。”
→ 使用 `clawhub-download.sh github`

用户说：“在 ClawHub 上搜索与天气相关的技能。”
→ 使用 `clawhub-search.sh "weather"`

用户说：“安装地址为 https://clawhub.ai/steipete/summarize 的技能。”
→ 使用 `clawhub-download.sh https://clawhub.ai/steipete/summarize`

用户问：“ClawHub 上哪些技能最受欢迎？”
→ 使用 `clawhub-search.sh` 按下载次数列出热门技能