---
name: raindrop-cli
description: 通过 Raindrop REST API，可以从命令行管理 Raindrop.io 的书签（搜索、检查是否存在、添加、更新、删除）。当使用个人 RAINDROP_TOKEN 自动化书签的捕获和整理时，可利用此功能。
---

# Raindrop CLI

本技能提供了 `scripts/raindrop`。

## 认证

请在本地环境文件中设置 `RAINDROP_TOKEN`（推荐路径：`~/.config/openclaw/gateway.env`，权限设置为 600）。

## 安全默认设置

- 如果某个 URL 已经存在，该工具会报告这一情况，并且**不会**创建重复的条目。
- 如果未提供收集目录（collection），系统将默认使用 **未排序**（Unsorted）的目录。

## 使用方法

- `raindrop collections`：列出所有收集的目录。
- `raindrop search "query" --collection all`：根据查询条件搜索所有条目。
- `raindrop exists <url>`：检查指定的 URL 是否存在。
- `raindrop add <url> --tags tag1,tag2 --collection unsorted`：向未排序的目录中添加新的条目，并设置标签。
- `raindrop update <id> --title "New title"`：更新指定条目的标题。
- `raindrop remove <id>`：删除指定的条目。