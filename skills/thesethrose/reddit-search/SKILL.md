---
name: reddit-search
description: 在 Reddit 上搜索子版块（subreddits），并获取关于它们的信息。
homepage: https://github.com/TheSethRose/clawdbot
metadata: {"clawdbot":{"emoji":"📮","requires":{"bins":["node","npx"],"env":[]}}}
---

# Reddit搜索

在Reddit上搜索子版块（subreddits），并获取有关它们的信息。

## 快速入门

```bash
{baseDir}/scripts/reddit-search info programming
{baseDir}/scripts/reddit-search search javascript
{baseDir}/scripts/reddit-search popular 10
{baseDir}/scripts/reddit-search posts typescript 5
```

## 命令

### 获取子版块信息

```bash
{baseDir}/scripts/reddit-search info <subreddit>
```

显示子版块的订阅者数量、是否适合工作场所（NSFW）的状态、创建日期以及描述，并提供侧边栏链接。

### 搜索子版块

```bash
{baseDir}/scripts/reddit-search search <query> [limit]
```

根据查询条件搜索子版块。默认搜索结果数量为10个。

### 列出热门子版块

```bash
{baseDir}/scripts/reddit-search popular [limit]
```

列出最受欢迎的子版块。默认显示数量为10个。

### 列出新创建的子版块

```bash
{baseDir}/scripts/reddit-search new [limit]
```

列出最近创建的子版块。默认显示数量为10个。

### 获取子版块的热门帖子

```bash
{baseDir}/scripts/reddit-search posts <subreddit> [limit]
```

获取某个子版块的热门帖子（按热度排序）。默认显示数量为5个。

## 示例

```bash
# Get info about r/programming
{baseDir}/scripts/reddit-search info programming

# Search for JavaScript communities
{baseDir}/scripts/reddit-search search javascript 20

# List top 15 popular subreddits
{baseDir}/scripts/reddit-search popular 15

# List new subreddits
{baseDir}/scripts/reddit-search new 10

# Get top 5 posts from r/typescript
{baseDir}/scripts/reddit-search posts typescript 5
```