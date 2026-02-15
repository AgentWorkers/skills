---
name: english-learn-cards
description: 基于闪卡的学习方法，用于英语词汇的记忆与巩固，结合了 SQLite 数据库和 SRS（Spaced Repetition System，间隔重复学习算法）。当与 OpenClaw 代理提示系统配合使用时，该方法可适用于任何聊天平台。
---

# 英语学习卡片（SQLite + SRS）

这是一个专为 OpenClaw 设计的便携式词汇闪卡工具。

- 将卡片数据存储在 SQLite 数据库中。
- 支持 SRS（Spaced Repetition System，间隔重复学习）复习模式（评分等级为 0–3）。
- 使用一个确定性的辅助命令行工具（`scripts/words.py`）来确保卡片格式的稳定性。

## 平台说明

该工具 **与具体平台无关**（支持 Slack、Discord、WhatsApp、Telegram 等）。  
您的频道特定代理提示（agent prompt）应负责决定以下内容：
- 消息的格式（项目符号列表/标题）
- 测验的交互流程
- 用户答案的解析方式。

一个可供直接复制的提示模板位于：
- `skill/prompt-examples/AGENT_PROMPT_TEMPLATE.md`

## 数据存储

- SQLite 数据库的路径通过环境变量控制：
  - `ENGLISH_LEARN_CARDS_DB`（默认值：`~/clawd/memory/english-learn-cards.db`）

## 辅助命令行工具（必需）

请使用该辅助工具来执行所有数据库操作：

```bash
python skill/scripts/words.py init
python skill/scripts/words.py migrate
python skill/scripts/words.py add "implement" ...
python skill/scripts/words.py render "implement" --fill-audio
python skill/scripts/words.py due
python skill/scripts/words.py grade <card_id> <0-3>
```

## 安全性 / 发布注意事项

请勿提交以下内容：
- 您的 SQLite 数据库文件
- 任何与敏感信息或访问权限相关的密钥/令牌
- 一次性使用的迁移或数据增强脚本

请将仅用于本地使用的脚本保留在仓库之外（请参考 `.gitignore` 文件）。