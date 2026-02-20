---
name: buffer
description: "**Buffer**：一款用于管理社交媒体的工具，支持发布计划、维护个人资料、查看待发布或已发布的更新内容以及分析社交媒体数据。同时，它还提供了用于社交媒体发布的命令行接口（CLI）。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📢", "requires": {"env": ["BUFFER_ACCESS_TOKEN"]}, "primaryEnv": "BUFFER_ACCESS_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 📢 Buffer

这是一个用于社交媒体内容管理的工具，支持创建帖子、管理发布计划以及查看分析数据的功能。

## 主要功能

- **个人资料**：列出您关联的所有社交媒体账户。
- **创建帖子**：将帖子安排发布到多个账户。
- **待发布队列**：查看已安排好的发布内容。
- **已发布帖子**：查看已发布的帖子及其相关数据（如浏览量、点赞数等）。
- **随机排序**：随机调整帖子的发布顺序。

## 运行要求

| 变量        | 必需      | 说明                          |
|------------|---------|---------------------------------------------|
| `BUFFER_ACCESS_TOKEN` | ✅       | 用于访问 Buffer API 的密钥/令牌                |
|            |          |                                  |

## 快速入门

```bash
python3 {baseDir}/scripts/buffer.py profiles
python3 {baseDir}/scripts/buffer.py create "Check out our new feature!" <profile-id>
python3 {baseDir}/scripts/buffer.py pending <profile-id>
python3 {baseDir}/scripts/buffer.py sent <profile-id>
python3 {baseDir}/scripts/buffer.py me
```

## 开发者信息

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源代码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
此工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)