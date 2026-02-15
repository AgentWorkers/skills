---
name: postsyncer
version: 1.0.0
description: 管理您的 PostSyncer 社交媒体工作流程。
author: abakermi
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      env: ["POSTSYNCER_API_KEY"]
---

# PostSyncer 技能

使用 PostSyncer 自动化您的社交媒体发布计划。

## 设置

1. 从 [PostSyncer 设置](https://app.postsyncer.com/settings) 获取您的 API 密钥。
2. 将其设置为：`export POSTSYNCER_API_KEY="your_key"`

## 命令

### 工作空间
列出您的工作空间。

```bash
postsyncer workspaces
```

### 帖子
列出您已安排或发布的帖子。

```bash
postsyncer posts
```

### 创建帖子
（基本文本帖子）

```bash
postsyncer create-post -w <workspace_id> -t "Hello world"
```