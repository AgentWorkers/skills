# 🐾 CRM 智能系统 — 智能联系人筛选

> 由 Odin's Eye Enterprises 提供 — 古老的智慧，现代的智能技术。

适用于个人 CRM 的两阶段 Berman 风格筛选及联系人评分功能。该系统能够学习您关注的重点信息。

## 功能概述

1. **第一阶段** — 快速的关键词/模式筛选（快速、高效）
2. **第二阶段** — 基于 AI 的相关性评分（更深入的分析）
3. 通过您的反馈不断学习，以提升筛选效果

## 常用指令

- “筛选我的联系人”
- “对这条潜在客户信息进行评分”
- “我应该联系谁”
- “CRM 筛选”
- “对联系人进行优先级排序”

## 使用方法

```bash
# Filter contacts from a CSV/JSON
python crm_filter.py filter contacts.json

# Score a specific contact
python crm_filter.py score "John Doe" --context "met at conference"

# Show learning stats
python crm_filter.py stats
```

## 相关文件

- `crm_filter.py` — 主要筛选引擎
- `learning.json` — 学习到的偏好设置（自动更新）

## 系统要求

- Python 3.10 及以上版本
- `ANTHROPIC_API_KEY` 环境变量（用于第二阶段的 AI 评分）

## 对于客服人员的使用说明

从技能目录中运行该工具。筛选结果将以 JSON 格式输出到标准输出（stdout）。

```bash
python crm_filter.py filter contacts.json --top 10
```

<!-- 🐾 Huginn 观察着，Muninn 记录着...